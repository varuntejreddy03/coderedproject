# 📊 API Response Examples

## How Data Flows & What You Get

### 🔄 Data Flow Architecture

```
┌─────────────────┐
│  Telegram       │──┐
│  Channels       │  │
└─────────────────┘  │
                     │
┌─────────────────┐  │    ┌──────────────┐    ┌─────────────┐
│  Reddit         │──┼───▶│  PumpWatch   │───▶│  Your App   │
│  Subreddits     │  │    │  Backend     │    │  Frontend   │
└─────────────────┘  │    └──────────────┘    └─────────────┘
                     │
┌─────────────────┐  │
│  Twitter/X      │──┘
│  (snscrape)     │
└─────────────────┘

Every 30 seconds: Fetch → Process → Store → Serve via API
```

---

## 🎯 Sample API Responses

### 1️⃣ GET /health
**What it does:** Check if system is running

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "messages_count": 847,
  "active_channels": 5
}
```

---

### 2️⃣ GET /messages?limit=3
**What it does:** Get latest messages from Telegram channels

**Request:**
```bash
curl http://localhost:8000/messages?limit=3
```

**Response:**
```json
[
  {
    "id": 12345,
    "channel": "stocktipsindia",
    "text": "🚀 YESBANK target 25 guaranteed! Upper circuit confirmed. Book profit at 30. BTST call.",
    "normalized_text": "yesbank target 25 guaranteed upper circuit confirmed book profit at 30 btst call",
    "date": "2024-01-15T10:30:00",
    "tickers": ["YESBANK"],
    "fraud_signals": ["guaranteed", "upper circuit", "confirmed", "book profit", "btst"],
    "risk_score": 5
  },
  {
    "id": 12346,
    "channel": "intradaycalls",
    "text": "Buy RELIANCE at 2450, target 2500, stop loss 2430",
    "normalized_text": "buy reliance at 2450 target 2500 stop loss 2430",
    "date": "2024-01-15T10:32:00",
    "tickers": ["RELIANCE"],
    "fraud_signals": ["target"],
    "risk_score": 1
  },
  {
    "id": 12347,
    "channel": "pennystockalerts",
    "text": "Multibagger alert! SUZLON can give 100% returns. Don't miss this jackpot opportunity!",
    "normalized_text": "multibagger alert suzlon can give 100 returns don t miss this jackpot opportunity",
    "date": "2024-01-15T10:35:00",
    "tickers": ["SUZLON"],
    "fraud_signals": ["multibagger", "100%", "don't miss", "jackpot"],
    "risk_score": 4
  }
]
```

---

### 3️⃣ GET /ticker/YESBANK
**What it does:** Get stats for specific stock ticker

**Request:**
```bash
curl http://localhost:8000/ticker/YESBANK
```

**Response:**
```json
{
  "symbol": "YESBANK",
  "mentions": 23,
  "recent_messages": [
    {
      "id": 12345,
      "channel": "stocktipsindia",
      "text": "🚀 YESBANK target 25 guaranteed!",
      "normalized_text": "yesbank target 25 guaranteed",
      "date": "2024-01-15T10:30:00",
      "tickers": ["YESBANK"],
      "fraud_signals": ["guaranteed", "target"],
      "risk_score": 2
    }
    // ... 9 more recent messages
  ]
}
```

---

### 4️⃣ GET /tickers
**What it does:** Get all tickers sorted by mention count (pump detection)

**Request:**
```bash
curl http://localhost:8000/tickers
```

**Response:**
```json
{
  "YESBANK": 23,
  "SUZLON": 18,
  "RELIANCE": 15,
  "TATAMOTORS": 12,
  "INFY": 8,
  "TCS": 5
}
```

**Use case:** If YESBANK suddenly has 23 mentions vs others = potential pump!

---

### 5️⃣ GET /fraud-alerts?min_risk=3
**What it does:** Get high-risk pump & dump messages

**Request:**
```bash
curl http://localhost:8000/fraud-alerts?min_risk=3
```

**Response:**
```json
{
  "high_risk_messages": [
    {
      "id": 12345,
      "channel": "stocktipsindia",
      "text": "🚀 YESBANK target 25 guaranteed! Upper circuit confirmed. Book profit at 30. BTST call.",
      "normalized_text": "yesbank target 25 guaranteed upper circuit confirmed book profit at 30 btst call",
      "date": "2024-01-15T10:30:00",
      "tickers": ["YESBANK"],
      "fraud_signals": ["guaranteed", "upper circuit", "confirmed", "book profit", "btst"],
      "risk_score": 5
    },
    {
      "id": 12347,
      "channel": "pennystockalerts",
      "text": "Multibagger alert! SUZLON can give 100% returns. Don't miss this jackpot opportunity!",
      "normalized_text": "multibagger alert suzlon can give 100 returns don t miss this jackpot opportunity",
      "date": "2024-01-15T10:35:00",
      "tickers": ["SUZLON"],
      "fraud_signals": ["multibagger", "100%", "don't miss", "jackpot"],
      "risk_score": 4
    }
  ],
  "total_alerts": 47,
  "top_suspicious_tickers": {
    "YESBANK": 12,
    "SUZLON": 8,
    "TATAMOTORS": 5
  }
}
```

---

### 6️⃣ GET /discover-channels?query=penny+stock
**What it does:** Auto-discover suspicious channels

**Request:**
```bash
curl "http://localhost:8000/discover-channels?query=penny+stock+india"
```

**Response:**
```json
{
  "query": "penny stock india",
  "found_channels": [
    {
      "username": "pennystockalerts",
      "title": "Penny Stock Alerts India",
      "participants": 15420
    },
    {
      "username": "multibaggerstocks",
      "title": "Multibagger Stocks 2024",
      "participants": 8930
    },
    {
      "username": "smallcapindia",
      "title": "Small Cap India",
      "participants": 5670
    }
  ],
  "count": 3
}
```

---

### 7️⃣ GET /reddit-posts?limit=2
**What it does:** Get scam reports from Reddit

**Request:**
```bash
curl http://localhost:8000/reddit-posts?limit=2
```

**Response:**
```json
{
  "posts": [
    {
      "id": "abc123",
      "channel": "r/IndianStockMarket",
      "text": "Warning: Telegram channel @stocktipsindia is pumping YESBANK. Lost 50k following their tips.",
      "date": "2024-01-15T09:20:00",
      "url": "https://reddit.com/r/IndianStockMarket/comments/abc123"
    },
    {
      "id": "def456",
      "channel": "r/IndianStreetBets",
      "text": "PSA: Avoid penny stock telegram groups. They coordinate pump and dump.",
      "date": "2024-01-15T08:45:00",
      "url": "https://reddit.com/r/IndianStreetBets/comments/def456"
    }
  ],
  "count": 2
}
```

---

### 8️⃣ GET /twitter-alerts?limit=2
**What it does:** Get SEBI alerts and scam warnings from Twitter

**Request:**
```bash
curl http://localhost:8000/twitter-alerts?limit=2
```

**Response:**
```json
{
  "tweets": [
    {
      "id": 1234567890,
      "channel": "twitter",
      "text": "SEBI warns against unregistered investment advisors operating via Telegram. Report suspicious channels to SEBI.",
      "date": "2024-01-15T11:00:00",
      "username": "SEBI_India",
      "url": "https://twitter.com/SEBI_India/status/1234567890"
    },
    {
      "id": 9876543210,
      "channel": "twitter",
      "text": "Beware of telegram stock tips scam. They pump penny stocks and retail investors lose money. #StockMarketScam",
      "date": "2024-01-15T10:15:00",
      "username": "MoneyControlNews",
      "url": "https://twitter.com/MoneyControlNews/status/9876543210"
    }
  ],
  "count": 2
}
```

---

## 🎯 Real-World Usage Example

### Scenario: Detect YESBANK Pump & Dump

```bash
# Step 1: Check fraud alerts
curl http://localhost:8000/fraud-alerts?min_risk=3

# Output: YESBANK has 12 high-risk mentions with keywords:
# "guaranteed", "upper circuit", "100% returns"

# Step 2: Check Reddit for victim reports
curl http://localhost:8000/reddit-posts?limit=50

# Output: Found 3 posts warning about YESBANK pump on Telegram

# Step 3: Check Twitter for SEBI alerts
curl http://localhost:8000/twitter-alerts?limit=50

# Output: SEBI tweeted warning about unregistered advisors

# Conclusion: YESBANK is being pumped! 🚨
```

---

## 🚀 Quick Test

Run the backend:
```bash
python main.py
```

Open browser:
```
http://localhost:8000/docs
```

You'll see interactive Swagger UI to test all endpoints!

---

## 📊 Data Update Frequency

- **Telegram**: Every 30 seconds (background polling)
- **Reddit**: On-demand (when you call the endpoint)
- **Twitter**: On-demand (when you call the endpoint)

---

## 💡 Pro Tips

1. **Monitor /fraud-alerts every minute** for real-time pump detection
2. **Cross-reference** Telegram alerts with Reddit/Twitter
3. **Track ticker velocity** - sudden spike in mentions = pump signal
4. **Risk score >= 3** = high probability of scam
5. **Compare with official channels** (NSE, BSE) for validation
