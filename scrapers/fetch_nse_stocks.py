"""
Fetch live NSE stock list using yfinance and NSE API
Updates INDIAN_STOCKS dynamically
"""
import yfinance as yf
import requests
import json
from typing import Set
import logging

logger = logging.getLogger(__name__)

def get_nse_stocks_from_yfinance() -> Set[str]:
    """
    Get NSE stocks using yfinance
    Note: yfinance doesn't have a direct API for all NSE stocks
    This is a fallback method
    """
    # Common NSE indices
    indices = [
        '^NSEI',  # Nifty 50
        '^NSEBANK',  # Bank Nifty
        '^CNXIT',  # Nifty IT
    ]
    
    stocks = set()
    for index in indices:
        try:
            ticker = yf.Ticker(index)
            # This won't work directly, yfinance doesn't provide constituents
            # Keeping as placeholder
            pass
        except Exception as e:
            logger.error(f"Error fetching {index}: {e}")
    
    return stocks


def get_nse_stocks_from_api() -> Set[str]:
    """
    Get live NSE stock list from NSE India API
    Returns set of stock symbols
    """
    stocks = set()
    
    try:
        # NSE API for equity list
        url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        # Create session to handle cookies
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        
        response = session.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            for stock in data.get('data', []):
                symbol = stock.get('symbol')
                if symbol:
                    stocks.add(symbol)
            
            logger.info(f"✅ Fetched {len(stocks)} stocks from NSE API")
        else:
            logger.warning(f"NSE API returned status {response.status_code}")
    
    except Exception as e:
        logger.error(f"Error fetching from NSE API: {e}")
    
    return stocks


def get_nifty_indices_stocks() -> Set[str]:
    """
    Get stocks from multiple Nifty indices
    """
    all_stocks = set()
    
    indices = [
        'NIFTY%2050',
        'NIFTY%20NEXT%2050',
        'NIFTY%20MIDCAP%20100',
        'NIFTY%20SMALLCAP%20100',
        'NIFTY%20500'
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers, timeout=10)
    
    for index in indices:
        try:
            url = f"https://www.nseindia.com/api/equity-stockIndices?index={index}"
            response = session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for stock in data.get('data', []):
                    symbol = stock.get('symbol')
                    if symbol:
                        all_stocks.add(symbol)
                
                logger.info(f"✅ Fetched stocks from {index.replace('%20', ' ')}")
        except Exception as e:
            logger.error(f"Error fetching {index}: {e}")
    
    return all_stocks


def get_all_nse_stocks() -> Set[str]:
    """
    Get comprehensive list of NSE stocks from multiple sources
    """
    all_stocks = set()
    
    # Method 1: Try NSE API
    nse_stocks = get_nse_stocks_from_api()
    all_stocks.update(nse_stocks)
    
    # Method 2: Try Nifty indices
    if len(all_stocks) < 100:  # If NSE API failed
        indices_stocks = get_nifty_indices_stocks()
        all_stocks.update(indices_stocks)
    
    # Method 3: Fallback to hardcoded list if all fail
    if len(all_stocks) < 50:
        logger.warning("API fetch failed, using fallback stock list")
        from reddit_hype_analyzer import INDIAN_STOCKS
        all_stocks = INDIAN_STOCKS
    
    logger.info(f"✅ Total stocks loaded: {len(all_stocks)}")
    return all_stocks


def save_stocks_to_file(stocks: Set[str], filename: str = 'nse_stocks.json'):
    """Save stocks to JSON file for caching"""
    try:
        with open(filename, 'w') as f:
            json.dump(list(stocks), f, indent=2)
        logger.info(f"✅ Saved {len(stocks)} stocks to {filename}")
    except Exception as e:
        logger.error(f"Error saving stocks: {e}")


def load_stocks_from_file(filename: str = 'nse_stocks.json') -> Set[str]:
    """Load stocks from JSON file"""
    import os
    
    # Try multiple paths
    paths = [
        os.path.join('data', filename),
        os.path.join('..', 'data', filename),
        os.path.join(os.path.dirname(__file__), '..', 'data', filename),
        filename
    ]
    
    for path in paths:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    stocks = set(json.load(f))
                logger.info(f"✅ Loaded {len(stocks)} stocks from {path}")
                return stocks
        except Exception as e:
            continue
    
    logger.warning(f"File {filename} not found in any location")
    return set()


def get_stocks_with_cache(force_refresh: bool = False) -> Set[str]:
    """
    Get stocks with caching
    - Tries to load from cache file first
    - If not found or force_refresh=True, fetches from API
    """
    cache_file = 'nse_stocks.json'
    
    if not force_refresh:
        cached_stocks = load_stocks_from_file(cache_file)
        if cached_stocks:
            return cached_stocks
    
    # Fetch fresh data
    stocks = get_all_nse_stocks()
    
    # Save to cache
    save_stocks_to_file(stocks, cache_file)
    
    return stocks


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Fetching live NSE stocks...")
    stocks = get_stocks_with_cache(force_refresh=True)
    
    print(f"\n✅ Total stocks: {len(stocks)}")
    print(f"\nSample stocks: {list(stocks)[:20]}")
    
    # Save to file
    save_stocks_to_file(stocks)
    print(f"\n✅ Saved to nse_stocks.json")
