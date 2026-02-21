# 🚀 Quick Start Guide

## Start Backend + Database

### Option 1: One Command (Windows)
```bash
start.bat
```

### Option 2: Manual Steps

**Step 1: Populate Database**
```bash
python tests/populate_db.py
```
This scrapes Telegram/Reddit/YouTube and stores in Supabase.

**Step 2: Start Backend**
```bash
python main.py
```
Backend runs at: http://localhost:8080

---

## Test API

### 1. Health Check
```bash
curl http://localhost:8080/health
```

### 2. Get Ticker Analysis
```bash
curl http://localhost:8080/ticker-analysis/YESBANK
```

### 3. View API Docs
Open browser: http://localhost:8080/docs

---

## View Database

1. Go to Supabase Dashboard
2. Click **Table Editor**
3. View tables:
   - `rumor_sources` - Telegram/Reddit/YouTube data
   - `risk_analysis` - Risk scores and analysis

---

## What's Running?

✅ **Backend (FastAPI)**: http://localhost:8080
✅ **Database (Supabase)**: Cloud-hosted
✅ **Data Sources**: 
   - 🔴 Telegram (RUMOR SOURCE)
   - 🔴 Reddit (RUMOR SOURCE)
   - 🔴 YouTube (RUMOR SOURCE)
   - ✅ yfinance (VERIFICATION SOURCE)

---

## Stop Backend

Press `Ctrl+C` in terminal
