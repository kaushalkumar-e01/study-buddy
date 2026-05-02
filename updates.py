import requests
import time
from datetime import datetime

def get_india_news():
    """Fetches top 10 headlines for India using a reliable RSS-to-JSON mirror."""
    try:
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://news.google.com/rss/headlines/section/topic/NATION?hl=en-IN&gl=IN&ceid=IN:en"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('items', [])
            return [{'title': item.get('title'), 'link': item.get('link')} for item in articles[:10]]
        return []
    except Exception:
        return []

def get_market_data():
    """Fetches live USD/INR and Market data."""
    market_results = {
        "Nifty": "Not Updated", 
        "Sensex": "Not Updated", 
        "USD_INR": "Not Updated"
    }
    
    # 1. ✅ USD/INR via Yahoo Finance (FIXED)
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/INR=X?interval=1m&range=1d"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10).json()

        price = response['chart']['result'][0]['meta']['regularMarketPrice']
        market_results["USD_INR"] = f"₹{price:.2f}"

    except Exception as e:
        market_results["USD_INR"] = f"Error: {str(e)}"

    # 2. Fetch Nifty and Sensex via Yahoo Finance (UNCHANGED)
    try:
        tickers = {"Nifty": "^NSEI", "Sensex": "^BSESN"}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        for name, ticker in tickers.items():
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d"
            response = requests.get(url, headers=headers, timeout=10).json()
            
            price = response['chart']['result'][0]['meta']['regularMarketPrice']
            market_results[name] = f"{price:,.2f}"
    except Exception:
        pass 

    return market_results

def get_live_question():
    """Fetches a real-time historical event about India using compliant 2026 headers."""
    fallback_bank = [
        {"q": "Who was the first woman Prime Minister of India?", "a": "Indira Gandhi"},
        {"q": "Which river is known as the 'Dakshin Ganga'?", "a": "Godavari"},
        {"q": "Who is known as the 'Iron Man of India'?", "a": "Sardar Vallabhbhai Patel"},
        {"q": "In which year did India adopt its Constitution?", "a": "1950"},
        {"q": "Which Indian city is known as the 'Silicon Valley of India'?", "a": "Bengaluru"}
    ]
    try:
        today = datetime.now()
        month, day = today.strftime("%B"), today.day
        
        headers = {'User-Agent': 'StudyBuddy/2.0 (kaushal@bmsce.edu) Streamlit/1.41'}
        url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{today.month}/{today.day}"
        response = requests.get(url, headers=headers, timeout=10).json()
        
        events = response.get('selected', [])
        
        keywords = ["India", "Indian", "Delhi", "Mumbai", "Calcutta", "Madras", "Bengal", "Gandhi", "Nehru"]
        indian_event = next((e for e in events if any(k in e.get('text', '') for k in keywords)), None)

        if indian_event:
            return {
                "q": f"What happened on {month} {day}, {indian_event.get('year')} in relation to Indian history?",
                "a": indian_event.get('text')
            }
        
        day_index = today.timetuple().tm_yday % len(fallback_bank)
        return fallback_bank[day_index]
    except Exception:
        day_index = datetime.now().timetuple().tm_yday % len(fallback_bank)
        return fallback_bank[day_index]