import os
import csv
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

def clean_company_name(company):
    if company:
        company = company.strip()
        if company.startswith('@'):
            company = company[1:]
        company = company.upper()
    return company or ""

def fetch_user_data(user_id):
    url = f"https://api.github.com/user/{user_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Fetched " + user_id)
        return response.json()
    else:
        print(f"Failed to fetch data for user ID {user_id}: {response.status_code}")
        return None

def process_and_save_users(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = [
            'login', 'name', 'company', 'location', 'email', 'hireable', 'bio',
            'public_repos', 'followers', 'following', 'created_at'
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            user_id = row['id']
            user_data = fetch_user_data(user_id)
            
            if user_data:
                writer.writerow({
                    'login': user_data.get('login', ''),
                    'name': user_data.get('name', ''),
                    'company': clean_company_name(user_data.get('company', '')),
                    'location': user_data.get('location', ''),
                    'email': user_data.get('email', ''),
                    'hireable': user_data.get('hireable', ''),
                    'bio': user_data.get('bio', ''),
                    'public_repos': user_data.get('public_repos', 0),
                    'followers': user_data.get('followers', 0),
                    'following': user_data.get('following', 0),
                    'created_at': user_data.get('created_at', '')
                })

process_and_save_users("/home/ashwa-22020/Desktop/github_users_meta.csv", "users.csv")
