import csv
import pprint
import random
from urllib.parse import urljoin
from urllib.request import urlopen

# import openai
import pandas as pd
import requests
from bs4 import BeautifulSoup

# req = requests.get("https://cafebrazil.com/")
# print(req.content)

def extract_link_metadata(link):
    try:
        response = requests.get(link, allow_redirects=True, timeout=20)
        response.raise_for_status()  # Raise exception for bad status codes
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract metadata such as title, description, etc.
        metadata = {
            'title': soup.title.string.strip() if soup.title else None,
            # Add more metadata fields as needed
        }
        
        return metadata
    except requests.exceptions.RequestException as e:
        print("Error fetching page:", e)
        return {}

def extract_links(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=20)
        response.raise_for_status()  # Raise exception for bad status codes
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        #Extract links
        links = []  # Using a set to avoid duplicate links
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(url, link['href'])  # Make relative URLs absolute
            # metadata = extract_link_metadata(url)
            links.append(absolute_url)
        return links
    except requests.exceptions.RequestException as e:
        print("Error fetching page:", e)
        return []

# Example usage:
df = pd.read_csv('Google_all_details.csv')
res_urls = df['Website'][:7].tolist()

df['menu_links'] = None
# Ensure URLs start with "https://"
res_urls = ['https://' + url if not url.startswith('http') else url for url in res_urls]
pprint.pprint(res_urls)

# Iterate over each URL, extract links, and update DataFrame
for i, url in enumerate(res_urls):
    print(i)
    menu_links = extract_links(url)
    df.at[i, 'menu_links'] = menu_links
    
# Save the final DataFrame to a CSV file
df.to_csv('final_data.csv', index=False)

pprint.pprint(df['menu_links'][:10])


