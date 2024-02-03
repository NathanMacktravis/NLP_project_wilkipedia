import requests
import csv

def fetch_article_details(page_id):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'pageids': page_id,
        'prop': 'extracts|pageimages',
        'exintro': True,
        'explaintext': True,
        'piprop': 'original',
        'format': 'json',
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = data['query']['pages'][page_id]
    return {
        'title': page.get('title'),
        'link': f"https://en.wikipedia.org/?curid={page_id}",
        'extract': page.get('extract'),
        'image': page.get('original', {}).get('source') if 'original' in page else 'No image available'
    }

def search_wikipedia_articles(topic):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': topic,
        'format': 'json',
        'srlimit': 10,  # On peut ajuster le nombre d'articles à récupérer
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
    with open('music_articles.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link', 'extract', 'image'])
        writer.writeheader()
        for article in articles:
            writer.writerow(article)

# Je lance la recherche d'articles sur le thème de la musique (Après je pourrai le faire pour d'autres thèmes si vous voulez)
search_wikipedia_articles('music')
