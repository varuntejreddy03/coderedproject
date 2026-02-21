# 🔧 Troubleshooting: Why Tests Return 404

## Problem
When you send a message to Telegram like:
```
YESBANK pakka upper circuit sure shot multibagger. Guaranteed 100%
```

The ticker-specific endpoints return 404:
- `/reality-check/YESBANK` → 404
- `/hype-intensity/YESBANK` → 404
- `/risk-score/YESBANK` → 404
- `/bot-activity/YESBANK` → 404
- `/why-risky/YESBANK` → 404

## Root Cause
The API only fetches Telegram messages **once during startup**. After that, it never refreshes unless you:
1. Restart the API
2. Call the `/refresh` endpoint

## Solutions

### Option 1: Call `/refresh` endpoint (Recommended)
```bash
# After sending a message to Telegram, refresh the API
curl http://localhost:8080/refresh
```

The updated `test_api.py` now automatically calls `/refresh` before running tests.

### Option 2: Restart the API
```bash
# Stop the API (Ctrl+C)
# Start it again
python main.py
```

### Option 3: Use the updated test script
```bash
# The new test_api.py automatically refreshes messages
python test_api.py
```

## How It Works

1. **Ticker Extraction**: ✅ Working correctly
   - Regex finds: `YESBANK`, `PAKKA`, `UPPER`, `CIRCUIT`, etc.
   - Filters to only: `YESBANK` (from TARGET_STOCKS)

2. **Message Storage**: ✅ Working correctly
   - Messages stored with `tickers: ['YESBANK']`
   - Fraud score calculated: `5` (pakka, upper circuit, sure shot, guaranteed, 100%)

3. **Endpoint Lookup**: ❌ Was failing
   - Endpoints search: `[m for m in scraper.messages if ticker in m['tickers']]`
   - If no messages fetched → empty list → 404

## Verification

Run this to verify ticker extraction:
```bash
python debug_ticker.py
```

Expected output:
```
Text: YESBANK pakka upper circuit sure shot multibagger. Guaranteed 100%
All caps words: ['YESBANK', 'PAKKA', 'UPPER', 'CIRCUIT', 'SURE', 'SHOT', 'GUARANTEED']
Matched tickers: ['YESBANK']
Result: ['YESBANK']
```

## Changes Made

### 1. Fixed ticker extraction (simple_telegram.py)
```python
# Before: Case-sensitive regex
tickers = re.findall(r'\b[A-Z]{2,10}\b', text)

# After: Convert to uppercase first
text_upper = text.upper()
tickers = re.findall(r'\b[A-Z]{2,10}\b', text_upper)
```

### 2. Added /refresh endpoint (main.py)
```python
@app.get("/refresh")
async def refresh_messages():
    """Manually refresh Telegram messages"""
    await scraper.fetch_messages(limit=100)
    return {
        "status": "refreshed",
        "messages_count": len(scraper.messages),
        "tickers_found": scraper.get_all_tickers()
    }
```

### 3. Updated test script (test_api.py)
- Now calls `/refresh` before running tests
- Ensures latest messages are fetched

## Testing Workflow

1. **Send message to Telegram**:
   ```
   YESBANK pakka upper circuit sure shot multibagger. Guaranteed 100%
   ```

2. **Run tests** (auto-refreshes):
   ```bash
   python test_api.py
   ```

3. **Verify results**:
   - All ticker-specific endpoints should return 200 OK
   - No more 404 errors

## Expected Test Results

After refresh:
```
✅ Refresh Messages: 2000ms
✅ Health Check: 50ms
✅ Fraud Alerts: 100ms
✅ Reality Check (YESBANK): 150ms
✅ Hype Intensity (YESBANK): 120ms
✅ Risk Score (YESBANK): 180ms
✅ Bot Activity (YESBANK): 90ms
✅ Why Risky (YESBANK): 200ms
```

## Notes

- **TARGET_STOCKS**: Only `YESBANK`, `TCS`, `RELIANCE`, `INFY` are tracked
- **Fraud Keywords**: 10+ patterns including Hinglish (pakka, zaroor, etc.)
- **Message Limit**: Fetches last 100 messages on refresh
- **Storage**: In-memory (lost on restart)
