# 🔄 PumpWatch Application Flow Explained

## Overview
PumpWatch is a **real-time fraud detection system** that monitors social media (Telegram + Reddit) to detect pump & dump schemes in Indian stock markets.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
├─────────────────────────────────────────────────────────────┤
│  Telegram Channels  │  Reddit Subreddits  │  NSE Stock Data │
│  (pakkapredictions) │  (r/IndianStocks)   │  (yfinance)     │
└──────────┬──────────┴──────────┬───────────┴────────┬────────┘
           │                     │                     │
           ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   SCRAPING LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  SimpleTelegramScraper  │  RedditHypeAnalyzer  │  yfinance  │
│  - Fetches messages     │  - Scrapes posts     │  - Market  │
│  - Extracts tickers     │  - Detects hype      │    data    │
│  - Detects fraud words  │  - Sentiment         │            │
└──────────┬──────────────┴──────────┬──────────┴────────┬────┘
           │                         │                    │
           ▼                         ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                  INTELLIGENCE LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  IntelligenceEngine     │  RiskAnalyzer    │  MarketData    │
│  - Sentiment analysis   │  - Volume        │  - Reality     │
│  - Fraud triggers       │    anomaly       │    check       │
│  - Hinglish support     │  - Bot detection │  - Fundamentals│
│  - Hype intensity       │  - Risk scoring  │                │
└──────────┬──────────────┴──────────┬───────┴────────┬───────┘
           │                         │                 │
           ▼                         ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                     │
├─────────────────────────────────────────────────────────────┤
│  /fraud-alerts  │  /risk-score/{ticker}  │  /reddit-hype   │
│  /safety-dashboard  │  /anomaly-detection  │  /tickers     │
│  /reality-check/{ticker}  │  /bot-activity/{ticker}        │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND / USER                           │
│  - Web Dashboard  - Mobile App  - API Consumers             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Detailed Request Flow

### Example: User calls `/why-risky/YESBANK`

```
1. USER REQUEST
   ↓
   GET /why-risky/YESBANK

2. MAIN.PY (API Endpoint)
   ↓
   - Check if scraper has data
   - Filter messages containing "YESBANK"
   - If no messages → 404 error

3. INTELLIGENCE ENGINE
   ↓
   - Calculate hype intensity:
     • Count mentions (25 points)
     • Measure velocity (25 points)
     • Detect fraud triggers (25 points)
     • Analyze sentiment (25 points)
   - Total: 0-100 hype score

4. RISK ANALYZER
   ↓
   A. Volume Anomaly Detection:
      - Fetch 3 months of stock data (yfinance)
      - Calculate Z-score
      - Detect unusual volume spikes
   
   B. Bot Activity Detection:
      - Check rapid posting patterns
      - Detect copy-paste messages
      - Find multi-channel coordination
   
   C. Unified Risk Score:
      - Combine: hype + fraud + anomaly + bot
      - Calculate 0-100 risk score
      - Assign color: RED/AMBER/GREEN

5. FRAUD TRIGGER EXTRACTION
   ↓
   - Loop through all YESBANK messages
   - Extract fraud keywords:
     • "pakka", "upper circuit", "sure shot"
     • "guaranteed", "multibagger", etc.

6. GENERATE EXPLANATION
   ↓
   - Create natural language explanation
   - List all risk factors
   - Provide recommendation

7. RETURN JSON RESPONSE
   ↓
   {
     "ticker": "YESBANK",
     "explanation": "⚠️ YESBANK shows HIGH risk...",
     "risk_score": 75.5,
     "color_indicator": "RED"
   }
```

---

## 📱 Reddit Analysis Flow (Why It Takes Time)

When you call `/reddit-hype`, here's what happens:

```
1. RedditHypeAnalyzer.get_top_hyped()
   ↓
2. Load NSE stocks from nse_stocks.json
   ✅ Loaded 506 stocks from nse_stocks.json
   ↓
3. Loop through 6 subreddits:
   ├─ r/IndianStockMarket  (2-3 seconds)
   ├─ r/IndianStreetBets   (2-3 seconds)
   ├─ r/DalalStreetTalks   (2-3 seconds)
   ├─ r/IndianStocks       (2-3 seconds)
   ├─ r/IndiaTrade         (2-3 seconds)
   └─ r/IndianInvestor     (2-3 seconds)
   ↓
4. For each subreddit:
   - Fetch 100 hot posts (HTTP request)
   - Extract tickers from titles/text
   - Count hype keywords
   - Calculate engagement score
   ↓
5. Aggregate results:
   - Group by ticker
   - Calculate hype intensity
   - Sort by hype score
   ↓
6. Return top N stocks

TOTAL TIME: ~12 seconds (6 subreddits × 2 seconds each)
```

