"""
PumpWatch API - Optimized for Hackathon Requirements

🔴 RUMOR SOURCES (Untrusted - monitored for fraud detection):
   - Telegram channels (pump & dump groups)
   - Reddit (IndianStockMarket, IndianStreetBets)
   - YouTube (stock tip videos & comments)

✅ VERIFICATION SOURCES (Trusted - used for validation):
   - yfinance (Yahoo Finance official data)
   - NSE/BSE official filings & announcements
   - Corporate action data
   - Official market metrics (volume, price, market cap)

Implements: Multi-platform scraper, Reality Check, Risk Scoring, Anomaly Detection
Core Logic: Detect rumors from social media → Validate against official sources
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import List, Dict
from datetime import datetime, timedelta

# Import from organized packages
from scrapers.simple_telegram import SimpleTelegramScraper
from scrapers.reddit_scraper import RedditScraper
from core.risk_analyzer import RiskAnalyzer, get_all_anomalies
from core.market_data import MarketDataChecker
from core.intelligence_engine import IntelligenceEngine
from core.comprehensive_analyzer import ComprehensiveTickerAnalyzer
from core.mention_burst_detector import burst_detector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

# Global instances
scraper = None
reddit_scraper: RedditScraper = None
youtube_scraper = None
supabase_db = None
job_queue = None
risk_analyzer = RiskAnalyzer()
startup_time = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scraper, reddit_scraper, startup_time, supabase_db
    startup_time = datetime.now()
    
    logger.info("🚀 Starting PumpWatch - AI Market Integrity Guard")
    logger.info("🔴 RUMOR SOURCES: Telegram + Reddit + YouTube (monitored for fraud)")
    logger.info("✅ VERIFICATION: yfinance + NSE/BSE (trusted validation)")
    
    # Supabase setup (DATABASE)
    try:
        from core.supabase_db import SupabaseDB
        supabase_db = SupabaseDB()
        logger.info("✅ Supabase database connected")
    except Exception as e:
        logger.warning(f"⚠️ Supabase not configured: {e}")
        supabase_db = None
    
    # Job Queue setup
    from core.job_queue import JobQueue
    job_queue = JobQueue(supabase_db)
    asyncio.create_task(job_queue.start_worker())
    logger.info("✅ Job queue worker started (async processing)")
    
    # Telegram setup (simplified)
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    channels = [c.strip() for c in os.getenv("CHANNELS", "").split(",") if c.strip()]
    
    if channels:
        scraper = SimpleTelegramScraper(api_id, api_hash, channels)
        try:
            logger.info("🔄 Connecting to Telegram...")
            await scraper.connect()
            logger.info("✅ Telegram connected")
            
            # Fetch messages
            logger.info("🔄 Fetching messages...")
            await scraper.fetch_messages(limit=50)
            logger.info(f"✅ Telegram: {len(scraper.messages)} messages loaded")
            
            # Store to DB
            if supabase_db:
                stored = 0
                for msg in scraper.messages:
                    try:
                        if supabase_db.store_telegram_message(msg):
                            stored += 1
                    except:
                        pass
                logger.info(f"💾 Stored {stored} messages to database")
            
            logger.info("✅ Telegram setup complete")
        except Exception as e:
            logger.error(f"❌ Telegram error: {e}")
            scraper = None
    else:
        logger.warning("⚠️ No Telegram channels configured")
        scraper = None
    
    # Reddit setup (RUMOR SOURCE)
    reddit_scraper = RedditScraper()
    logger.info("✅ Reddit scraper initialized (RUMOR SOURCE)")
    
    # Auto-scrape and store Reddit data
    if supabase_db:
        try:
            from scrapers.reddit_hype_analyzer import RedditHypeAnalyzer
            reddit_analyzer = RedditHypeAnalyzer()
            logger.info("🔍 Scraping Reddit...")
            reddit_result = reddit_analyzer.analyze_reddit_hype()
            
            stored = 0
            skipped = 0
            for ticker, data in list(reddit_result['top_hyped_stocks'].items())[:10]:
                for post in data['posts'][:3]:
                    # Add to queue (non-blocking)
                    if job_queue:
                        await job_queue.add_job('reddit_post', post)
                        stored += 1
            logger.info(f"📥 Queued {stored} Reddit posts for processing")
        except Exception as e:
            logger.warning(f"⚠️ Reddit scraping failed: {e}")
    
    # YouTube setup (RUMOR SOURCE)
    try:
        from scrapers.youtube_scraper import YouTubeScraperNoAPI
        youtube_scraper = YouTubeScraperNoAPI()
        logger.info("✅ YouTube scraper initialized (RUMOR SOURCE - No API)")
        
        # Auto-scrape and store YouTube data
        if supabase_db:
            try:
                logger.info("🔍 Scraping YouTube...")
                youtube_result = youtube_scraper.analyze_youtube_hype()
                
                stored = 0
                skipped = 0
                for ticker, data in list(youtube_result['top_hyped_stocks'].items())[:10]:
                    for video_title in data['videos'][:2]:
                        video_data = {
                            'title': video_title,
                            'channel': 'Unknown',
                            'tickers': [ticker],
                            'hype_score': data['avg_hype_score'],
                            'url': f'https://youtube.com/results?search_query={ticker}'
                        }
                        # Add to queue (non-blocking)
                        if job_queue:
                            await job_queue.add_job('youtube_video', video_data)
                            stored += 1
                logger.info(f"📥 Queued {stored} YouTube videos for processing")
            except Exception as e:
                logger.warning(f"⚠️ YouTube scraping failed: {e}")
    except Exception as e:
        logger.warning(f"⚠️ YouTube scraper failed to initialize: {e}")
    
    logger.info("✅ Backend ready at http://localhost:8080")
    logger.info("📚 API Docs at http://localhost:8080/docs")
    
    yield
    
    if scraper:
        await scraper.disconnect()
    logger.info("👋 PumpWatch shutdown complete")


app = FastAPI(
    title="PumpWatch - AI Market Integrity Guard",
    description="Real-time pump & dump detection using multi-platform social intelligence",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# CORE DETECTION APIs
# ============================================================================

@app.get("/fraud-alerts")
async def get_fraud_alerts(min_risk: int = 2):
    """
    🚨 High-Risk Fraud Detection from DATABASE
    🔴 Analyzes: Telegram/Reddit messages (UNTRUSTED)
    Returns messages with fraud triggers (Hinglish supported)
    """
    if not supabase_db:
        return {"high_risk_messages": [], "total_alerts": 0}
    
    # Query database for high fraud score messages
    result = supabase_db.client.table('rumor_sources')\
        .select('*')\
        .gte('fraud_score', min_risk)\
        .order('created_at', desc=True)\
        .limit(50)\
        .execute()
    
    alerts = result.data
    
    # Count by ticker
    ticker_fraud_count = {}
    for msg in alerts:
        for ticker in msg.get('tickers', []):
            ticker_fraud_count[ticker] = ticker_fraud_count.get(ticker, 0) + 1
    
    return {
        "high_risk_messages": alerts,
        "total_alerts": len(alerts),
        "top_suspicious_tickers": dict(sorted(ticker_fraud_count.items(), key=lambda x: x[1], reverse=True)[:10]),
        "source": "database"
    }


@app.get("/safety-dashboard")
async def safety_dashboard():
    """
    🎯 RED/AMBER/GREEN Safety Dashboard
    🔴 RUMOR: Social hype from Telegram/Reddit
    ✅ VERIFICATION: Market data from yfinance
    Real-time risk indicators for all monitored stocks
    """
    if not scraper:
        return {"error": "No data available", "red_alerts": [], "amber_alerts": [], "green_stocks": []}
    
    checker = MarketDataChecker()
    intelligence = IntelligenceEngine()
    
    all_tickers = scraper.get_all_tickers()
    red_alerts, amber_alerts, green_stocks = [], [], []
    
    for ticker in list(all_tickers.keys())[:20]:  # Limit to top 20 for speed
        matching = [m for m in scraper.messages if ticker in m.get('tickers', [])]
        if not matching:
            continue
        
        msg_dicts = [{'text': m.get('text', ''), 'date': m.get('date')} for m in matching]
        intensity = intelligence.calculate_hype_intensity(ticker, msg_dicts)
        
        result = checker.reality_check(
            ticker=ticker,
            social_hype=intensity['hype_score'],
            fraud_score=int(intensity['metrics'].get('trigger_density', 0) * 10)
        )
        
        if result['safety_indicator'] == 'RED':
            red_alerts.append(result)
        elif result['safety_indicator'] == 'AMBER':
            amber_alerts.append(result)
        else:
            green_stocks.append(result)
    
    return {
        "last_updated": datetime.now().isoformat(),
        "detection_latency_seconds": (datetime.now() - startup_time).total_seconds(),
        "total_stocks_monitored": len(all_tickers),
        "red_alerts": red_alerts,
        "amber_alerts": amber_alerts,
        "green_stocks": green_stocks,
        "summary": {
            "critical": len(red_alerts),
            "warning": len(amber_alerts),
            "safe": len(green_stocks)
        }
    }


@app.get("/reality-check/{ticker}")
async def reality_check(ticker: str):
    """
    ⚖️ Reality Check: RUMOR vs REALITY
    🔴 RUMOR: Social Hype from Telegram/Reddit (UNTRUSTED)
    ✅ VERIFICATION: Market Fundamentals from yfinance (TRUSTED)
    Detects manipulation when hype is HIGH but fundamentals are ZERO
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    intelligence = IntelligenceEngine()
    msg_dicts = [{'text': m.get('text', ''), 'date': m.get('date')} for m in matching]
    intensity = intelligence.calculate_hype_intensity(ticker.upper(), msg_dicts)
    
    checker = MarketDataChecker()
    result = checker.reality_check(
        ticker=ticker.upper(),
        social_hype=intensity['hype_score'],
        fraud_score=int(intensity['metrics'].get('trigger_density', 0) * 10)
    )
    
    return result


