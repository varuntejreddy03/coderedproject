# PumpWatch - AI Market Integrity Guard

Real-time pump & dump detection system using multi-platform social intelligence.

## 🎯 Core Concept

### 🔴 RUMOR SOURCES (Untrusted - Monitored for Fraud)
- **Telegram**: Pump & dump groups, tip channels
- **Reddit**: IndianStockMarket, IndianStreetBets (speculation)

### ✅ VERIFICATION SOURCES (Trusted - Used for Validation)
- **yfinance**: Yahoo Finance official market data
- **NSE/BSE**: Official filings & corporate announcements
- **Market Data**: Volume, price, market cap, liquidity metrics

### 🧠 Detection Logic
```
Rumor Detection (Telegram/Reddit) → Validation (yfinance/NSE) → Risk Score

IF Social Hype HIGH + Official Data ZERO → LIKELY RUMOR (RED FLAG)
IF Social Hype HIGH + Official Data PRESENT → LEGITIMATE (GREEN)
```

## 🎯 Features

- ✅ **Multi-Platform Monitoring**: 
  - 🔴 **Rumor Sources**: Telegram + Reddit (untrusted, monitored for fraud)
  - ✅ **Verification Sources**: yfinance + NSE/BSE (trusted, used for validation)
- ✅ **Rumor Validation**: Validates social media claims against official NSE filings & yfinance data
- ✅ **Risk Scoring**: 0-100 unified risk score with 5-component breakdown
- ✅ **Bot Detection**: Identifies coordinated manipulation patterns
- ✅ **Volume Anomaly**: Z-score based statistical analysis using yfinance
- ✅ **Hinglish Support**: Understands Indian market language
- ✅ **Real-time API**: FastAPI with comprehensive endpoints

## 📁 Project Structure

```
nmims24hr/
├── main.py                 # FastAPI application
├── requirements.txt        # Dependencies
├── .env                    # Configuration
│
├── core/                   # Analysis engines
│   ├── intelligence_engine.py
│   ├── risk_analyzer.py
│   ├── market_data.py
│   ├── legitimacy_validator.py
│   └── comprehensive_analyzer.py
│
├── scrapers/               # Data collection
│   ├── simple_telegram.py
│   ├── reddit_scraper.py
│   ├── reddit_hype_analyzer.py
│   └── fetch_nse_stocks.py
│
├── tests/                  # Test scripts
│   ├── test_api.py
│   └── test_comprehensive.py
│
├── data/                   # Data files
│   └── nse_stocks.json
│
├── sessions/               # Telegram sessions
│   └── pumpwatch_session.session
│
└── docs/                   # Documentation
    ├── RUMOR_VALIDATION_GUIDE.md
    ├── FLOW_EXPLANATION.md
    └── ...
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Telegram API credentials
```

### 3. Run Server
```bash
python main.py
```

### 4. Test API
```bash
python tests/test_api.py
```

## 📡 Key API Endpoints

### Comprehensive Analysis
```
GET /ticker-analysis/{ticker}
```
Returns complete analysis matching UI requirements:
- Risk Assessment (0-100)
- Market Data (Price, Volume, Z-Score)
- Social Activity (Telegram, Reddit, X)
- AI Analysis
- Risk Breakdown (5 components)
- Legitimacy Validation

### Other Endpoints
- `GET /health` - System health
- `GET /refresh` - Refresh Telegram messages
- `GET /fraud-alerts` - High-risk messages
- `GET /safety-dashboard` - RED/AMBER/GREEN indicators
- `GET /risk-score/{ticker}` - Unified risk score
- `GET /anomaly-detection` - Volume anomalies
- `GET /bot-activity/{ticker}` - Bot detection
- `GET /reddit-hype` - Reddit analysis

## 🔍 How It Works

### Data Flow Architecture

```
┌──────────────────────────────────────────────────────┐
│  🔴 RUMOR SOURCES (Untrusted - Monitored)        │
│  - Telegram pump groups                           │
│  - Reddit speculation (IndianStockMarket)         │
└──────────────────────────────────────────────────────┘
                        │
                        ↓ Scrape & Analyze
                        │
┌──────────────────────────────────────────────────────┐
│  🧠 DETECTION ENGINE                            │
│  - Extract tickers & sentiment                    │
│  - Detect fraud keywords (Hinglish)               │
│  - Calculate hype intensity                       │
│  - Identify bot patterns                          │
└──────────────────────────────────────────────────────┘
                        │
                        ↓ Validate Against
                        │
┌──────────────────────────────────────────────────────┐
│  ✅ VERIFICATION SOURCES (Trusted)                │
│  - yfinance (Yahoo Finance official data)         │
│  - NSE/BSE filings & announcements                │
│  - Corporate actions (dividends, splits)          │
│  - Volume & price data                            │
└──────────────────────────────────────────────────────┘
                        │
                        ↓ Generate
                        │
┌──────────────────────────────────────────────────────┐
│  🚨 RISK ASSESSMENT                             │
│  - Unified Risk Score (0-100)                     │
│  - RED/AMBER/GREEN indicator                      │
│  - Legitimacy verdict                             │
│  - AI-generated explanation                       │
└──────────────────────────────────────────────────────┘
```

### Rumor Validation System

```
Social Media Claims (Telegram/Reddit) → Validate → Official Data (yfinance/NSE)
                                                            ↓
                                                  Legitimacy Score
                                                            ↓
                                      LEGITIMATE / UNCERTAIN / LIKELY_RUMOR
```

**Red Flags** (Indicates RUMOR):
- High social hype + NO official filings (yfinance/NSE)
- Volume spike + NO corporate action
- NO coverage from trusted sources

**Green Flags** (Indicates LEGITIMATE):
- Official NSE filings present (via yfinance)
- Corporate action announced
- Covered by official sources

## 📊 Risk Breakdown Components

1. **Social Hype Score** (0-100): Mention count + velocity + fraud triggers
2. **Volume Anomaly** (0-100): Z-score based statistical analysis
3. **Bot Coordination** (0-100): Rapid posting + copy-paste detection
4. **Sentiment Spike** (0-100): Extreme bullish/bearish sentiment
5. **Lack of Filings** (0-100): Absence of official NSE announcements

## 🧪 Testing

```bash
# Test all endpoints
python tests/test_api.py

# Test comprehensive analysis
python tests/test_comprehensive.py
```

## 📚 Documentation

See `docs/` folder for detailed guides:
- `RUMOR_VALIDATION_GUIDE.md` - Complete system documentation
- `FLOW_EXPLANATION.md` - Application flow explained
- `TROUBLESHOOTING.md` - Common issues and fixes

## 🔧 Configuration

Edit `.env`:
```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
CHANNELS=pakkapredictions890
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please read the documentation in `docs/` folder.

---

**Built for NMIMS 24hr Hackathon** 🏆
