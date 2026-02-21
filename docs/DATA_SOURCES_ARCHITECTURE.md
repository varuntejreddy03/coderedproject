# 🏗️ PumpWatch - Data Sources Architecture

## Overview

PumpWatch uses a **two-tier data architecture** to detect pump & dump schemes:

1. **🔴 RUMOR SOURCES (Untrusted)** - Monitored for fraud detection
2. **✅ VERIFICATION SOURCES (Trusted)** - Used for validation

---

## 🔴 RUMOR SOURCES (Untrusted)

These platforms are **monitored** for potential fraud, manipulation, and pump & dump schemes. Data from these sources is **NOT trusted** and must be validated.

### 1. Telegram Channels

**Purpose**: Detect coordinated pump & dump activity

**What We Monitor**:
- Pump & dump groups (e.g., "pakkapredictions890")
- Stock tip channels
- Trading signal groups

**Data Collected**:
- Message text (with Hinglish support)
- Ticker mentions
- Fraud keywords ("pakka", "guaranteed", "upper circuit")
- Posting velocity (rapid posting = bot activity)
- Sentiment (bullish/bearish)

**Implementation**: `scrapers/simple_telegram.py`

**Why Untrusted**:
- Anonymous users
- No accountability
- Known for manipulation
- Coordinated bot activity
- False claims & rumors

---

### 2. Reddit Communities

**Purpose**: Detect social media hype & speculation

**Subreddits Monitored**:
- r/IndianStockMarket
- r/IndianStreetBets
- r/DalalStreetTalks
- r/StockMarketIndia

**Data Collected**:
- Post titles & content
- Ticker mentions
- Hype keywords ("moon", "rocket", "multibagger")
- Upvotes & comments (engagement)
- Sentiment analysis

**Implementation**: `scrapers/reddit_hype_analyzer.py`

**Why Untrusted**:
- Speculative discussions
- Retail investor sentiment (not expert analysis)
- Hype-driven content
- No verification required
- Echo chamber effect

---

## ✅ VERIFICATION SOURCES (Trusted)

These sources provide **official, verified data** used to validate social media claims.

### 1. yfinance (Yahoo Finance)

**Purpose**: Official market data & corporate information

**Data Retrieved**:
- **Real-time Price**: Current stock price
- **Volume Data**: Trading volume (for anomaly detection)
- **Market Cap**: Company valuation
- **Price Changes**: Daily/weekly price movements
- **Corporate Actions**: Dividends, stock splits
- **News**: Official news articles
- **Historical Data**: 3-month volume history (for Z-score calculation)

**Implementation**: Used in all `core/` modules
```python
import yfinance as yf
stock = yf.Ticker(f"{ticker}.NS")  # .NS for NSE stocks
info = stock.info
hist = stock.history(period="3mo")
```

**Why Trusted**:
- Official Yahoo Finance data
- Aggregates from NSE/BSE
- Real-time market data
- Corporate filings included
- Widely used by financial institutions

---

### 2. NSE/BSE Official Filings

**Purpose**: Verify corporate announcements & regulatory filings

**Data Retrieved** (via yfinance):
- Corporate announcements
- Dividend declarations
- Stock split notifications
- Quarterly results
- Board meeting outcomes
- Insider trading disclosures

**Implementation**: `core/legitimacy_validator.py`
```python
def get_nse_filings(self, ticker: str) -> Dict:
    stock = yf.Ticker(f"{ticker}.NS")
    news = stock.news  # Official news from NSE/BSE
    info = stock.info  # Corporate actions
```

**Why Trusted**:
- Regulatory requirement (SEBI)
- Legally binding
- Audited information
- Penalties for false disclosure
- Public record

---

### 3. Market Metrics (via yfinance)

**Purpose**: Statistical analysis & anomaly detection

**Metrics Used**:
- **Volume Z-Score**: Detect unusual volume spikes
  ```python
  z_score = (current_volume - mean_volume) / std_volume
  # Z > 3 = 99.7% confidence anomaly
  ```
- **Liquidity**: Average trading volume
- **Market Cap**: Company size (penny stock detection)
- **Price Volatility**: Unusual price movements

**Implementation**: `core/risk_analyzer.py`, `core/market_data.py`

**Why Trusted**:
- Mathematical/statistical analysis
- Based on historical data
- Objective metrics
- Industry-standard calculations

---

## 🧠 Validation Logic

