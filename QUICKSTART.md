# Quick Start Guide

## 🚀 Getting Started (5 Minutes)

### 1. Setup (First Time Only)
```bash
cd /home/vineet/yout
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up the project

**Or manually:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Start server
./run_dev.sh
# OR
python3 -m backend.app
```

You should see:
```
╔═══════════════════════════════════════════════════════╗
║   Media Utility Platform - Backend Server             ║
╠═══════════════════════════════════════════════════════╣
║   Server running at: http://127.0.0.1:5000            ║
╚═══════════════════════════════════════════════════════╝
```

### 3. Test the API (Optional)
Open a new terminal and run:
```bash
python3 backend/test_api.py
```

Or test manually:
```bash
curl http://127.0.0.1:5000/api/health
```

### 4. Stop the Server
Press `Ctrl+C` in the terminal where the server is running.

---

## 📁 Project Structure

```
yout/
├── backend/
│   ├── app.py              # Main Flask server
│   ├── config.py           # Configuration
│   ├── download_service.py  # Download logic
│   └── test_api.py         # Test script
├── frontend/               # (Will build in Phase 3)
├── downloads/              # (Created automatically)
└── requirements.txt        # Python dependencies
```

---

## 🔧 Common Issues

**Issue:** `ModuleNotFoundError: No module named 'backend'`
- **Fix:** Run from project root: `python3 backend/app.py`

**Issue:** `Port 5000 already in use`
- **Fix:** Change `FLASK_PORT` in `backend/config.py` or kill the process

**Issue:** `yt-dlp not found`
- **Fix:** `pip3 install yt-dlp`

---

## 📚 Documentation

- **Phase 1:** `ARCHITECTURE.md` - Project structure
- **Phase 2:** `PHASE2_GUIDE.md` - Backend API details
- **Full Guide:** `README.md` - Overview

---

## ✅ Next Steps

Phase 2 is complete! The backend API is ready.

**To continue:** Say "Yes, continue" to proceed to Phase 3 (Frontend UI).

