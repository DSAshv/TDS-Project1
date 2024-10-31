import os
import csv
import requests
from dotenv import load_dotenv
import time

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

def fetch_repositories(repos_url):
    repositories = []

    response = requests.get(repos_url, headers=headers)

    if response.status_code == 403:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        sleep_duration = max(0, reset_time - int(time.time()))
        print(f"Rate limit reached. Sleeping for {sleep_duration // 60} minutes.")
        time.sleep(sleep_duration)
        return fetch_repositories(repos_url)

    elif response.status_code == 200:
        data = response.json()
        if data:
            for repo in data:
                repositories.append({
                    'login': repo['owner']['login'],
                    'full_name': repo['full_name'],
                    'created_at': repo['created_at'],
                    'stargazers_count': repo['stargazers_count'],
                    'watchers_count': repo['watchers_count'],
                    'language': repo['language'] or "",
                    'has_projects': repo['has_projects'],
                    'has_wiki': repo['has_wiki'],
                    'license_name': repo['license']['key'] if repo['license'] else "",
                    'pushed_at': repo['pushed_at']
                })

            repositories.sort(key=lambda x: x['pushed_at'], reverse=True)
            return repositories[:5]

    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return []
    
    return []


def process_and_save_repositories(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        total_users = sum(1 for row in infile) - 1
    
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = [
            'login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count',
            'language', 'has_projects', 'has_wiki', 'license_name', 'pushed_at'
        ]

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        count = 0

        for row in reader:
            count += 1
            login = row['login']
            repos_url = row['repos_url']
            
            print(f"Processing user {count}/{total_users}: {login}")
            time.sleep(2)

            user_repositories = fetch_repositories(repos_url)
            
            if (user_repositories != None  and user_repositories!=[]):
                for repo in user_repositories:
                    writer.writerow(repo)



process_and_save_repositories("/home/ashwa-22020/Desktop/github_users_meta.csv", "repositories.csv")
