import requests
import os
from dotenv import load_dotenv
import urllib.parse
import csv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("RENTOMETER_API_KEY")

if not API_KEY:
    raise ValueError("Missing RENTOMETER_API_KEY in .env file or environment.")

headers = {
    "Authorization": f"Token {API_KEY}"
}

# Remove duplicates by converting to a set, then back to list for ordering
zip_codes = list(set([
    "94030", "94112", "94112"
]))

results = []

for zip_code in zip_codes:
    print(f"Checking {zip_code}...")
    try:
        encoded_address = urllib.parse.quote(f"{zip_code}, CA")
        response = requests.get(
            "https://www.rentometer.com/api/v1/summary",
            headers=headers,
            params={
                "address": encoded_address,
                "bedrooms": 3,
                "baths": "1.5"
            }
        )

        if response.status_code == 200:
            data = response.json()
            mean_rent = data.get("mean")
            median_rent = data.get("median")
            print(f"ZIP {zip_code} - Mean: ${mean_rent}, Median: ${median_rent}")
            results.append({
                "zip_code": zip_code,
                "mean_rent": mean_rent,
                "median_rent": median_rent
            })
        else:
            print(f"Error {response.status_code} for ZIP {zip_code}: {response.text}")
            results.append({
                "zip_code": zip_code,
                "mean_rent": None,
                "median_rent": None
            })
    except Exception as e:
        print(f"Failed to fetch for {zip_code}: {e}")
        results.append({
            "zip_code": zip_code,
            "mean_rent": None,
            "median_rent": None
        })

# Write results to CSV
output_file = "rent_summary.csv"
with open(output_file, mode="w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["zip_code", "mean_rent", "median_rent"])
    writer.writeheader()
    writer.writerows(results)

print(f"\nExport complete. Data saved to {output_file}")
