import requests
from textblob import TextBlob

# Optional: Get your own key at https://newsapi.org
NEWS_API_KEY = "f3bc50b5708744aca5cd6c4e8e7ae382"  # Replace with your real key if needed

def get_news_headlines(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={NEWS_API_KEY}&language=en"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    headlines = [article["title"] for article in articles if article.get("title")]
    return headlines[:5]  # Return up to 5


def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Range: -1 to 1
