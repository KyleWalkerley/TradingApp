# news_sentiment.py
from newsapi import NewsApiClient
from textblob import TextBlob

NEWS_API_KEY = "f3bc50b5708744aca5cd6c4e8e7ae382"

def get_news_sentiment(ticker):
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    
    try:
        all_articles = newsapi.get_everything(q=ticker, language='en', sort_by='relevancy', page_size=5)
        articles = all_articles['articles']
        
        if not articles:
            return "No recent news found", None
        
        sentiment_score = 0
        for article in articles:
            analysis = TextBlob(article['description'] or "")
            sentiment_score += analysis.sentiment.polarity

        sentiment_score /= len(articles)
        
        sentiment_label = "🟢 Positive" if sentiment_score > 0 else "🔴 Negative" if sentiment_score < 0 else "🟡 Neutral"
        return sentiment_label, round(sentiment_score, 2)
    
    except Exception as e:
        return f"Error: {str(e)}", None
