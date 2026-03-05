"""Real-time news updates via WebSocket"""
from flask_socketio import emit
import threading
import time

def background_news_updates(socketio):
    """Background thread for sending news updates"""
    from app.api.news_api import NewsAPI
    
    news_api = NewsAPI()
    last_articles = set()
    
    while True:
        try:
            result = news_api.get_top_headlines(page_size=10)
            articles = result.get('articles', [])
            
            # Check for new articles
            current_articles = {a['url'] for a in articles if a.get('url')}
            new_articles = [a for a in articles if a.get('url') not in last_articles]
            
            if new_articles and socketio:
                socketio.emit('news_update', {
                    'new_count': len(new_articles),
                    'articles': new_articles[:3]  # Send first 3 new articles
                }, namespace='/news')
            
            last_articles = current_articles
            time.sleep(300)  # Check every 5 minutes
            
        except Exception as e:
            print(f"Error in news updates: {e}")
            time.sleep(600)
