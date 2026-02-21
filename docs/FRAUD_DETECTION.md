# 🚨 Fraud Detection Setup Guide

## 🎯 Best Ways to Find Suspicious Channels

### ✅ Option 1: Automated Channel Discovery (RECOMMENDED)

Use Telethon's built-in search to auto-discover channels:

```python
# Add to telegram_scraper.py
async def search_channels(self, query: str, limit: int = 20):
    """Search for public channels by keyword"""
    from telethon.tl.functions.contacts import SearchRequest
    result = await self.client(SearchRequest(q=query, limit=limit))
    return [chat.username for chat in result.chats if hasattr(chat, 'username') and chat.username]
```

Search queries:
- "stock tips" / "intraday" / "multibagger" / "BTST"
- "penny stock" / "operator stock"
- "Nifty option" / "BankNifty calls"
- "share bazaar" / "stock tips hindi"

### ✅ Option 2: Monitor Public Channel Directories

**Telegram Channel Aggregators:**
- https://telegramchannels.me/list/business (India business channels)
- https:// tchannels.me/search?q=stock+tips
- https://tgstat.com (Telegram analytics)

Filter by:
- Country: India
- Category: Finance/Trading
- Subscribers: 1K-50K (sweet spot for pump groups)

### ✅ Option 3: Scrape from Known Pump Groups

Many pump groups share "sister channels" in their descriptions:

```python
# Get channel description and extract @mentions
async def get_related_channels(self, channel: str):
    entity = await self.client.get_entity(channel)
    description = entity.about or ""
    return re.findall(r'@(\w+)', description)
```

### ✅ Option 4: Use SEBI Complaint Database

SEBI publishes lists of unregistered advisors:
- https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=40
- Cross-reference names with Telegram search

### ✅ Option 5: Reddit/Twitter Intelligence

Monitor:
- r/IndianStockMarket (users report scam channels)
- Twitter: Search "telegram stock tips scam"
- Extract channel usernames from complaints

### 🚀 Quick Start (Automated)

**Step 1:** Use built-in search endpoint (add to main.py):
```python
@app.get("/discover-channels")
async def discover_channels(query: str = "stock tips"):
    channels = await scraper.search_channels(query)
    return {"query": query, "found_channels": channels}
```

**Step 2:** Call API:
```bash
curl "http://localhost:8000/discover-channels?query=intraday+stock+tips"
```

**Step 3:** Auto-add to monitoring list

### ⚡ Recommended Approach

**Hybrid Strategy:**
1. Start with 5-10 known suspicious channels (manual)
2. Use Option 3 to discover their network
3. Use Option 1 to search by fraud keywords
4. Cross-reference with SEBI complaints (Option 4)
5. Continuously expand based on fraud_alerts data

## How to Add Channels

1. Search for channels using above terms in Telegram
2. Join the channels (some may require approval)
3. Get the channel username (e.g., @channelname)
4. Add to `.env` file:
   ```
   CHANNELS=channel1,channel2,channel3
   ```

## Fraud Detection Features

### New API Endpoint
```
GET /fraud-alerts?min_risk=2
```

Returns:
- High-risk messages with fraud keywords
- Total alert count
- Top 10 suspicious tickers being pumped

### Fraud Keywords Detected
- guaranteed, sure shot, confirmed, 100%, risk free
- upper circuit, lower circuit, operator, big move
- multibagger, jackpot, bumper, target
- btst, intraday call, premium tip
- urgent, last chance, don't miss

### Risk Scoring
- Each fraud keyword = +1 risk score
- Messages with risk_score >= 2 are flagged
- Higher score = more suspicious

## Example Usage

1. Monitor suspicious channels
2. Call `/fraud-alerts` to get pump attempts
3. Compare with official channels (NSE, BSE, SEBI)
4. Identify coordinated ticker mentions
5. Detect fake news patterns

## ⚠️ Legal Disclaimer

This tool is for:
- Educational purposes
- Research on misinformation
- Fraud awareness and detection
- Protecting retail investors

NOT for:
- Market manipulation
- Insider trading
- Illegal activities

Monitor responsibly and report suspicious activity to SEBI.
