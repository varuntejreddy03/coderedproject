# 🔄 PumpWatch - Complete Project Flow

## 🏗️ Data Architecture

### Two-Tier System

```
🔴 RUMOR SOURCES (Untrusted - Monitored)
├─ Telegram (pump groups)
└─ Reddit (speculation)
         ↓
    DETECTION
         ↓
✅ VERIFICATION SOURCES (Trusted - Validation)
├─ yfinance (Yahoo Finance)
├─ NSE/BSE filings
└─ Market metrics
         ↓
   RISK ASSESSMENT
```

## 📋 Table of Contents
1. [System Architecture](#system-architecture)
2. [Startup Flow](#startup-flow)
3. [Data Collection Flow](#data-collection-flow)
4. [Analysis Flow](#analysis-flow)
5. [API Request Flow](#api-request-flow)
6. [Component Details](#component-details)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ENTRY POINT                              │
│                         main.py                                  │
│                    FastAPI Application                           │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│   SCRAPERS   │          │     CORE     │
│   Package    │          │   Package    │
└──────────────┘          └──────────────┘
        │                         │
        ├─ simple_telegram.py     ├─ intelligence_engine.py
        ├─ reddit_scraper.py      ├─ risk_analyzer.py
        ├─ reddit_hype_analyzer   ├─ market_data.py
        └─ fetch_nse_stocks.py    ├─ legitimacy_validator.py
                                  └─ comprehensive_analyzer.py
```

---

## 🚀 Startup Flow

### Step 1: Application Initialization
```python
# main.py - Line 1-30
1. Load environment variables (.env file)
   - API_ID (Telegram)
   - API_HASH (Telegram)
   - CHANNELS (Telegram channels to monitor)

2. Initialize global instances:
   - scraper = None
   - reddit_scraper = None
   - risk_analyzer = RiskAnalyzer()
   - startup_time = None
```

### Step 2: Lifespan Context Manager
```python
# main.py - Line 32-60
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # STARTUP
    1. Set startup_time = datetime.now()
    
    2. Telegram Setup:
       - Create SimpleTelegramScraper instance
       - Connect to Telegram (await scraper.connect())
       - Fetch initial 50 messages (await scraper.fetch_messages(50))
       - Load 506 NSE stocks from data/nse_stocks.json
       - Extract tickers from messages
       - Store in memory: scraper.messages = [...]
    
    3. Reddit Setup:
       - Initialize RedditScraper instance
       - Ready to scrape on-demand
    
    yield  # Application runs
    
    # SHUTDOWN
    4. Disconnect Telegram client
    5. Cleanup resources
```

---

## 📡 Data Collection Flow

### Telegram Scraping (scrapers/simple_telegram.py)

```
1. LOAD NSE STOCKS (Line 11-28)
   ├─ Try: data/nse_stocks.json
   ├─ Try: ../data/nse_stocks.json
   ├─ Try: scrapers/../data/nse_stocks.json
   └─ Fallback: 7 common stocks
   
   Result: TARGET_STOCKS = Set of 506 NSE stocks

2. CONNECT TO TELEGRAM (Line 54-57)
   ├─ Create TelegramClient with API credentials
   ├─ Start session (creates/reuses pumpwatch_session.session)
   └─ Ready to fetch messages

3. FETCH MESSAGES (Line 59-85)
   For each channel in CHANNELS:
   ├─ Get channel entity
   ├─ Fetch last N messages
   └─ For each message:
       ├─ Extract text
       ├─ Extract tickers (regex: \b[A-Z]{2,15}\b)
       ├─ Filter to NSE stocks only
       ├─ Count fraud keywords
       └─ Store: {id, channel, text, date, tickers, fraud_score}

4. STORE IN MEMORY
   self.messages = [
       {
           'id': 12345,
           'channel': 'pakkapredictions890',
           'text': 'YESBANK pakka upper circuit',
           'date': '2026-02-21T20:00:00',
           'tickers': ['YESBANK'],
           'fraud_score': 3
       },
       ...
   ]
```

### Reddit Scraping (scrapers/reddit_hype_analyzer.py)

```
1. LOAD NSE STOCKS (Line 11-17)
   ├─ Import from fetch_nse_stocks.py
   └─ Fallback to hardcoded 90+ stocks

2. ANALYZE REDDIT (Line 175-230)
   For each subreddit in [IndianStockMarket, IndianStreetBets, ...]:
   ├─ Fetch 100 hot posts (Reddit JSON API)
   ├─ Extract title + selftext
   ├─ Find tickers using regex
   ├─ Count hype keywords (moon, rocket, guaranteed, etc.)
   └─ Calculate engagement (upvotes + comments)

3. AGGREGATE BY TICKER
   ticker_data = {
       'YESBANK': {
           'mentions': 45,
           'total_hype_score': 120,
           'total_upvotes': 500,
           'total_comments': 200,
           'posts': [...]
       }
   }

4. CALCULATE HYPE INTENSITY
   hype_intensity = (mentions × 10) + (avg_hype × 5) + (engagement / 10)
```

---

## 🧠 Analysis Flow

### Intelligence Engine (core/intelligence_engine.py)

```
1. NORMALIZE HINGLISH (Line 70-82)
   Input: "pakkaaa zaroor bilkul"
   ├─ Remove repeated chars: "pakka zaroor bilkul"
   ├─ Map to English: "sure sure absolutely"
   └─ Output: Normalized text

2. CALCULATE SENTIMENT (Line 84-104)
   Input: "YESBANK rocket to moon"
   ├─ Check positive keywords: rocket (+0.8), moon (+0.7)
   ├─ Check negative keywords: none
   ├─ Average: (0.8 + 0.7) / 2 = 0.75
   └─ Output: +0.75 (Bullish)

3. DETECT FRAUD TRIGGERS (Line 106-120)
   Input: "pakka upper circuit guaranteed 100%"
   ├─ Match: "pakka" (weight: 2)
   ├─ Match: "upper circuit" (weight: 3)
   ├─ Match: "guaranteed" (weight: 3)
   ├─ Match: "100%" (weight: 3)
   └─ Output: {triggers: [...], total_score: 11}

4. CALCULATE HYPE INTENSITY (Line 160-210)
   For ticker + messages:
   ├─ Mention score (0-25): count × 1
   ├─ Velocity score (0-25): mentions in last hour
   ├─ Trigger score (0-25): fraud keywords density
   ├─ Sentiment score (0-25): extreme sentiment
   └─ Total: 0-100 hype score
```

### Risk Analyzer (core/risk_analyzer.py)

```
1. VOLUME ANOMALY DETECTION (Line 17-56)
   Input: Ticker
   ├─ Fetch 3 months volume data (yfinance)
   ├─ Calculate mean & std deviation
   ├─ Z-score = (today_volume - mean) / std
   ├─ If Z > 3: ANOMALY (99.7% confidence)
   └─ Output: {anomaly_detected, z_score, volume_spike_%}

2. BOT ACTIVITY DETECTION (Line 58-115)
   Input: Ticker + Messages
   ├─ Check rapid posting (< 5 min intervals)
   ├─ Check copy-paste (70% text similarity)
   ├─ Check multi-channel coordination
   ├─ Calculate confidence (0-100)
   └─ Output: {bot_detected, confidence, indicators}

3. UNIFIED RISK SCORE (Line 117-160)
   Input: Hype + Fraud + Anomaly + Bot
   ├─ Normalize each to 0-25 scale
   ├─ Sum all components
   ├─ Adjust by legitimacy (×1.2 if rumor, ×0.8 if legit)
   └─ Output: {risk_score: 0-100, level, color}
```

### Market Data Checker (core/market_data.py)

```
1. GET STOCK FUNDAMENTALS (Line 23-60)
   Input: Ticker
   ├─ Fetch from yfinance (ticker.NS)
   ├─ Get: market_cap, volume, price_change
   ├─ Check: has_official_news, is_liquid
   └─ Output: Fundamental data

2. REALITY CHECK (Line 62-130)
   Input: Ticker + Social Hype + Fraud Score
   
   Calculate Risk Factors:
   ├─ High hype + No news → +30 risk
   ├─ Low liquidity → +20 risk
   ├─ Small market cap → +20 risk
   ├─ High fraud score → +30 risk
   
   Determine Safety:
   ├─ Risk ≥ 70: RED (Critical)
   ├─ Risk ≥ 50: AMBER (High)
   ├─ Risk ≥ 30: AMBER (Medium)
   └─ Risk < 30: GREEN (Low)
```

### Legitimacy Validator (core/legitimacy_validator.py)

```
1. GET NSE FILINGS (Line 23-40)
   Input: Ticker
   ├─ Fetch yfinance news
   ├─ Check dividend/split announcements
   ├─ Count official sources (BSE/NSE)
   └─ Output: {has_filings, filing_count, news}

2. VALIDATE SOCIAL VS OFFICIAL (Line 80-140)
   Input: Ticker + Social Hype + Sentiment
   
   Start: legitimacy_score = 50
   
   Red Flags (subtract):
   ├─ High hype + No filings → -30
   ├─ Volume spike + No action → -25
   ├─ No official sources → -15
   
   Green Flags (add):
   ├─ Official filings present → +20
   ├─ Corporate action → +15
   ├─ Official coverage → +15
   
   Verdict:
   ├─ Score ≥ 70: LEGITIMATE
   ├─ Score 40-69: UNCERTAIN
   └─ Score < 40: LIKELY_RUMOR
```

### Comprehensive Analyzer (core/comprehensive_analyzer.py)

```
1. ANALYZE TICKER (Line 30-70)
   Input: Ticker + Telegram Messages + Reddit Posts
   
   Step 1: Get Market Data
   ├─ Price, volume, Z-score
   └─ Volume chart (30 days)
   
   Step 2: Analyze Social Activity
   ├─ Telegram: mentions, sentiment, keywords
   ├─ Reddit: mentions, sentiment, keywords
   └─ X/Twitter: placeholder (needs paid API)
   
   Step 3: Calculate Risk Breakdown
   ├─ Social Hype Score (0-100)
   ├─ Volume Anomaly (0-100)
   ├─ Bot Coordination (0-100)
   ├─ Sentiment Spike (0-100)
   └─ Lack of Filings (0-100)
   
   Step 4: Validate Legitimacy
   ├─ Check NSE filings
   ├─ Compare social vs official
   └─ Generate verdict
   
   Step 5: Calculate Unified Risk
   ├─ Weight all components
   ├─ Adjust by legitimacy
   └─ Assign color (RED/AMBER/GREEN)
   
   Step 6: Generate AI Analysis
   └─ Natural language explanation
```

---

## 🌐 API Request Flow

### Example: GET /ticker-analysis/YESBANK

```
1. USER REQUEST
   GET http://localhost:8080/ticker-analysis/YESBANK

2. MAIN.PY - comprehensive_ticker_analysis() (Line 320-350)
   ├─ Check if scraper exists
   ├─ Filter messages: ticker in m['tickers']
   ├─ If no messages → 404 error
   └─ Get Reddit data (optional)

3. COMPREHENSIVE ANALYZER
   analyzer.analyze_ticker(YESBANK, messages, reddit_posts)
   
   ├─ Market Data (yfinance)
   │   ├─ Price: ₹42.30
   │   ├─ Change: +11.2%
   │   ├─ Volume: 4.2M
   │   ├─ Avg Volume: 900K
   │   └─ Z-Score: 3.8
   
   ├─ Social Activity
   │   ├─ Telegram: 342 mentions, Bullish
   │   ├─ Reddit: 87 mentions, Bullish
   │   └─ Keywords: ["Upper Circuit Pakka", "Target 5x"]
   
   ├─ Risk Breakdown
   │   ├─ Social Hype: 85%
   │   ├─ Volume Anomaly: 74%
   │   ├─ Bot Coordination: 68%
   │   ├─ Sentiment Spike: 80%
   │   └─ Lack of Filings: 90%
   
   ├─ Legitimacy Check
   │   ├─ NSE Filings: 0 found
   │   ├─ Legitimacy Score: 25/100
   │   ├─ Verdict: LIKELY_RUMOR
   │   └─ Red Flags: 3
   
   ├─ Unified Risk Score
   │   ├─ Calculate: (85×0.25 + 74×0.20 + 68×0.20 + 80×0.15 + 90×0.20)
   │   ├─ Adjust: ×1.2 (because LIKELY_RUMOR)
   │   └─ Result: 82/100 (HIGH RISK, RED)
   
   └─ AI Analysis
       "Coordinated Telegram activity detected across 3 channels.
        Volume spike 4.3x above 5-day average.
        No NSE filings found in last 90 days.
        Bot-like posting patterns identified with 68% confidence."

4. RETURN JSON RESPONSE
   {
     "ticker": "YESBANK",
     "risk_assessment": {
       "score": 82,
       "level": "HIGH RISK",
       "color": "RED"
     },
     "market_data": {...},
     "social_activity": {...},
     "ai_analysis": "...",
     "risk_breakdown": {...},
     "legitimacy": {...}
   }
```

---

## 📊 Component Details

### 1. SimpleTelegramScraper
**File**: `scrapers/simple_telegram.py`
**Purpose**: Fetch messages from Telegram channels

**Key Methods**:
- `load_nse_stocks()`: Load 506 NSE stocks from JSON
- `extract_tickers(text)`: Find stock symbols in text
- `detect_fraud(text)`: Count fraud keywords
- `fetch_messages(limit)`: Get messages from channels
- `get_all_tickers()`: Return ticker mention counts

**Data Flow**:
```
Telegram API → fetch_messages() → extract_tickers() → self.messages[]
```

### 2. IntelligenceEngine
**File**: `core/intelligence_engine.py`
**Purpose**: Analyze message content for fraud signals

**Key Methods**:
- `normalize_hinglish(text)`: Convert Hinglish to English
- `calculate_sentiment(text)`: -1 to +1 sentiment score
- `detect_fraud_triggers(text)`: Find fraud keywords
- `calculate_hype_intensity(ticker, messages)`: 0-100 hype score
- `track_ticker_mention(ticker, timestamp)`: Track velocity

**Data Flow**:
```
Messages → normalize → sentiment + fraud → hype_intensity → Risk Score
```

### 3. RiskAnalyzer
**File**: `core/risk_analyzer.py`
**Purpose**: Detect market manipulation patterns

**Key Methods**:
- `detect_volume_anomaly(ticker)`: Z-score analysis
- `detect_bot_activity(ticker, messages)`: Bot detection
- `calculate_unified_risk_score()`: Combine all signals
- `generate_risk_explanation()`: Natural language output

**Data Flow**:
```
yfinance data + Messages → anomaly + bot → unified_risk → Explanation
```

### 4. MarketDataChecker
**File**: `core/market_data.py`
**Purpose**: Validate against official market data

**Key Methods**:
- `get_stock_fundamentals(ticker)`: Fetch NSE data
- `reality_check(ticker, hype, fraud)`: Compare social vs official

**Data Flow**:
```
yfinance API → fundamentals → reality_check → RED/AMBER/GREEN
```

### 5. LegitimacyValidator
**File**: `core/legitimacy_validator.py`
**Purpose**: Validate rumors against NSE filings

**Key Methods**:
- `get_nse_filings(ticker)`: Check official announcements
- `validate_social_vs_official()`: Compare claims vs reality

**Data Flow**:
```
Social Claims → NSE Filings → Red/Green Flags → LEGITIMATE/RUMOR
```

### 6. ComprehensiveTickerAnalyzer
**File**: `core/comprehensive_analyzer.py`
**Purpose**: Complete analysis for UI

**Key Methods**:
- `analyze_ticker()`: Main analysis function
- `_get_market_data()`: Fetch market data
- `_analyze_social_activity()`: Analyze Telegram + Reddit
- `_calculate_risk_breakdown()`: 5-component breakdown
- `_calculate_unified_risk()`: Final risk score
- `_generate_ai_analysis()`: Natural language summary

**Data Flow**:
```
All Components → Comprehensive Analysis → UI-Ready JSON
```

---

## 🔄 Complete Request-Response Cycle

```
1. USER SENDS MESSAGE TO TELEGRAM
   "YESBANK pakka upper circuit guaranteed 100%"

2. API STARTUP
   ├─ Load .env configuration
   ├─ Connect to Telegram
   ├─ Fetch last 50 messages
   ├─ Extract tickers: ['YESBANK']
   └─ Store in memory

3. USER CALLS API
   GET /ticker-analysis/YESBANK

4. DATA COLLECTION
   ├─ Filter messages with YESBANK
   ├─ Scrape Reddit (optional)
   └─ Fetch market data (yfinance)

5. ANALYSIS PIPELINE
   ├─ Intelligence Engine
   │   ├─ Normalize Hinglish
   │   ├─ Calculate sentiment
   │   ├─ Detect fraud triggers
   │   └─ Calculate hype intensity
   │
   ├─ Risk Analyzer
   │   ├─ Detect volume anomaly
   │   ├─ Detect bot activity
   │   └─ Calculate unified risk
   │
   ├─ Market Data Checker
   │   ├─ Get fundamentals
   │   └─ Reality check
   │
   └─ Legitimacy Validator
       ├─ Check NSE filings
       └─ Validate social vs official

6. COMPREHENSIVE ANALYSIS
   ├─ Combine all signals
   ├─ Calculate risk breakdown
   ├─ Generate AI explanation
   └─ Assign color indicator

7. RETURN JSON RESPONSE
   {
     "risk_assessment": {...},
     "market_data": {...},
     "social_activity": {...},
     "ai_analysis": "...",
     "risk_breakdown": {...},
     "legitimacy": {...}
   }

8. FRONTEND DISPLAYS
   ├─ Risk gauge (82/100)
   ├─ Market data chart
   ├─ Social activity cards
   ├─ AI analysis text
   └─ Risk breakdown bars
```

---

## 📈 Data Storage

### In-Memory Storage
```python
scraper.messages = [
    {
        'id': 12345,
        'channel': 'pakkapredictions890',
        'text': 'YESBANK pakka upper circuit',
        'date': '2026-02-21T20:00:00',
        'tickers': ['YESBANK'],
        'fraud_score': 3
    },
    ...
]
```

### File Storage
```
data/nse_stocks.json          # 506 NSE stock symbols
sessions/pumpwatch_session.session  # Telegram session
.env                           # Configuration
```

---

## 🎯 Key Features

1. **Multi-Platform**: Telegram + Reddit + Market Data
2. **Real-Time**: Fetches latest messages on demand
3. **Intelligent**: Hinglish support, sentiment analysis
4. **Statistical**: Z-score anomaly detection
5. **Validation**: Compares social vs official NSE data
6. **Comprehensive**: 5-component risk breakdown
7. **Actionable**: Natural language explanations

---

## 🚀 Performance

- **Startup**: 2-3 seconds (Telegram connection)
- **Message Fetch**: 1-2 seconds (50 messages)
- **Ticker Analysis**: 2-3 seconds (yfinance + analysis)
- **Reddit Scrape**: 12 seconds (6 subreddits)
- **Memory**: ~50MB (500 messages cached)

---

**End of Complete Project Flow** 🎯
