import requests
import json
from datetime import datetime

# Define base URL for historical PyPI data
BASE_URL = "https://raw.githubusercontent.com/hugovk/top-pypi-packages/refs/tags/{year}.{month:02d}/top-pypi-packages.json"
BASE_URL_OLD = "https://raw.githubusercontent.com/hugovk/top-pypi-packages/refs/tags/{year}.{month:02d}/top-pypi-packages-30-days.json"

# Start tracking from September 2024
start_year = 2024
start_month = 9

# Get the current year and month
current_year = datetime.utcnow().year
current_month = datetime.utcnow().month

# Package we want to track
TARGET_PACKAGE = "transparent-background"

# Variables to track rankings
latest_rank = None
latest_downloads = None
latest_year = None
latest_month = None
highest_rank = float("inf")  # Lowest numerical value is best rank

def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None

# Loop through historical months up to the current month
for year in range(start_year, current_year + 1):
    for month in range(1, 13):
        # Skip months before the starting point (2024.09)
        if year == start_year and month < start_month:
            continue

        # Stop once we reach the current month
        if year == current_year and month > current_month:
            break

        print(f"Checking data for {year}.{month:02d}...")
        
        response = fetch_data(BASE_URL.format(year=year, month=month))
        if response is None:
            response = fetch_data(BASE_URL_OLD.format(year=year, month=month))
        
        if response is None:
            print(f"⚠️ Data not available for {year}.{month:02d}, skipping...")
            continue

        try:
            data = response.json()
            packages = data["rows"]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Error parsing data for {year}.{month:02d}: {e}")
            continue

        # Find the rank for the target package in this month
        package_found = False
        for i, package in enumerate(packages):
            if package["project"] == TARGET_PACKAGE:
                rank = i + 1  # Convert zero-based index to 1-based ranking
                downloads = package["download_count"]
                
                print(f"📊 {year}.{month:02d} - Rank: {rank}, Downloads: {downloads:,}")

                # Update latest rank (most recent data found)
                latest_rank = rank
                latest_downloads = downloads
                latest_year = year
                latest_month = month

                # Update highest rank ever achieved
                if rank < highest_rank:
                    highest_rank = rank

                package_found = True
                break  # Stop searching once found

        if not package_found:
            print(f"📦 Package '{TARGET_PACKAGE}' not found in top packages for {year}.{month:02d}")

# Save the rank data in rank.json
rank_data = {
    "package": TARGET_PACKAGE,
    "latest-rank": latest_rank,
    "latest-downloads": latest_downloads,
    "latest-data-from": f"{latest_year}.{latest_month:02d}" if latest_year and latest_month else None,
    "all-time-highest-rank": highest_rank if highest_rank != float("inf") else None,
    "last-updated": datetime.utcnow().isoformat()
}

with open("rank.json", "w", encoding="utf-8") as f:
    json.dump(rank_data, f, indent=2)

print("\n" + "="*50)
if latest_rank:
    print(f"✅ Latest Rank: {latest_rank} (from {latest_year}.{latest_month:02d})")
    print(f"✅ Latest Downloads: {latest_downloads:,}")
else:
    print(f"❌ Package '{TARGET_PACKAGE}' not found in any available data")

if highest_rank != float("inf"):
    print(f"🏆 All-Time Highest Rank: {highest_rank}")
else:
    print(f"🏆 All-Time Highest Rank: Not available")

print(f"💾 Data saved to rank.json")