### Why It's Slow:
- **6 HTTP requests** to Reddit (one per subreddit)
- **No API key needed** (uses public JSON endpoints)
- **Network latency** (Reddit servers respond in 2-3 seconds)
- **Processing 600+ posts** (100 per subreddit)

---

## 🎯 Key Components Explained

### 1. SimpleTelegramScraper (`simple_telegram.py`)
**Purpose**: Fetch messages from Telegram channels

**Flow**:
```python
1. Connect to Telegram (Telethon)
2. For each channel:
   - Fetch last 50-100 messages
   - Extract tickers using regex: \b[A-Z]{2,10}\b
   - Filter to TARGET_STOCKS: YESBANK, TCS, RELIANCE, INFY
   - Count fraud keywords: "pakka", "upper circuit", etc.
   - Store in memory: self.messages = [...]
3. Return messages
```

**Why**: Telegram is where pump & dump operators coordinate

---

### 2. IntelligenceEngine (`intelligence_engine.py`)
**Purpose**: Analyze message content for fraud signals

**Key Functions**:

#### A. Sentiment Analysis
```python
calculate_sentiment(text)
→ Returns: -1.0 (bearish) to +1.0 (bullish)

Example:
"YESBANK rocket to moon" → +0.7 (bullish)
"YESBANK crash dump" → -0.8 (bearish)
```

#### B. Fraud Trigger Detection
```python
detect_fraud_triggers(text)
→ Returns: List of fraud keywords + weighted score

Example:
"YESBANK pakka upper circuit guaranteed"
→ Triggers: ["pakka", "upper circuit", "guaranteed"]
→ Score: 3 + 3 + 3 = 9 (HIGH RISK)
```

#### C. Hinglish Normalization
```python
normalize_hinglish(text)
→ Converts: "pakkaaa" → "pakka"
→ Converts: "zaroor" → "sure"

Why: Indian users mix Hindi + English
```

#### D. Hype Intensity (0-100)
```python
calculate_hype_intensity(ticker, messages)
→ Combines:
  - Mention count (0-25)
  - Velocity/acceleration (0-25)
  - Fraud trigger density (0-25)
  - Sentiment spike (0-25)
→ Total: 0-100

Example:
YESBANK: 50 mentions + 10 triggers + high sentiment
→ Hype Score: 85/100 (CRITICAL)
```

---

### 3. RiskAnalyzer (`risk_analyzer.py`)
**Purpose**: Detect market manipulation patterns

#### A. Volume Anomaly Detection
```python
detect_volume_anomaly(ticker)
→ Uses Z-score statistics

Steps:
1. Fetch 3 months of volume data (yfinance)
2. Calculate mean & std deviation
3. Z-score = (today_volume - mean) / std
4. If Z > 3 → ANOMALY (99.7% confidence)

Example:
YESBANK avg volume: 1M shares
Today's volume: 5M shares
Z-score: 4.2 → ANOMALY DETECTED
```

#### B. Bot Activity Detection
```python
detect_bot_activity(ticker, messages)
→ Looks for:
  - Rapid posting (3+ posts in 5 minutes)
  - Copy-paste messages (70% text similarity)
  - Multi-channel coordination (3+ channels)

Example:
YESBANK: 5 identical messages in 3 channels within 2 minutes
→ Bot confidence: 90% (HIGH)
```

#### C. Unified Risk Score
```python
calculate_unified_risk_score(...)
→ Combines 4 components (each 0-25):
  - Hype intensity
  - Fraud signals
  - Volume anomaly
  - Bot activity
→ Total: 0-100

Risk Levels:
0-30: GREEN (Low risk)
30-50: AMBER (Medium risk)
50-75: RED (High risk)
75-100: RED (Critical risk)
```

---

### 4. MarketDataChecker (`market_data.py`)
**Purpose**: Reality check - compare social hype vs fundamentals

```python
reality_check(ticker, social_hype, fraud_score)
→ Fetches from yfinance:
  - Market cap
  - Trading volume
  - Price change
  - Company info

→ Red flags:
  ✗ High hype (>60) + No official news
  ✗ Low liquidity (<100K volume)
  ✗ Small market cap (<500 crore)
  ✗ High fraud score (>5)

Example:
YESBANK:
- Social hype: 85/100
- Market cap: 200 crore (small)
- Volume: 50K (low liquidity)
- Fraud score: 9
→ VERDICT: RED - High manipulation risk
```