### Core Algorithm

```python
# Step 1: Collect rumors from untrusted sources
telegram_hype = analyze_telegram_messages(ticker)
reddit_hype = analyze_reddit_posts(ticker)

# Step 2: Get official data from trusted sources
official_data = yfinance.get_stock_data(ticker)
nse_filings = yfinance.get_news(ticker)

# Step 3: Compare & validate
if telegram_hype > 70 and nse_filings == 0:
    verdict = "LIKELY_RUMOR"  # RED FLAG
    risk_score = 85
elif telegram_hype > 70 and nse_filings > 0:
    verdict = "LEGITIMATE"  # GREEN
    risk_score = 30
else:
    verdict = "UNCERTAIN"  # AMBER
    risk_score = 50
```

### Decision Matrix

| Social Hype | Official Filings | Volume Spike | Verdict | Risk Score |
|-------------|------------------|--------------|---------|------------|
| HIGH (>70)  | ZERO             | YES          | **LIKELY_RUMOR** | 85-100 |
| HIGH (>70)  | PRESENT          | YES          | **LEGITIMATE** | 20-40 |
| HIGH (>70)  | ZERO             | NO           | **LIKELY_RUMOR** | 70-85 |
| LOW (<30)   | PRESENT          | NO           | **LEGITIMATE** | 0-20 |
| MEDIUM      | ZERO             | YES          | **UNCERTAIN** | 50-70 |

---

## 📊 Data Flow Example

### Scenario: "YESBANK" mentioned in Telegram

```
1. RUMOR DETECTION (Untrusted Sources)
   ├─ Telegram: 45 messages with "YESBANK pakka upper circuit"
   ├─ Reddit: 12 posts mentioning "YESBANK moon"
   └─ Hype Score: 85/100 (HIGH)

2. VERIFICATION (Trusted Sources)
   ├─ yfinance: Fetch YESBANK.NS data
   │   ├─ Price: ₹42.30 (+11.2%)
   │   ├─ Volume: 4.2M (Z-score: 3.8 - ANOMALY)
   │   ├─ Market Cap: ₹12,500 Cr
   │   └─ News: 0 official filings in last 90 days
   │
   └─ NSE Filings: ZERO corporate actions

3. RISK ASSESSMENT
   ├─ Social Hype: 85/100 (HIGH)
   ├─ Volume Anomaly: 74/100 (Z-score > 3)
   ├─ Official Filings: 0 (RED FLAG)
   ├─ Bot Activity: 68/100 (Coordinated posting)
   └─ VERDICT: LIKELY_RUMOR (Risk: 82/100 - RED)

4. EXPLANATION
   "High social hype (85) with ZERO official NSE filings.
    Volume spike 3.8x above average with no corporate action.
    Bot-like posting patterns detected. AVOID."
```

---

## 🔧 Implementation Files

### Rumor Sources (Untrusted)
- `scrapers/simple_telegram.py` - Telegram scraper
- `scrapers/reddit_scraper.py` - Reddit scraper
- `scrapers/reddit_hype_analyzer.py` - Reddit hype analysis

### Verification Sources (Trusted)
- `core/market_data.py` - yfinance integration
- `core/legitimacy_validator.py` - NSE filing validation
- `core/risk_analyzer.py` - Volume anomaly detection

### Analysis Engines
- `core/intelligence_engine.py` - Sentiment & fraud detection
- `core/comprehensive_analyzer.py` - Complete ticker analysis

### API Layer
- `main.py` - FastAPI endpoints

---

## 🎯 Key Principles

1. **Never Trust Social Media Alone**
   - Telegram & Reddit are monitored, not trusted
   - Always validate against official sources

2. **Official Data is Ground Truth**
   - yfinance provides verified market data
   - NSE/BSE filings are legally binding

3. **High Hype + No Official Data = RED FLAG**
   - Core detection logic
   - Indicates potential pump & dump

4. **Statistical Validation**
   - Z-score for volume anomalies
   - Historical data for context

5. **Multi-Source Verification**
   - Cross-check multiple trusted sources
   - Reduce false positives

---

## 📚 References

- **yfinance Documentation**: https://pypi.org/project/yfinance/
- **NSE India**: https://www.nseindia.com/
- **BSE India**: https://www.bseindia.com/
- **SEBI Regulations**: https://www.sebi.gov.in/

---

**Built for NMIMS 24hr Hackathon** 🏆
