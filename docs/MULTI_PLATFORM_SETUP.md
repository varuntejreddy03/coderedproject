# 🔧 Multi-Platform Setup Guide

## 🎯 Why Multi-Platform Monitoring?

**Telegram** = Where scams happen  
**Reddit** = Where victims report scams  
**Twitter/X** = Where SEBI/regulators post alerts

Cross-referencing all 3 gives complete fraud detection.

---

## 📱 1. Telegram Setup (Already Done)

Get credentials: https://my.telegram.org/apps

---

## 🔴 2. Reddit Setup (NO API KEY NEEDED!)

### ✅ Using Public JSON API (Recommended)

**Why no API?**
- ✅ No registration needed
- ✅ No rate limits for basic usage
- ✅ Works immediately
- ✅ Uses Reddit's public JSON endpoints
- ✅ Perfect for hackathons

**Setup:**
```bash
pip install requests beautifulsoup4
```

That's it! No configuration needed.

### How It Works
Reddit provides public JSON endpoints:
```
https://www.reddit.com/r/IndianStockMarket/new.json
```

No authentication required for reading public posts!

### Alternative: Reddit API (Not Recommended)

If you still want official API (not needed):
1. Go to https://www.reddit.com/prefs/apps
2. Create "script" app
3. Get client_id and secret

**But public API is faster and easier!**

---

## 🐦 3. Twitter/X Setup (NO API KEY NEEDED!)

### ✅ Using snscrape (Recommended for Hackathons)

**Why snscrape?**
- ✅ No API key required
- ✅ No rate limits
- ✅ Works immediately
- ✅ Scrapes public tweets
- ✅ Perfect for hackathons

**Setup:**
```bash
pip install snscrape
```

That's it! No configuration needed.

### Monitored Queries
- "stock tips scam telegram lang:en OR lang:hi"
- "pump and dump India stocks"
- "fake stock tips India"
- "SEBI fraud alert"
- "telegram stock scam India"

### Alternative: Twitter API (Not Recommended for Hackathons)

If you still want to use official API:
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Apply for developer account (takes 1-2 days)
3. Get bearer token
4. Add to .env: `TWITTER_BEARER_TOKEN=your_token`

**But snscrape is faster and easier!**

---

## 🚀 New API Endpoints

### Reddit Posts
```bash
GET /reddit-posts?limit=50
```
Returns posts from Indian stock subreddits discussing scams.

### Twitter Alerts
```bash
GET /twitter-alerts?limit=50
```
Returns tweets about stock market fraud and SEBI alerts.

### Combined Intelligence
```bash
# Get Telegram fraud alerts
GET /fraud-alerts

# Cross-reference with Reddit reports
GET /reddit-posts

# Check Twitter for SEBI warnings
GET /twitter-alerts
```

---

## 🎯 Usage Strategy

### 1. Telegram → Detect Scams
Monitor suspicious channels for pump signals

### 2. Reddit → Validate Scams
Check if users are reporting the same tickers/channels

### 3. Twitter → Official Alerts
Cross-check with SEBI/regulatory warnings

### Example Workflow
```python
# 1. Detect pump on Telegram
fraud_alerts = requests.get('/fraud-alerts').json()
suspicious_ticker = fraud_alerts['top_suspicious_tickers'][0]

# 2. Check Reddit for victim reports
reddit_posts = requests.get('/reddit-posts').json()
# Search for ticker mentions

# 3. Check Twitter for SEBI alerts
twitter_alerts = requests.get('/twitter-alerts').json()
# Verify if officially flagged
```

---

## ⚠️ Rate Limits

- **Telegram**: No official limit (use 30s polling)
- **Reddit**: ~60 requests/minute (public JSON API)
- **Twitter (snscrape)**: ❌ Currently blocked by X/Twitter

**Note:** Twitter/X frequently blocks scrapers. Reddit works perfectly!

---

## 🔒 Security Notes

- Never commit `.env` file
- Add `.env` to `.gitignore`
- Rotate tokens if exposed
- Use read-only API access