---

## 🔍 Why Reddit Analysis Happens

When you call `/reddit-hype`:

1. **Purpose**: Cross-verify Telegram signals with Reddit discussions
2. **Why**: Victims often report scams on Reddit after losing money
3. **What it does**:
   - Scans 6 Indian stock subreddits
   - Finds most discussed stocks
   - Detects warning posts ("scam", "fraud", "lost money")
   - Provides community sentiment

**Example Output**:
```json
{
  "top_hyped_stocks": [
    {
      "ticker": "YESBANK",
      "mentions": 45,
      "hype_intensity": 78.5,
      "avg_sentiment": -0.6,  // Negative = warnings
      "posts": [...]
    }
  ]
}
```

---

## 🎯 Complete User Journey

### Scenario: Detecting YESBANK Pump & Dump

```
1. OPERATOR POSTS ON TELEGRAM
   "YESBANK pakka upper circuit guaranteed 100%"
   ↓
2. YOUR API FETCHES MESSAGE
   - SimpleTelegramScraper.fetch_messages()
   - Extracts: ticker=YESBANK, fraud_score=5
   ↓
3. USER CALLS /why-risky/YESBANK
   ↓
4. INTELLIGENCE ENGINE ANALYZES
   - 50 mentions in last hour (HIGH)
   - Fraud triggers: pakka, upper circuit, guaranteed
   - Sentiment: +0.8 (extremely bullish)
   - Hype score: 85/100
   ↓
5. RISK ANALYZER CHECKS
   - Volume anomaly: Z-score 4.2 (SPIKE)
   - Bot activity: 90% confidence (BOTS)
   ↓
6. MARKET DATA CHECKER
   - Market cap: 200 crore (SMALL)
   - Liquidity: Low (RISKY)
   - No official news (RED FLAG)
   ↓
7. UNIFIED RISK SCORE
   - Hype: 21/25
   - Fraud: 22/25
   - Anomaly: 21/25
   - Bot: 22/25
   - TOTAL: 86/100 (CRITICAL)
   ↓
8. GENERATE EXPLANATION
   "⚠️ YESBANK shows CRITICAL risk (86/100).
   High social media hype | Detected 5 fraud keywords |
   Unusual volume spike: 320% above average (4.2σ) |
   Coordinated bot activity detected.
   Recommendation: AVOID - High manipulation risk."
   ↓
9. RETURN TO USER
   {
     "ticker": "YESBANK",
     "risk_score": 86,
     "color_indicator": "RED",
     "explanation": "..."
   }
```

---

## ⚡ Performance Optimization

### Current Bottlenecks:
1. **Reddit scraping**: 12 seconds (6 subreddits)
2. **yfinance API**: 2-3 seconds per ticker
3. **No caching**: Fetches data every time

### Why It's Acceptable:
- **Hackathon demo**: Speed not critical
- **Real-time data**: Fresh data more important
- **Low traffic**: Single user testing

### Production Improvements:
```python
# Add caching
@lru_cache(maxsize=100, ttl=300)  # 5 min cache
def get_risk_score(ticker):
    ...

# Background jobs
@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(poll_telegram_every_30s())
    asyncio.create_task(refresh_reddit_every_5min())

# Database storage
# Replace in-memory lists with PostgreSQL/MongoDB
```

---

## 📊 Data Flow Summary

```
Telegram Messages → SimpleTelegramScraper → In-Memory Storage
                                                    ↓
Reddit Posts → RedditHypeAnalyzer → Hype Scores
                                                    ↓
Stock Data → yfinance → Market Fundamentals
                                                    ↓
                    IntelligenceEngine + RiskAnalyzer
                                                    ↓
                         Unified Risk Assessment
                                                    ↓
                         FastAPI JSON Response
                                                    ↓
                              User/Frontend
```

---

## 🎓 Key Takeaways

1. **Multi-source intelligence**: Telegram + Reddit + Market data
2. **Layered analysis**: Scraping → Intelligence → Risk → API
3. **Real-time detection**: Fetches latest data on demand
4. **Hinglish support**: Understands Indian market language
5. **Statistical rigor**: Z-scores, sentiment analysis, bot detection
6. **Actionable output**: Clear RED/AMBER/GREEN indicators

**Bottom Line**: Your system detects pump & dump schemes by combining social media signals, market data, and AI analysis to protect retail investors! 🛡️
