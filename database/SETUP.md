# Supabase Setup Guide

## Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Sign up / Login
3. Click "New Project"
4. Name: `pumpwatch`
5. Database Password: (save this)
6. Region: Choose closest to you
7. Click "Create new project"

## Step 2: Get Connection Details
1. Go to Project Settings → API
2. Copy:
   - Project URL (e.g., https://xxxxx.supabase.co)
   - anon/public key

## Step 3: Add to .env
```env
# Add these to your .env file
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_anon_key_here
```

## Step 4: Create Tables
1. Go to SQL Editor in Supabase dashboard
2. Copy contents from `database/schema.sql`
3. Paste and click "Run"
4. Tables created: `rumor_sources`, `risk_analysis`

## Step 5: Install Package
```bash
pip install supabase
```

## Step 6: Test Connection
```bash
python tests/test_supabase.py
```

## Why Connection String?
✅ **Best for this project:**
- Direct database access
- Fast queries
- No API rate limits
- Full SQL control
- Works with Python easily

❌ **Not needed:**
- App Frameworks (for web apps)
- Mobile Frameworks (for mobile apps)
- ORMs (we use direct SQL)
- MCP (for complex workflows)

## Usage in Code
```python
from core.supabase_db import SupabaseDB

db = SupabaseDB()

# Store Telegram message
db.store_telegram_message(message)

# Store risk analysis
db.store_risk_analysis(ticker, analysis)

# Query high risk stocks
high_risk = db.get_high_risk_tickers(min_risk=70)
```
