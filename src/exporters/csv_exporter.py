import csv
from pathlib import Path


FIELDS = [
    "company_name",
    "industry",
    "category",
    "city",
    "state",
    "website",
    "phone",
    "rating",
    "review_count",
    "google_maps_url",
    "is_sponsored",
    "status",
]


def save_leads_to_csv(leads, filepath="data/raw/prospects.csv"):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for lead in leads:
        rows.append({
            "company_name": lead.get("company_name"),
            "industry": "roofing",
            "category": lead.get("category"),
            "city": "Miami",
            "state": "FL",
            "website": lead.get("website"),
            "phone": lead.get("phone"),
            "rating": lead.get("rating"),
            "review_count": lead.get("review_count"),
            "google_maps_url": lead.get("google_maps_url"),
            "is_sponsored": lead.get("is_sponsored"),
            "status": "new",
        })

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nCSV saved: {path}")
    print(f"Leads saved: {len(rows)}")