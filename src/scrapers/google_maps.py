import re

from playwright.sync_api import sync_playwright


def extract_rating(card) -> float | None:
    rating_element = card.locator(
        '[role="img"][aria-label*="estrellas"]'
    ).first

    if rating_element.count() == 0:
        return None

    aria_label = rating_element.get_attribute("aria-label")

    if not aria_label:
        return None

    match = re.search(r"([0-5](?:\.\d)?)", aria_label)

    if not match:
        return None

    return float(match.group(1))


def extract_phone(card) -> str | None:
    phone_element = card.locator(".UsdlK").first

    if phone_element.count() == 0:
        return None

    phone = phone_element.inner_text().strip()

    return phone if phone else None


def extract_address(card) -> str | None:
    address_elements = card.locator(".W4Efsd")

    for i in range(address_elements.count()):
        block = address_elements.nth(i)

        # Look specifically for the text containing the business category
        # and address.
        spans = block.locator("span")

        for j in range(spans.count()):
            text = spans.nth(j).inner_text().strip()

            if not text:
                continue

            if "·" not in text:
                continue

            parts = [
                part.strip()
                for part in text.split("·")
                if part.strip()
            ]

            for part in parts:
                if any(char.isdigit() for char in part):
                    if re.search(
                        r"\+?1[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
                        part,
                    ):
                        continue

                    if part.lower() in {
                        "abierto",
                        "cerrado",
                    }:
                        continue

                    return part

    return None


def extract_website(card) -> str | None:
    # Sponsored businesses can expose Google's advertising redirect
    # instead of the real business website.
    if is_sponsored(card):
        return None

    website_link = card.locator(
        'a[aria-label^="Visitar el sitio web"]'
    ).first

    if website_link.count() == 0:
        return None

    href = website_link.get_attribute("href")

    if not href:
        return None

    # Never treat Google's internal ad redirects as a business website.
    if href.startswith("/aclk"):
        return None

    return href


def extract_maps_url(card) -> str | None:
    business_link = card.locator("a.hfpxzc").first

    if business_link.count() == 0:
        return None

    return business_link.get_attribute("href")


def is_sponsored(card) -> bool:
    sponsored = card.locator(
        '[aria-label="Patrocinado"]'
    )

    return sponsored.count() > 0


def parse_business_card(card) -> dict:
    name_element = card.locator("a.hfpxzc").first

    company_name = None

    if name_element.count() > 0:
        company_name = name_element.get_attribute("aria-label")

    return {
        "company_name": company_name,
        "address": extract_address(card),
        "phone": extract_phone(card),
        "rating": extract_rating(card),
        "website": extract_website(card),
        "google_maps_url": extract_maps_url(card),
        "is_sponsored": is_sponsored(card),
        "category": extract_category(card),
    }



def search_google_maps(
    query: str,
    max_results: int = 20,
) -> list[dict]:

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1440, "height": 900}
        )

        url = (
            "https://www.google.com/maps/search/"
            f"{query.replace(' ', '+')}"
        )

        print(f"Opening Google Maps: {url}")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        page.wait_for_timeout(5000)

        print(f"Page title: {page.title()}")

        feed = page.locator('[role="feed"]')

        if feed.count() == 0:
            print("Could not find Google Maps results feed.")
            browser.close()
            return results

        print("Google Maps results feed found.")

        for _ in range(5):
            feed.evaluate(
                "(element) => element.scrollTop = element.scrollHeight"
            )

            page.wait_for_timeout(1500)

        cards = feed.locator('div[role="article"]')

        print(f"Business cards detected: {cards.count()}")

        limit = min(cards.count(), max_results)

        for i in range(limit):
            card = cards.nth(i)

            try:
                lead = parse_business_card(card)

                results.append(lead)

            except Exception as error:
                print(f"Could not parse card {i}: {error}")

        browser.close()

    return results

def extract_category(card) -> str | None:
    blocks = card.locator("div.W4Efsd")

    for i in range(blocks.count()):
        texts = [
            text.strip()
            for text in blocks.nth(i).locator("span").all_inner_texts()
            if text.strip()
        ]

        for text in texts:
            lower = text.lower()

            if any(char.isdigit() for char in text):
                continue

            if lower in {
                "abierto",
                "cerrado",
            }:
                continue

            if lower.startswith(("cierra", "abre")):
                continue

            if len(text) < 3:
                continue

            if text in {"·"}:
                continue

            return text

    return None