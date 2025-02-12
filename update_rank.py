import requests
import json

# Fetch the PyPI statistics JSON
url = "https://raw.githubusercontent.com/hugovk/top-pypi-packages/refs/heads/main/top-pypi-packages-30-days.json"
response = requests.get(url)

if response.status_code != 200:
    print("❌ Failed to fetch PyPI data")
    exit()

data = response.json()
top_packages = data["rows"]

# Find the ranking and download count of "transparent-background"
rank = None
download_count = None

for i, package in enumerate(top_packages):
    if package["project"] == "transparent-background":
        rank = i + 1  # Convert zero-based index to 1-based ranking
        download_count = package["download_count"]
        break

if rank is None:
    print("⚠️ Package 'transparent-background' not found in the top PyPI list!")
    exit()

# Prepare the JSON output
rank_data = {
    "transparent-background-rank": rank,
    "transparent-background-downloads": download_count
}

# Save the rank and download count to a JSON file
with open("rank.json", "w", encoding="utf-8") as f:
    json.dump(rank_data, f, indent=2)

print(f"✅ Rank extracted: {rank}")
print(f"✅ Download count: {download_count}")
