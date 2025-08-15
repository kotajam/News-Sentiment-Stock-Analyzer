from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SimpleSentimentAnalyzer:

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def analyze_text(self, text):
        if not text:
            return None

        blob = TextBlob(text)
        textblob_score = blob.sentiment.polarity

        vader_scores = self.vader.polarity_scores(text)

        result = {
            'textblob_score': textblob_score,
            'vader_positive': vader_scores['pos'],
            'vader_negative': vader_scores['neg'],
            'vader_neutral': vader_scores['neu'],
            'vader_compound': vader_scores['compound'],
            'overall_sentiment': self._get_sentiment_label(vader_scores['compound'])
        }

        return result

    def _get_sentiment_label(self, score):
        if score >= 0.05:
            return "POSITIVE"
        elif score <= -0.05:
            return "NEGATIVE"
        else:
            return "NEUTRAL"

    def analyze_article(self, article):
        text = f"{article.get('title', '')} {article.get('description', '')}"

        sentiment = self.analyze_text(text)

        return {
            'title': article.get('title', 'No title'),
            'source': article.get('source', {}).get('name', 'Unknown'),
            'sentiment': sentiment
        }

if __name__ == "__main__":
    analyzer = SimpleSentimentAnalyzer()

    test_headlines = [
        "Apple reports record-breaking profits and amazing growth",
        "Company faces lawsuit and declining sales",
        "Stock price remains stable amid market uncertainty"
    ]

    print("SENTIMENT ANALYSIS TEST")
    print("=" * 50)

    for headline in test_headlines:
        result = analyzer.analyze_text(headline)
        print(f"\nHeadline: {headline}")
        print(f"Sentiment: {result['overall_sentiment']}")
        print(f"Score: {result['vader_compound']:.3f}")
        print("-" * 30)