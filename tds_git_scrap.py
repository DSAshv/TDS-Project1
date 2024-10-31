import os
import requests
import csv
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

def search_github_users(location, min_followers=50, output_file="github_users_meta.csv"):
    url = 'https://api.github.com/search/users'
    query = f'location:{location} followers:>{min_followers}'
    
    all_users = []
    page = 1

    while True:
        print(f"Fetching page {page}...")

        params = {
            'q': query,
            'per_page': 100,
            'page': page
        }
        
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            users = response.json().get("items", [])
            
            if not users:
                print("No more users found.")
                break
            
            for user in users:
                all_users.append({
                    "login": user.get("login"),
                    "id": user.get("id"),
                    "url": user.get("html_url"),
                    "repos_url": user.get("repos_url")
                })
            
            page += 1
        else:
            print(f"Failed to fetch users: {response.status_code}")
            print(response.json())
            break

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["login", "id", "url", "repos_url"])
        writer.writeheader()
        writer.writerows(all_users)

    print(f"Saved {len(all_users)} users to {output_file}")


search_github_users(location="Hyderabad", min_followers=50)
