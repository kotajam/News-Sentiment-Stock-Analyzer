import requests
import json
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import NEWS_API_KEY

class SimpleNewsCollector:

    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"

    def get_news_for_company(self, company_name):
        print(f"Searching for news about {company_name}...")

        today = datetime.now()
        week_ago = today - timedelta(days=7)

        parameters = {
            'q': company_name,
            'from': week_ago.strftime('%Y-%m-%d'),
            'to': today.strftime('%Y-%m-%d'),
            'sortBy': 'popularity',
            'apiKey': self.api_key,
            'language': 'en'
        }

        try:
            response = requests.get(self.base_url, params=parameters)

            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                print(f"Found {len(articles)} articles!")
                return articles
            else:
                print(f"Error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Something went wrong: {e}")
            return []

    def display_articles(self, articles):

        if not articles:
            print("No articles to display")
            return

        print("\n" + "="*50)
        print("NEWS ARTICLES FOUND:")
        print("="*50)

        for i, article in enumerate(articles[:5], 1):
            print(f"\n{i}. {article.get('title', 'No title')}")
            print(f"   Source: {article.get('source', {}).get('name', 'Unknown')}")
            print(f"   Date: {article.get('publishedAt', 'Unknown date')}")
            print(f"   Description: {article.get('description', 'No description')[:100]}...")
            print("-" * 50)

if __name__ == "__main__":
    collector = SimpleNewsCollector()
    articles = collector.get_news_for_company("Apple")
    collector.display_articles(articles)