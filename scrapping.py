import requests
import csv
from datetime import datetime

def fetch_article_details(page_id):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'pageids': page_id,
        'prop': 'extracts|info|extlinks|revisions',
        'exintro': True,
        'explaintext': True,
        'inprop': 'url',
        'rvprop': 'timestamp',
        'rvslots': 'main',
        'ellimit': 'max',
        'format': 'json',
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = data['query']['pages'][page_id]
    
    # Convert the timestamp to a readable format
    timestamp = page['revisions'][0]['timestamp']
    publication_date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').date()

    return {
        'title': page.get('title'),
        'url': page.get('fullurl'),
        'extract': page.get('extract'),
        'publication_date': publication_date,
        'references': [link['*'] for link in page.get('extlinks', [])]  # List of external links
    }

def search_wikipedia_articles(topic):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': topic,
        'format': 'json',
        'srlimit': 100,  # The parameter to adjust the number of articles to retrieve
    }
    headers = {
        'User-Agent': 'nathan-wilfried.wandji-tabeko@efrei.net'  
    }
    response = requests.get(url, headers=headers, params=params)
    search_results = response.json()['query']['search']
    
    articles = []
    for result in search_results:
        page_id = str(result['pageid'])
        article_details = fetch_article_details(page_id)
        articles.append(article_details)
    
    # Write to CSV
    with open('wikipedia_articles.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'url', 'extract', 'publication_date', 'references'])
        writer.writeheader()
        for article in articles:
            writer.writerow(article)

# Use of the function
search_wikipedia_articles('animals')
