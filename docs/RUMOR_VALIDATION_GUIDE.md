# 🎯 Rumor Validation System - Complete Guide

## Overview
This system treats **Telegram and Reddit as "rumored platforms"** and validates their claims against **official NSE market data** to detect pump & dump schemes.

---

## 🔍 Core Concept: Rumor vs Reality

### Rumored Platforms (Unverified)
- **Telegram**: Where operators coordinate pump & dump
- **Reddit**: Where retail investors discuss (mix of rumors + warnings)

### Official Data Sources (Verified)
- **NSE Filings**: Corporate announcements, dividends, splits
- **BSE News**: Official press releases
- **yfinance**: Real-time price, volume, market cap
- **Market Fundamentals**: P/E ratio, debt, revenue

---

## 📊 Complete Analysis Parameters (Matching UI)

### 1. RISK ASSESSMENT (Main Circle)
```
Score: 82/100
Level: HIGH RISK
Color: RED
```

**Calculation**:
```python
Risk Score = Weighted Average of:
  - Social Hype Score (25%)
  - Volume Anomaly (20%)
  - Bot Coordination (20%)
  - Sentiment Spike (15%)
  - Lack of Filings (20%)

Adjusted by Legitimacy:
  - If LIKELY_RUMOR → Score × 1.2
  - If LEGITIMATE → Score × 0.8
```

---

### 2. MARKET DATA

#### Price & Change
```
Price: ₹42.30
Change: +11.2%
```
**Source**: yfinance real-time data

#### Volume Analysis
```
Volume: 4.2M
Avg Volume: 900K
Z-Score: 3.8
```

**Z-Score Interpretation**:
- `< 2`: Normal volume
- `2-3`: Elevated volume
- `> 3`: **ANOMALY** (99.7% confidence)

**Chart**: 30-day volume bars with trend line

---

### 3. SOCIAL ACTIVITY (Last 5 min)

#### Telegram
```
Mentions: 342
Sentiment: Bullish
Keywords: ["Upper Circuit Pakka", "Target 5x"]
```

**Analysis**:
- Extracts fraud keywords
- Calculates hype intensity (0-100)
- Tracks mention velocity

#### Reddit
```
Mentions: 87
Sentiment: Bullish
Keywords: ["Operator Game", "Insider News"]
```

**Analysis**:
- Scans 6 Indian stock subreddits
- Detects warning posts
- Community sentiment

#### X (Twitter)
```
Mentions: 156
Sentiment: Bullish
Keywords: ["Target 5x", "Upper Circuit Pakka"]
```

**Note**: Requires paid API ($100/month)

---

### 4. AI ANALYSIS

**Example Output**:
```
Coordinated Telegram activity detected across 3 channels. 
Volume spike 4.3x above 5-day average. 
No NSE filings found in last 90 days. 
Bot-like posting patterns identified with 68% confidence.
```

**Components**:
1. **Coordination Detection**: Multi-channel activity
2. **Volume Analysis**: Statistical anomaly
3. **Filing Check**: Official news presence
4. **Bot Detection**: Automated posting patterns

---

### 5. RISK BREAKDOWN (5 Bars)

#### Social Hype Score: 85%
```
████████████████████ (RED)
```
**Calculation**:
- Mention count (0-25)
- Velocity/acceleration (0-25)
- Fraud trigger density (0-25)
- Sentiment extremity (0-25)

#### Volume Anomaly: 74%
```
███████████████ (RED)
```
**Calculation**:
- Z-score based
- `Z > 3` → High risk
- Compares to 3-month average

#### Bot Coordination: 68%
```
██████████████ (ORANGE)
```
**Detection**:
- Rapid posting (< 5 min intervals)
- Copy-paste messages (70% similarity)
- Multi-channel coordination

#### Sentiment Spike: 80%
```
████████████████ (RED)
```
**Calculation**:
- Extreme bullish/bearish sentiment
- Deviation from normal
- FOMO indicators

