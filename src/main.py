from src.scrapers.google_maps import search_google_maps
from src.exporters.csv_exporter import save_leads_to_csv

def main():
    print("================================")
    print("      FLOWBIT LEAD ENGINE")
    print("================================")

    leads = search_google_maps(
        query="roofing contractors Miami Florida",
        max_results=20,
    )

    print(f"\nBusinesses found: {len(leads)}")

    save_leads_to_csv(leads)

    for index, lead in enumerate(leads, start=1):
        print(f"\n--- LEAD {index} ---")
        print(f"Company: {lead['company_name']}")
        print(f"Category: {lead['category']}")
        print(f"Address: {lead['address']}")
        print(f"Phone: {lead['phone']}")
        print(f"Rating: {lead['rating']}")
        print(f"Website: {lead['website']}")
        print(f"Google Maps: {lead['google_maps_url']}")
        print(f"Sponsored: {lead['is_sponsored']}")


if __name__ == "__main__":
    main()