@app.get("/hype-intensity/{ticker}")
async def get_hype_intensity(ticker: str):
    """
    📊 Hype Intensity Analysis from RUMOR SOURCES
    🔴 Analyzes: Telegram/Reddit (UNTRUSTED)
    Combines: mentions + velocity + fraud triggers + sentiment
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    intelligence = IntelligenceEngine()
    msg_dicts = [{'text': m.get('text', ''), 'date': m.get('date')} for m in matching]
    intensity = intelligence.calculate_hype_intensity(ticker.upper(), msg_dicts)
    intensity['recent_messages'] = matching[-10:]
    
    return {
        "ticker": ticker.upper(),
        **intensity
    }


# ============================================================================
# NEW REQUIRED APIs
# ============================================================================

@app.get("/risk-score/{ticker}")
async def get_risk_score(ticker: str):
    """
    🎲 Unified Risk Score (0-100)
    🔴 RUMOR: Hype + Fraud from Telegram/Reddit
    ✅ VERIFICATION: Volume Anomaly from yfinance
    Combines: Hype + Fraud + Volume Anomaly + Bot Activity
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    # Get hype intensity
    intelligence = IntelligenceEngine()
    msg_dicts = [{'text': m.get('text', ''), 'date': m.get('date')} for m in matching]
    intensity = intelligence.calculate_hype_intensity(ticker.upper(), msg_dicts)
    
    # Detect anomalies
    anomaly_data = risk_analyzer.detect_volume_anomaly(ticker.upper())
    
    # Detect bot activity
    bot_data = risk_analyzer.detect_bot_activity(ticker.upper(), matching)
    
    # Calculate unified risk score
    risk_data = risk_analyzer.calculate_unified_risk_score(
        ticker.upper(),
        intensity['hype_score'],
        intensity['metrics'].get('trigger_density', 0) * 10,
        anomaly_data,
        bot_data
    )
    
    return {
        **risk_data,
        "anomaly_detection": anomaly_data,
        "bot_activity": bot_data,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/anomaly-detection")
async def detect_anomalies():
    """
    📈 Volume Anomaly Detection using TRUSTED yfinance data
    Uses Z-score to detect unusual volume spikes in monitored stocks
    """
    if not scraper:
        return {"anomalies": [], "total_checked": 0}
    
    all_tickers = list(scraper.get_all_tickers().keys())[:30]  # Check top 30
    anomalies = get_all_anomalies(all_tickers)
    
    return {
        "anomalies": anomalies,
        "total_checked": len(all_tickers),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/mention-burst/{ticker}")
async def get_mention_burst(ticker: str):
    """
    💥 Mention Burst Detection - Early Warning
    Tracks mention rate: 5-min baseline vs current 5-min window
    Catches pumps BEFORE price spike
    """
    result = burst_detector.detect_burst(ticker.upper())
    return {
        "ticker": ticker.upper(),
        **result,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/vernacular-analysis/{ticker}")
async def analyze_vernacular(ticker: str):
    """
    🌏 Vernacular & Hinglish Fraud Detection
    Detects pump phrases in Hindi, Telugu, Tamil, and transliteration variants
    Returns: detected phrases, language, fraud score
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    from core.vernacular_detector import vernacular_detector
    
    all_detections = []
    languages_found = set()
    total_fraud_score = 0
    
    for msg in matching:
        text = msg.get('text', '')
        detection = vernacular_detector.detect_vernacular_fraud(text)
        
        if detection['detected_phrases']:
            all_detections.append({
                'text': text[:100],
                'detected_phrases': detection['detected_phrases'],
                'language': detection['language'],
                'fraud_score': detection['fraud_score']
            })
            languages_found.add(detection['language'])
            total_fraud_score += detection['fraud_score']
    
    return {
        'ticker': ticker.upper(),
        'vernacular_detections': all_detections,
        'languages_detected': list(languages_found),
        'total_fraud_score': total_fraud_score,
        'messages_analyzed': len(matching),
        'vernacular_messages': len(all_detections),
        'timestamp': datetime.now().isoformat()
    }


@app.get("/trending-bursts")
async def get_trending_bursts(min_score: int = 50):
    """
    🔥 Trending Tickers with Burst Activity
    Returns tickers with sudden mention spikes (early pump warning)
    """
    trending = burst_detector.get_trending_tickers(min_burst_score=min_score)
    return {
        "trending_tickers": trending,
        "count": len(trending),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/bot-activity/{ticker}")
async def detect_bot_activity(ticker: str):
    """
    🤖 Coordinated Bot Activity Detection from RUMOR SOURCES
    🔴 Analyzes: Telegram/Reddit patterns (UNTRUSTED)
    Detects: Rapid posting, copy-paste messages, multi-channel coordination
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    bot_data = risk_analyzer.detect_bot_activity(ticker.upper(), matching)
    
    return {
        "ticker": ticker.upper(),
        **bot_data,
        "messages_analyzed": len(matching),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/ticker-analysis/{ticker}")
async def comprehensive_ticker_analysis(ticker: str):
    """
    🎯 COMPREHENSIVE TICKER ANALYSIS (Matches UI)
    🔴 RUMOR SOURCES: Telegram/Reddit (monitored for fraud)
    ✅ VERIFICATION: yfinance/NSE (validates claims)
    
    Returns: Risk Score, Market Data, Social Activity, AI Analysis, Risk Breakdown
    Validates social media rumors against official NSE data
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    # Get messages for this ticker
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    # Get Reddit data if available
    reddit_posts = []
    if reddit_scraper:
        try:
            from scrapers.reddit_hype_analyzer import RedditHypeAnalyzer
            analyzer = RedditHypeAnalyzer()
            reddit_data = analyzer.analyze_reddit_hype(limit=100)
            
            # Filter for this ticker
            for t, data in reddit_data.items():
                if t == ticker.upper():
                    reddit_posts = data.get('posts', [])
                    break
        except:
            pass
    
    # Run comprehensive analysis
    analyzer = ComprehensiveTickerAnalyzer()
    result = analyzer.analyze_ticker(ticker.upper(), matching, reddit_posts)
    
    # Store in Supabase via queue (non-blocking)
    if job_queue:
        try:
            await job_queue.add_job('risk_analysis', {
                'ticker': ticker.upper(),
                'analysis': result
            })
            logger.info(f"📥 Queued analysis for {ticker}")
        except Exception as e:
            logger.error(f"Error queuing analysis: {e}")
    
    return result


@app.get("/smart-alerts")
async def get_smart_alerts(min_confidence: int = 70):
    """
    🚨 Smart Alerts with Quality Controls
    Returns only high-confidence alerts with cooldown management
    States: ALERT / NEEDS_REVIEW / SUPPRESSED
    """
    if not scraper or not scraper.messages:
        return {
            "alerts": [],
            "needs_review": [],
            "suppressed": [],
            "summary": {
                "total_alerts": 0,
                "needs_review": 0,
                "suppressed": 0
            },
            "timestamp": datetime.now().isoformat(),
            "message": "No data available - Telegram loading or no messages yet"
        }
    
    from core.alert_quality_control import alert_controller
    from core.comprehensive_analyzer import ComprehensiveTickerAnalyzer
    
    analyzer = ComprehensiveTickerAnalyzer()
    all_tickers = list(scraper.get_all_tickers().keys())[:20]
    
    alerts = []
    needs_review = []
    suppressed = []
    
    for ticker in all_tickers:
        matching = [m for m in scraper.messages if ticker in m.get('tickers', [])]
        if not matching:
            continue
        
        # Analyze ticker
        analysis = analyzer.analyze_ticker(ticker, matching, [])
        risk_score = analysis['risk_assessment']['score']
        risk_breakdown = analysis['risk_breakdown']
        
        # Calculate confidence
        confidence_data = alert_controller.calculate_confidence(risk_breakdown)
        confidence = confidence_data['confidence_score']
        
        # Check if should alert
        decision = alert_controller.should_alert(ticker, risk_score, confidence)
        
        alert_item = {
            'ticker': ticker,
            'risk_score': risk_score,
            'confidence': confidence,
            'state': decision['state'],
            'reason': decision['reason'],
            'signal_distribution': confidence_data['signal_distribution'],
            'agreement_level': confidence_data['agreement_level']
        }
        
        if decision['state'] == 'ALERT':
            alerts.append(alert_item)
        elif decision['state'] == 'NEEDS_REVIEW':
            needs_review.append(alert_item)
        elif decision['state'] == 'SUPPRESSED':
            alert_item['next_alert_in'] = decision.get('next_alert_in', 0)
            alert_item['suppressed_count'] = decision.get('suppressed_count', 0)
            suppressed.append(alert_item)
    
    return {
        'alerts': sorted(alerts, key=lambda x: x['risk_score'], reverse=True),
        'needs_review': sorted(needs_review, key=lambda x: x['risk_score'], reverse=True),
        'suppressed': suppressed,
        'summary': {
            'total_alerts': len(alerts),
            'needs_review': len(needs_review),
            'suppressed': len(suppressed)
        },
        'timestamp': datetime.now().isoformat()
    }


@app.get("/alert-status/{ticker}")
async def get_alert_status(ticker: str):
    """
    🔔 Alert Status for Specific Ticker
    Shows cooldown status, confidence, and alert decision
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    from core.alert_quality_control import alert_controller
    from core.comprehensive_analyzer import ComprehensiveTickerAnalyzer
    
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    # Get analysis
    analyzer = ComprehensiveTickerAnalyzer()
    analysis = analyzer.analyze_ticker(ticker.upper(), matching, [])
    
    # Calculate confidence
    confidence_data = alert_controller.calculate_confidence(analysis['risk_breakdown'])
    
    # Get alert decision
    decision = alert_controller.should_alert(
        ticker.upper(),
        analysis['risk_assessment']['score'],
        confidence_data['confidence_score']
    )
    
    # Get cooldown status
    cooldown_status = alert_controller.get_alert_status(ticker.upper())
    
    return {
        'ticker': ticker.upper(),
        'risk_score': analysis['risk_assessment']['score'],
        'confidence': confidence_data,
        'alert_decision': decision,
        'cooldown_status': cooldown_status,
        'timestamp': datetime.now().isoformat()
    }


@app.get("/alert-statistics")
async def get_alert_statistics():
    """
    📊 Alert System Statistics
    Shows cooldown status, suppression counts, system health
    """
    from core.alert_quality_control import alert_controller
    
    stats = alert_controller.get_statistics()
    
    return {
        'statistics': stats,
        'timestamp': datetime.now().isoformat()
    }


@app.post("/reset-cooldown/{ticker}")
async def reset_cooldown(ticker: str):
    """
    🔄 Reset Alert Cooldown for Ticker
    Manually reset cooldown to allow immediate alert
    """
    from core.alert_quality_control import alert_controller
    
    alert_controller.reset_cooldown(ticker.upper())
    
    return {
        'ticker': ticker.upper(),
        'status': 'cooldown_reset',
        'message': f'Cooldown reset for {ticker.upper()}, can alert immediately',
        'timestamp': datetime.now().isoformat()
    }


@app.get("/calibration-status")
async def get_calibration_status():
    """
    🎯 Risk Score Calibration Status
    Shows current weights and validation against known cases
    """
    from core.risk_calibrator import risk_calibrator
    
    validation = risk_calibrator.validate_calibration()
    
    return {
        'calibration': {
            'accuracy': validation['accuracy'],
            'correct': validation['correct'],
            'total': validation['total'],
            'weights': validation['weights_used']
        },
        'validation_results': validation['results'],
        'timestamp': datetime.now().isoformat()
    }


@app.get("/evidence/{ticker}")
async def get_evidence_card(ticker: str):
    """
    📊 Evidence-First Explainability (Judge-Friendly)
    Returns comprehensive evidence card with all supporting proof:
    - Top matched triggers (3-5)
    - Activity metrics (#messages, #channels, time window)
    - Mention burst factor
    - Volume anomaly score
    - Bot coordination proof
    - Official filing verification
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    # Get comprehensive analysis
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    # Get all analysis components
    from core.comprehensive_analyzer import ComprehensiveTickerAnalyzer
    from core.evidence_builder import evidence_builder
    from core.mention_burst_detector import burst_detector
    
    analyzer = ComprehensiveTickerAnalyzer()
    analysis = analyzer.analyze_ticker(ticker.upper(), matching, [])
    
    # Add burst detection
    burst_data = burst_detector.detect_burst(ticker.upper())
    analysis['mention_burst'] = burst_data
    
    # Add bot activity
    bot_data = risk_analyzer.detect_bot_activity(ticker.upper(), matching)
    analysis['bot_activity'] = bot_data
    
    # Build evidence card
    evidence = evidence_builder.build_evidence_card(ticker.upper(), analysis)
    
    return evidence


@app.get("/why-risky/{ticker}")
async def explain_risk(ticker: str):
    """
    💡 AI-Generated Risk Explanation
    Natural language "Why" tooltip for risk indicators
    """
    if not scraper:
        raise HTTPException(status_code=503, detail="No data available")
    
    matching = [m for m in scraper.messages if ticker.upper() in m.get('tickers', [])]
    if not matching:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")
    
    # Get all risk components
    intelligence = IntelligenceEngine()
    msg_dicts = [{'text': m.get('text', ''), 'date': m.get('date')} for m in matching]
    intensity = intelligence.calculate_hype_intensity(ticker.upper(), msg_dicts)
    
    anomaly_data = risk_analyzer.detect_volume_anomaly(ticker.upper())
    bot_data = risk_analyzer.detect_bot_activity(ticker.upper(), matching)
    
    risk_data = risk_analyzer.calculate_unified_risk_score(
        ticker.upper(),
        intensity['hype_score'],
        intensity['metrics'].get('trigger_density', 0) * 10,
        anomaly_data,
        bot_data
    )
    
    # Extract fraud triggers
    fraud_triggers = []
    for msg in matching:
        analysis = intelligence.analyze_message(
            msg.get('text', ''),
            [ticker.upper()],
            msg.get('date', datetime.now())
        )
        fraud_triggers.extend(analysis.get('fraud_triggers', []))
    
    explanation = risk_analyzer.generate_risk_explanation(
        ticker.upper(),
        risk_data,
        anomaly_data,
        bot_data,
        list(set(fraud_triggers))
    )
    
    return {
        "ticker": ticker.upper(),
        "explanation": explanation,
        "risk_score": risk_data['risk_score'],
        "color_indicator": risk_data['color_indicator'],
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# DATA SOURCE APIs
# ============================================================================

@app.get("/reddit-hype")
async def get_reddit_hype(limit: int = 10):
    """
    📱 Reddit Hype Analysis from RUMOR SOURCE
    🔴 Analyzes: Reddit speculation (UNTRUSTED)
    Most hyped stocks on Indian stock subreddits
    """
    from scrapers.reddit_hype_analyzer import RedditHypeAnalyzer
    analyzer = RedditHypeAnalyzer()
    top_hyped = analyzer.get_top_hyped(limit=limit)
    return {
        "top_hyped_stocks": top_hyped,
        "count": len(top_hyped),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/youtube-hype")
async def get_youtube_hype(limit: int = 10):
    """
    📺 YouTube Hype Analysis from RUMOR SOURCE
    🔴 Analyzes: YouTube video titles/comments (UNTRUSTED)
    Most hyped stocks on Indian stock YouTube channels
    """
    if not youtube_scraper:
        return {"error": "YouTube scraper not initialized", "top_hyped_stocks": []}
    
    try:
        analysis = youtube_scraper.analyze_youtube_hype()
        top_stocks = []
        
        for ticker, data in list(analysis['top_hyped_stocks'].items())[:limit]:
            top_stocks.append({
                'ticker': ticker,
                'mentions': data['mentions'],
                'hype_intensity': data['hype_intensity'],
                'avg_hype_score': data['avg_hype_score'],
                'sample_videos': data['videos'][:3]
            })
        
        return {
            'top_hyped_stocks': top_stocks,
            'count': len(top_stocks),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing YouTube: {e}")
        return {"error": str(e), "top_hyped_stocks": []}


@app.get("/tickers")
async def get_tickers():
    """
    📋 All Monitored Tickers (from DATABASE)
    Returns tickers from Supabase, not in-memory
    """
    if not supabase_db:
        return {"error": "Database not connected"}
    
    # Query database for all tickers
    result = supabase_db.client.table('rumor_sources')\
        .select('tickers')\
        .execute()
    
    # Count ticker mentions
    ticker_counts = {}
    for row in result.data:
        for ticker in row.get('tickers', []):
            ticker_counts[ticker] = ticker_counts.get(ticker, 0) + 1
    
    # Sort by count
    sorted_tickers = dict(sorted(ticker_counts.items(), key=lambda x: x[1], reverse=True))
    
    return {
        "tickers": sorted_tickers,
        "total_unique": len(sorted_tickers),
        "source": "database"
    }


# ============================================================================
# UTILITY APIs
# ============================================================================

@app.get("/health")
async def health():
    """System health check"""
    return {
        "status": "healthy",
        "uptime_seconds": (datetime.now() - startup_time).total_seconds() if startup_time else 0,
        "messages_count": len(scraper.messages) if scraper else 0,
        "telegram_active": scraper is not None,
        "reddit_active": reddit_scraper is not None
    }


@app.get("/refresh")
async def refresh_messages():
    """Manually refresh Telegram messages"""
    if not scraper:
        raise HTTPException(status_code=503, detail="Telegram not configured")
    
    await scraper.fetch_messages(limit=100)
    return {
        "status": "refreshed",
        "messages_count": len(scraper.messages),
        "tickers_found": scraper.get_all_tickers()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
