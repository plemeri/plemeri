import requests
import json
from datetime import datetime

# Define base URL for historical PyPI data
BASE_URL = "https://raw.githubusercontent.com/hugovk/top-pypi-packages/refs/tags/{year}.{month:02d}/top-pypi-packages-30-days.json"

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
highest_rank = float("inf")  # Lowest numerical value is best rank

# Loop through historical months up to the current month
for year in range(start_year, current_year + 1):
    for month in range(1, 13):
        # Skip months before the starting point (2024.09)
        if year == start_year and month < start_month:
            continue

        # Stop once we reach the current month
        if year == current_year and month > current_month:
            break

        # Construct the URL for the JSON file
        json_url = BASE_URL.format(year=year, month=month)
        print(f"Fetching data from: {json_url}")

        # Fetch JSON data
        response = requests.get(json_url)
        if response.status_code != 200:
            print(f"⚠️ Data not available for {year}.{month:02d}, skipping...")
            continue

        data = response.json()
        packages = data["rows"]

        # Find the rank for the target package in this month
        for i, package in enumerate(packages):
            if package["project"] == TARGET_PACKAGE:
                rank = i + 1  # Convert zero-based index to 1-based ranking
                downloads = package["download_count"]

                # Update latest rank (last fetched month)
                if year == current_year and month == current_month:
                    latest_rank = rank
                    latest_downloads = downloads

                # Update highest rank ever achieved
                if rank < highest_rank:
                    highest_rank = rank

                break  # Stop searching once found

# Save the rank data in rank.json
rank_data = {
    "latest-rank": latest_rank,
    "latest-downloads": latest_downloads,
    "all-time-highest-rank": highest_rank
}

with open("rank.json", "w", encoding="utf-8") as f:
    json.dump(rank_data, f, indent=2)

print(f"✅ Latest Rank: {latest_rank}")
print(f"✅ Latest Downloads: {latest_downloads}")
print(f"🏆 All-Time Highest Rank: {highest_rank}")
