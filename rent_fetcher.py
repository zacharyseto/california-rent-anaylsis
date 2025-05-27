import requests
import json
import csv
import time

API_KEY = 'YOUR_RENTOMETER_API_KEY'  # 🔐 Replace with your actual key
CSV_FILE = 'high_income_zips.csv'
OUTPUT_FILE = 'rent_data.json'

def fetch_rent(zip_code):
    url = 'https://api.rentometer.com/v2/summary'
    params = {
        'api_key': API_KEY,
        'address': zip_code,
        'bedrooms': 3,
        'bathrooms': 2,
        'radius': 3
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error for {zip_code}: {response.status_code}")
        return None

def main():
    results = {}
    with open(CSV_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            zip_code = row['zip_code']
            print(f"Checking {zip_code}...")
            data = fetch_rent(zip_code)
            if data:
                results[zip_code] = data
                time.sleep(2)  # Delay to avoid hitting rate limits
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
