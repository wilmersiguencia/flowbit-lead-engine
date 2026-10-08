from src.scrapers.google_maps import search_google_maps


def main():
    print("================================")
    print("      FLOWBIT LEAD ENGINE")
    print("================================")

    leads = search_google_maps(
        query="roofing contractors Miami Florida",
        max_results=20,
    )

    print(f"\nBusinesses found: {len(leads)}")


if __name__ == "__main__":
    main()