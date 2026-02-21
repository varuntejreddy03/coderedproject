"""
FastAPI Integration for Production Telegram Scraper
Proper lifecycle management with startup/shutdown
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from scrapers.production_telegram import ProductionTelegramScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# Global scraper instance
scraper = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan with proper Telegram setup"""
    global scraper
    
    logger.info("🚀 Starting PumpWatch")
    
    # Get credentials
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    channels = [c.strip() for c in os.getenv("CHANNELS", "").split(",") if c.strip()]
    
    if not channels:
        logger.warning("⚠️ No channels configured")
        yield
        return
    
    # Initialize scraper
    scraper = ProductionTelegramScraper(api_id, api_hash, channels)
    
    # Connect
    connected = await scraper.connect()
    if not connected:
        logger.error("❌ Failed to connect to Telegram")
        yield
        return
    
    # Initial fetch
    logger.info("📥 Fetching initial messages...")
    await scraper.fetch_messages(limit=50)
    logger.info(f"✅ Loaded {len(scraper.messages)} messages")
    
    # Start background polling (non-blocking)
    async def on_new_message(message):
        """Callback for new messages"""
        logger.info(f"📨 New message: {message['tickers']}")
        # Add to database here if needed
    
    # Start polling in background
    scraper.polling_task = asyncio.create_task(
        scraper.start_polling(callback=on_new_message, interval=30)
    )
    logger.info("✅ Background polling started (30s interval)")
    
    logger.info("✅ Backend ready at http://localhost:8080")
    
    yield
    
    # Cleanup on shutdown
    logger.info("🛑 Shutting down...")
    await scraper.disconnect()
    logger.info("✅ Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="PumpWatch",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example endpoints
@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "telegram_active": scraper is not None,
        "messages_count": len(scraper.messages) if scraper else 0
    }

@app.get("/tickers")
async def get_tickers():
    """Get all monitored tickers"""
    if not scraper:
        return {"tickers": {}, "total": 0}
    
    tickers = scraper.get_all_tickers()
    return {
        "tickers": tickers,
        "total": len(tickers)
    }

@app.get("/messages")
async def get_messages(limit: int = 50):
    """Get recent messages"""
    if not scraper:
        return {"messages": [], "total": 0}
    
    return {
        "messages": scraper.messages[-limit:],
        "total": len(scraper.messages)
    }

@app.post("/refresh")
async def refresh_messages():
    """Manually refresh messages"""
    if not scraper:
        return {"error": "Scraper not initialized"}
    
    await scraper.fetch_messages(limit=50)
    return {
        "status": "refreshed",
        "messages_count": len(scraper.messages)
    }

if __name__ == "__main__":
    import uvicorn
    # IMPORTANT: Use single worker only
    uvicorn.run(app, host="0.0.0.0", port=8080, workers=1)