#### Lack of Filings: 90%
```
██████████████████ (RED)
```
**Check**:
- NSE announcements (last 90 days)
- Corporate actions (dividend, split)
- Official news sources

---

## 🛡️ Legitimacy Validation

### Core Logic: Rumor vs Reality

```python
IF social_hype > 70 AND no_official_filings:
    RED FLAG: "High hype with ZERO official news"
    
IF volume_spike > 150% AND no_corporate_action:
    RED FLAG: "Volume spike without reason"
    
IF no_official_news_sources:
    RED FLAG: "Not covered by BSE/NSE"
```

### Legitimacy Score (0-100)

**Starts at 50 (neutral)**

**Red Flags** (subtract points):
- High social hype + No filings: **-30**
- Volume spike + No corporate action: **-25**
- No official news sources: **-15**

**Green Flags** (add points):
- Official filings present: **+20**
- Corporate action announced: **+15**
- Covered by official sources: **+15**

### Verdict

```
Score >= 70: LEGITIMATE (GREEN)
Score 40-69: UNCERTAIN (AMBER)
Score < 40: LIKELY_RUMOR (RED)
```

---

## 🔄 Complete Flow

### Step 1: Data Collection
```
Telegram Messages → SimpleTelegramScraper
Reddit Posts → RedditHypeAnalyzer
Market Data → yfinance
NSE Filings → yfinance.info
```

### Step 2: Social Analysis
```
IntelligenceEngine:
  - Sentiment analysis
  - Fraud trigger detection
  - Hinglish normalization
  - Hype intensity calculation
```

### Step 3: Market Validation
```
LegitimacyValidator:
  - Check NSE filings
  - Validate price claims
  - Verify volume legitimacy
  - Compare social vs official
```

### Step 4: Risk Assessment
```
RiskAnalyzer:
  - Volume anomaly (Z-score)
  - Bot activity detection
  - Unified risk scoring
```

### Step 5: Comprehensive Output
```
ComprehensiveTickerAnalyzer:
  - Risk assessment (0-100)
  - Market data
  - Social activity
  - AI analysis
  - Risk breakdown
  - Legitimacy verdict
```

---

## 📡 API Endpoint

### `/ticker-analysis/{ticker}`

**Example Request**:
```bash
GET http://localhost:8080/ticker-analysis/YESBANK
```

**Response Structure**:
```json
{
  "ticker": "YESBANK",
  "timestamp": "2026-02-21T20:30:00",
  
  "risk_assessment": {
    "score": 82,
    "level": "HIGH RISK",
    "color": "RED"
  },
  
  "market_data": {
    "price": 42.30,
    "change_percent": 11.2,
    "volume": 4200000,
    "avg_volume": 900000,
    "z_score": 3.8,
    "volume_chart": [...]
  },
  
  "social_activity": {
    "telegram": {
      "mention_count": 342,
      "sentiment": "Bullish",
      "keywords": ["Upper Circuit Pakka", "Target 5x"]
    },
    "reddit": {...},
    "x": {...}
  },
  
  "ai_analysis": "Coordinated Telegram activity...",
  
  "risk_breakdown": {
    "social_hype_score": {"value": 85, "color": "red"},
    "volume_anomaly": {"value": 74, "color": "red"},
    "bot_coordination": {"value": 68, "color": "orange"},
    "sentiment_spike": {"value": 80, "color": "red"},
    "lack_of_filings": {"value": 90, "color": "red"}
  },
  
  "legitimacy": {
    "legitimacy_score": 25,
    "verdict": "LIKELY_RUMOR",
    "color_indicator": "RED",
    "red_flags": [
      "High social hype with ZERO official filings",
      "Unusual volume spike without corporate action"
    ],
    "green_flags": [],
    "recommendation": "🚨 LIKELY RUMOR: 2 red flags detected..."
  }
}
```

---

## 🧪 Testing

### 1. Start Server
```bash
python main.py
```

### 2. Send Test Message to Telegram
```
YESBANK pakka upper circuit guaranteed 100% multibagger
```

### 3. Refresh Data
```bash
curl http://localhost:8080/refresh
```

