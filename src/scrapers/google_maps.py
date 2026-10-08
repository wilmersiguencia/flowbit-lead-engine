from playwright.sync_api import sync_playwright


def search_google_maps(query: str, max_results: int = 20) -> list[dict]:
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

        page.goto(url, wait_until="domcontentloaded")

        page.wait_for_timeout(3000)

        print(f"Searching Google Maps for: {query}")

        # TODO:
        # Extract business cards here.

        browser.close()

    return results