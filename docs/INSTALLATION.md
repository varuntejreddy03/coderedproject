# 🚀 Installation Guide - Windows

## Step-by-Step Setup

### 1️⃣ Create Virtual Environment

```bash
# Navigate to project folder
cd C:\Users\varun\Downloads\nmims24hr

# Create virtual environment
python -m venv venv
```

### 2️⃣ Activate Virtual Environment

**Windows Command Prompt:**
```bash
venv\Scripts\activate
```

**Windows PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

**Git Bash (Windows):**
```bash
source venv/Scripts/activate
```

You'll see `(venv)` in your terminal when activated.

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- fastapi
- uvicorn
- telethon
- python-dotenv
- pydantic
- requests
- beautifulsoup4
- snscrape

### 4️⃣ Configure Environment

Your `.env` file is already set up with Telegram credentials!

### 5️⃣ Run the Application

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

### 6️⃣ Test the API

Open browser:
```
http://localhost:8000/docs
```

Or test with curl:
```bash
curl http://localhost:8000/health
```

---

## 🔧 Troubleshooting

### Issue: "python not found"
**Solution:**
```bash
py -m venv venv
```

### Issue: PowerShell execution policy error
**Solution:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: pip install fails
**Solution:**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Telethon asks for phone number
**Solution:** This is normal! Enter your phone number for first-time authentication.

---

## 📦 Quick Commands Reference

```bash
# Activate venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run app
python main.py

# Deactivate venv
deactivate
```

---

## ✅ Verify Installation

After running `python main.py`, you should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Starting PumpWatch backend...
INFO:     Telegram client connected
INFO:     Reddit scraper initialized (public API)
INFO:     Twitter scraper initialized (snscrape)
INFO:     Fetching initial messages...
INFO:     Background polling started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🎯 Next Steps

1. Open http://localhost:8000/docs
2. Test `/health` endpoint
3. Test `/messages` endpoint
4. Test `/fraud-alerts` endpoint
5. Test `/hype-intensity/YESBANK` endpoint

Your PumpWatch backend is ready! 🚀
