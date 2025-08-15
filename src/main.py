import sys
import os
from datetime import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from news_collector import SimpleNewsCollector
from sentiment_analyzer import SimpleSentimentAnalyzer
from stock_data import SimpleStockData

class NewsStockAnalyzer:

    def __init__(self):
        print("Initializing")
        self.news_collector = SimpleNewsCollector()
        self.sentiment_analyzer = SimpleSentimentAnalyzer()
        self.stock_data = SimpleStockData()
        self.search_history = []
        print("Begin\n")

    def analyze_company(self, company_name):
        self.search_history.append({
            'company': company_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print("=" * 60)
        print(f"ANALYZING: {company_name}")
        print("=" * 60)

        print("\nSTEP 1: Pulling News Articles")
        articles = self.news_collector.get_news_for_company(company_name)

        if not articles:
            print("No articles found. Try again.")
            return

        print(f"\nSTEP 2: Analyzing sentiment of {len(articles)} articles")

        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for article in articles[:10]:
            result = self.sentiment_analyzer.analyze_article(article)
            sentiments.append(result)

            sentiment_label = result['sentiment']['overall_sentiment']
            if 'POSITIVE' in sentiment_label:
                positive_count += 1
            elif 'NEGATIVE' in sentiment_label:
                negative_count += 1
            else:
                neutral_count += 1

        avg_sentiment = sum(s['sentiment']['vader_compound'] for s in sentiments) / len(sentiments)

        print(f"\nSTEP 3: Pulling stock data")
        stock_history = self.stock_data.get_stock_data(company_name, days=7)
        current_price = self.stock_data.get_current_price(company_name)

        if stock_history is not None:
            price_changes = self.stock_data.calculate_price_change(stock_history)
        else:
            price_changes = None

        self.display_results(
            company_name,
            sentiments[:5],
            positive_count,
            negative_count,
            neutral_count,
            avg_sentiment,
            current_price,
            price_changes
        )

    def display_results(self, company_name, sentiments, pos_count, neg_count,
                        neu_count, avg_sentiment, current_price, price_changes):

        print("\n" + "=" * 60)
        print("Results")
        print("=" * 60)

        print("\nSentiment Summary:")
        print(f"  Positive Articles: {pos_count}")
        print(f"  Negative Articles: {neg_count}")
        print(f"  Neutral Articles: {neu_count}")
        print(f"  Average Sentiment Score: {avg_sentiment:.3f}")

        if avg_sentiment > 0.1:
            print(f"  Overall: Positive Sentiment")
        elif avg_sentiment < -0.1:
            print(f"  Overall: Negative Sentiment")
        else:
            print(f"  Overall: Neutral Sentiment")

        print("\nStock Information:")
        if current_price:
            print(f"  Current Price: ${current_price}")

        if price_changes:
            print(f"  7-Day Change: ${price_changes['price_change']} ({price_changes['percent_change']}%)")
            print(f"  Trend: {price_changes['trend']}")

        print("\nTop Headlines:")
        for i, item in enumerate(sentiments, 1):
            print(f"\n  {i}. {item['title'][:80]}...")
            print(f"     Source: {item['source']}")
            print(f"     Sentiment: {item['sentiment']['overall_sentiment']}")

        print("\n" + "=" * 60)
        print("Conclusion:")
        print("=" * 60)

        if avg_sentiment > 0.1:
            if price_changes and price_changes['percent_change'] > 0:
                print("Positive news & Rising stock = Bullish")
                print("   The positive sentiment aligns with upward price movement.")
            else:
                print("Positive news but stock not rising yet")
                print("   Could be a buying opportunity if news impact is delayed.")
        elif avg_sentiment < -0.1:
            if price_changes and price_changes['percent_change'] < 0:
                print("Negative news + Falling stock = Bearish")
                print("   The negative sentiment aligns with downward price movement.")
            else:
                print("Negative news but stock holding steady")
                print("   Market might have already priced in the bad news.")
        else:
            print("Neutral sentiment - No strong signals")
            print("   Consider other factors before making investment decisions.")

        print("\nDISCLAIMER: This is for educational purposes only!")
        print("   Always do your own research before investing.")
        print("=" * 60)

def main_menu():
    analyzer = NewsStockAnalyzer()

    while True:
        print("\n" + "=" * 60)
        print("News Sentiment Stock Analyzer")
        print("=" * 60)
        print("\nOptions:")
        print("  1. Analyze any company (type the name)")
        print("  2. Quick analyze popular companies")
        print("  3. Analyze multiple companies")
        print("  4. View analysis history")
        print("  0. Exit")

        choice = input("\nEnter your choice (0-4): ").strip()

        if choice == '0':
            print("\nThanks!")
            break

        elif choice == '1':
            print("\nEnter a stock ticker symbol or company name")
            print("Examples of tickers:")
            print("  US Stocks: AAPL, MSFT, TSLA, NVDA, AMD")
            print("  ETFs: SPY, QQQ, VOO, VTI")
            print("  Crypto stocks: COIN, MSTR, RIOT")
            print("  International: TSM, BABA, NIO, SONY")
            print("  Penny stocks: Any valid ticker")
            print("\nTip: Using the ticker symbol (e.g., 'AAPL') is more reliable than company name")

            company = input("\nEnter ticker or company name: ").strip()

            if company:
                print(f"\nSearching for {company}...")
                analyzer.analyze_company(company)
            else:
                print("No input entered.")

        elif choice == '2':
            print("\nPopular Companies:")
            print("  1. Apple (AAPL)")
            print("  2. Microsoft (MSFT)")
            print("  3. Tesla (TSLA)")
            print("  4. Amazon (AMZN)")

            quick_choice = input("\nSelect company (1-8): ").strip()

            companies = {
                '1': 'Apple',
                '2': 'Microsoft',
                '3': 'Tesla',
                '4': 'Amazon',
            }

            if quick_choice in companies:
                analyzer.analyze_company(companies[quick_choice])
            else:
                print("Invalid selection.")

        elif choice == '3':
            print("\nEnter company names or tickers separated by commas")
            print("Example: AAPL, MSFT, TSLA  or  Apple, Microsoft, Tesla")
            companies_input = input("Companies/Tickers: ").strip()

            if companies_input:
                companies = [c.strip() for c in companies_input.split(',')]
                print(f"\nAnalyzing {len(companies)} companies")

                for company in companies:
                    print(f"\n{'='*60}")
                    analyzer.analyze_company(company)
                    print("\nPausing before next company")
                    time.sleep(2)

        elif choice == '4':
            print("\nANALYSIS HISTORY (This Session)")
            print("=" * 60)

            if analyzer.search_history:
                for i, search in enumerate(analyzer.search_history, 1):
                    print(f"{i}. {search['company']} - {search['timestamp']}")
            else:
                print("No searches yet this session.")

            print("\nTip: Check the 'outputs' folder for saved reports")

        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()