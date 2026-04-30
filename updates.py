import requests
from datetime import datetime

def get_india_news():
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
    try:
        # Fetching latest USD/INR from a public API
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        usd_to_inr = res['rates']['INR']
        
        # We are leaving Nifty and Sensex as "Not Updated" because free APIs 
        # for NSE/BSE often require paid keys or complex scraping.
        return {
            "Nifty": "Not Updated", 
            "Sensex": "Not Updated", 
            "USD_INR": f"₹{usd_to_inr:.2f}"
        }
    except Exception:
        # If the internet is down, everything shows as Not Updated
        return {
            "Nifty": "Not Updated", 
            "Sensex": "Not Updated", 
            "USD_INR": "Not Updated"
        }

def get_live_question():
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
        url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{today.month}/{today.day}"
        response = requests.get(url, timeout=10).json()
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