### 4. Run Comprehensive Analysis
```bash
python test_comprehensive.py
```

### Expected Output
```
================================================================================
RISK ASSESSMENT
================================================================================
Score: 82/100
Level: HIGH RISK
Color: RED

================================================================================
MARKET DATA
================================================================================
Price: ₹42.30
Change: +11.20%
Volume: 4,200,000
Avg Volume: 900,000
Z-Score: 3.8

================================================================================
SOCIAL ACTIVITY
================================================================================

Telegram: 342 mentions
  Sentiment: Bullish
  Keywords: Upper Circuit Pakka, Target 5x

Reddit: 87 mentions
  Sentiment: Bullish
  Keywords: Operator Game, Insider News

================================================================================
AI ANALYSIS
================================================================================
Coordinated Telegram activity detected across 3 channels. Volume spike 4.3x 
above 5-day average. No NSE filings found in last 90 days. Bot-like posting 
patterns identified with 68% confidence.

================================================================================
RISK BREAKDOWN
================================================================================
Social Hype Score.............. 85% ████████████████████
Volume Anomaly................. 74% ███████████████
Bot Coordination............... 68% ██████████████
Sentiment Spike................ 80% ████████████████
Lack of Filings................ 90% ██████████████████

================================================================================
LEGITIMACY VALIDATION (Rumor vs Reality)
================================================================================
Verdict: LIKELY_RUMOR
Legitimacy Score: 25/100
Color: RED

🚨 RED FLAGS:
  - High social hype with ZERO official filings
  - Unusual volume spike without corporate action
  - No coverage from official news sources (BSE/NSE)

Recommendation: 🚨 LIKELY RUMOR: 3 red flags detected. Avoid acting on 
social media claims alone.
```

---

## 🎯 Key Differentiators

### Traditional Systems
- Trust social media blindly
- No validation against official data
- Simple keyword matching

### PumpWatch (This System)
- ✅ Treats social media as **rumors**
- ✅ Validates against **NSE filings**
- ✅ Cross-checks **volume with corporate actions**
- ✅ Detects **bot coordination**
- ✅ Provides **legitimacy score**
- ✅ Generates **actionable recommendations**

---

## 📈 Use Cases

### 1. Retail Investor Protection
```
Scenario: User sees "YESBANK guaranteed 100%" on Telegram
Action: Check /ticker-analysis/YESBANK
Result: 82/100 risk, LIKELY_RUMOR verdict
Decision: AVOID
```

### 2. SEBI Monitoring
```
Scenario: Detect coordinated pump & dump
Action: Monitor high-risk tickers
Result: Identify operator networks
Decision: Investigate
```

### 3. Broker Risk Management
```
Scenario: Client wants to buy hyped penny stock
Action: Check legitimacy score
Result: 25/100 legitimacy, no filings
Decision: Warn client
```

---

## 🚀 Production Deployment

### Enhancements Needed
1. **Database**: PostgreSQL for message storage
2. **Caching**: Redis for API responses
3. **Background Jobs**: Celery for continuous monitoring
4. **Webhooks**: Real-time alerts
5. **ML Models**: Advanced bot detection
6. **Twitter API**: Paid tier for X integration

### Scalability
- Handle 10K+ messages/minute
- Support 500+ NSE stocks
- Real-time risk updates
- Multi-user dashboard

---

## 📚 Files Created

1. `legitimacy_validator.py` - Validates rumors vs reality
2. `comprehensive_analyzer.py` - Complete ticker analysis
3. `test_comprehensive.py` - Testing script
4. `RUMOR_VALIDATION_GUIDE.md` - This documentation

---

## 🎓 Summary

**Problem**: Social media pump & dump schemes

**Solution**: Validate social rumors against official NSE data

**Output**: 
- Risk score (0-100)
- Legitimacy verdict (RUMOR vs LEGITIMATE)
- 5-component risk breakdown
- AI-generated analysis
- Actionable recommendations

**Impact**: Protect retail investors from manipulation! 🛡️
