import requests
from datetime import datetime

def get_india_news():
    """Fetches top 10 headlines for India using a reliable RSS-to-JSON mirror."""
    try:
        # Pulls live Google News India headlines
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
    """Fetches live USD/INR, Nifty 50, and Sensex values from the internet."""
    market_results = {
        "Nifty": "Not Updated", 
        "Sensex": "Not Updated", 
        "USD_INR": "Not Updated"
    }
    
    # 1. Fetch Live Currency (USD/INR)
    try:
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5).json()
        market_results["USD_INR"] = f"₹{res['rates']['INR']:.2f}"
    except Exception:
        pass

    # 2. Fetch Nifty and Sensex via Yahoo Finance Tickers
    try:
        # ^NSEI is the ticker for Nifty 50; ^BSESN is for Sensex
        tickers = {"Nifty": "^NSEI", "Sensex": "^BSESN"}
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        for name, ticker in tickers.items():
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d"
            response = requests.get(url, headers=headers, timeout=10).json()
            
            # Extracting the most recent market price from the JSON
            price = response['chart']['result'][0]['meta']['regularMarketPrice']
            market_results[name] = f"{price:,.2f}"
    except Exception:
        pass 

    return market_results

def get_live_question():
    """Fetches a real-time historical event about India based on today's date."""
    # Fallback bank of Indian GK if the API is unreachable
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
        # Wikipedia API for events occurring on this specific calendar day
        url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{today.month}/{today.day}"
        response = requests.get(url, timeout=10).json()
        events = response.get('selected', [])
        
        # Smart Filter to prioritize Indian history/politics
        keywords = ["India", "Indian", "Delhi", "Mumbai", "Calcutta", "Madras", "Bengal", "Gandhi", "Nehru"]
        indian_event = next((e for e in events if any(k in e.get('text', '') for k in keywords)), None)

        if indian_event:
            return {
                "q": f"What happened on {month} {day}, {indian_event.get('year')} in relation to Indian history?",
                "a": indian_event.get('text')
            }
        
        # If no India-specific event exists for today, use the fallback bank
        day_index = today.timetuple().tm_yday % len(fallback_bank)
        return fallback_bank[day_index]
    except Exception:
        day_index = datetime.now().timetuple().tm_yday % len(fallback_bank)
        return fallback_bank[day_index]