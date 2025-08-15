# src/stock_data.py
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class SimpleStockData:
    """Fetches stock prices and calculates changes"""

    def __init__(self):
        # Keep common names for convenience, but not required
        self.common_names = {
            'Apple': 'AAPL',
            'Microsoft': 'MSFT',
            'Google': 'GOOGL',
            'Amazon': 'AMZN',
            'Tesla': 'TSLA',
            'Meta': 'META',
            'Facebook': 'META',
        }

    def validate_ticker(self, ticker_symbol):
        """Check if a ticker exists and get company info"""
        try:
            stock = yf.Ticker(ticker_symbol.upper())
            info = stock.info

            # Check if we got valid data
            if info and 'longName' in info:
                return {
                    'valid': True,
                    'ticker': ticker_symbol.upper(),
                    'name': info.get('longName', 'Unknown Company'),
                    'sector': info.get('sector', 'Unknown'),
                    'industry': info.get('industry', 'Unknown'),
                    'market_cap': info.get('marketCap', 0),
                    'exchange': info.get('exchange', 'Unknown')
                }
            return {'valid': False}
        except:
            return {'valid': False}

    def search_ticker(self, query):
        """
        Search for a stock ticker - tries multiple approaches
        Returns the most likely ticker symbol
        """
        query = query.strip()

        # Method 1: Check if it's already a valid ticker
        if len(query) <= 5 and query.replace('.', '').replace('-', '').isalpha():
            ticker_check = self.validate_ticker(query)
            if ticker_check['valid']:
                print(f"✅ Found: {ticker_check['name']} ({ticker_check['ticker']})")
                return ticker_check['ticker']

        # Method 2: Check common names dictionary
        for name, ticker in self.common_names.items():
            if query.lower() == name.lower():
                print(f"✅ Found common stock: {name} ({ticker})")
                return ticker

        # Method 3: Try using yfinance's search/download capability
        # Try common variations
        variations = [
            query.upper(),  # AAPL
            query.upper().replace(' ', '-'),  # BRK-B
            query.upper().replace(' ', '.'),  # BRK.B
            query.upper().replace(' ', ''),   # BRKB
        ]

        for variant in variations:
            if len(variant) <= 10:  # Tickers are usually short
                ticker_check = self.validate_ticker(variant)
                if ticker_check['valid']:
                    print(f"✅ Found: {ticker_check['name']} ({ticker_check['ticker']})")
                    return ticker_check['ticker']

        # Method 4: If nothing found, return the original query uppercase
        print(f"⚠️ Could not verify '{query}', trying as ticker '{query.upper()}'")
        return query.upper()

    def get_stock_ticker(self, company_name):
        """Convert company name to stock ticker - now searches broadly"""
        return self.search_ticker(company_name)

    def get_stock_data(self, company_name, days=30):
        """
        Get stock price data for a company

        company_name: Company name or ticker symbol
        days: Number of days of history to fetch
        """
        ticker = self.get_stock_ticker(company_name)
        print(f"📊 Fetching stock data for {ticker}...")

        try:
            # Create ticker object
            stock = yf.Ticker(ticker)

            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Fetch the data
            hist = stock.history(start=start_date, end=end_date)

            if hist.empty:
                print(f"❌ No data found for {ticker}")
                print("   Tips: • Make sure the ticker symbol is correct")
                print("         • Try using the exact ticker (e.g., 'AAPL' for Apple)")
                print("         • Some international stocks need exchange suffix (e.g., 'NESN.SW')")
                return None

            # Get company info for display
            try:
                info = stock.info
                if info and 'longName' in info:
                    print(f"✅ Got data for: {info['longName']}")
            except:
                pass

            print(f"✅ Retrieved {len(hist)} days of stock data")
            return hist

        except Exception as e:
            print(f"❌ Error fetching stock data: {e}")
            print("\n💡 Tips for searching stocks:")
            print("   • US Stocks: Just use ticker (AAPL, MSFT, TSLA)")
            print("   • ETFs: SPY, QQQ, VOO, etc.")
            print("   • International: May need suffix (.L for London, .TO for Toronto)")
            print("   • Crypto stocks: COIN, MSTR, RIOT")
            print("   • Penny stocks: Full ticker required")
            return None

    def calculate_price_change(self, stock_data):
        """Calculate how much the stock price changed"""
        if stock_data is None or stock_data.empty:
            return None

        # Get first and last closing prices
        first_price = stock_data['Close'].iloc[0]
        last_price = stock_data['Close'].iloc[-1]

        # Calculate change
        price_change = last_price - first_price
        percent_change = (price_change / first_price) * 100

        return {
            'first_price': round(first_price, 2),
            'last_price': round(last_price, 2),
            'price_change': round(price_change, 2),
            'percent_change': round(percent_change, 2),
            'trend': 'UP 📈' if price_change > 0 else 'DOWN 📉'
        }

    def get_current_price(self, company_name):
        """Get the current stock price"""
        ticker = self.get_stock_ticker(company_name)

        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='1d')

            if not data.empty:
                current_price = data['Close'].iloc[-1]
                return round(current_price, 2)
            return None

        except:
            return None

    def get_stock_info(self, company_name):
        """Get detailed information about a stock"""
        ticker = self.get_stock_ticker(company_name)

        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'ticker': ticker,
                'name': info.get('longName', 'Unknown'),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'employees': info.get('fullTimeEmployees', 'Unknown'),
                'country': info.get('country', 'Unknown'),
                'website': info.get('website', 'Unknown'),
                'description': info.get('longBusinessSummary', 'No description available')[:200] + '...'
            }
        except:
            return None

# Test the stock data fetcher
if __name__ == "__main__":
    stock_fetcher = SimpleStockData()

    print("🧪 TESTING STOCK DATA FETCHER")
    print("=" * 50)

    # Test with various ticker types
    test_tickers = [
        "AAPL",      # Standard US stock
        "MSFT",      # Another US stock
        "SPY",       # ETF
        "BRK-B",     # Stock with hyphen
        "TSM",       # Foreign company (Taiwan)
        "COIN",      # Crypto-related
        "GME",       # Meme stock
        "PLTR",      # Tech stock
        "RIVN",      # EV stock
        "UNKNOWN123" # Invalid ticker
    ]

    for ticker in test_tickers[:3]:  # Test first 3
        print(f"\n📊 Testing: {ticker}")
        print("-" * 30)

        # Validate ticker
        validation = stock_fetcher.validate_ticker(ticker)
        if validation['valid']:
            print(f"✅ Valid ticker: {validation['name']}")
            print(f"   Sector: {validation['sector']}")
            print(f"   Exchange: {validation['exchange']}")

            # Get current price
            price = stock_fetcher.get_current_price(ticker)
            if price:
                print(f"   Current Price: ${price}")
        else:
            print(f"❌ Invalid or not found: {ticker}")

    # Interactive test
    print("\n" + "=" * 50)
    print("Try searching for any stock!")
    print("Examples: AAPL, GOOGL, SPY, NVDA, AMZN, BTC-USD")
    user_input = input("Enter ticker to search: ").strip()

    if user_input:
        data = stock_fetcher.get_stock_data(user_input, days=7)
        if data is not None:
            changes = stock_fetcher.calculate_price_change(data)
            print(f"\n📈 Results:")
            print(f"   Last Price: ${changes['last_price']}")
            print(f"   7-Day Change: {changes['percent_change']}%")