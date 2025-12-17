# Quick Deployment Guide - Render.com (5 Minutes)

## Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/media-utility.git
git push -u origin main
```

## Step 2: Deploy on Render

1. Go to **https://render.com**
2. Sign up with **GitHub**
3. Click **"New +"** → **"Web Service"**
4. Connect your repository
5. Fill in:
   - **Name**: `media-utility`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -c gunicorn_config.py backend.app:app`
   - **Plan**: **Free**
6. Add Environment Variables:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=generate-random-string-here
   ```
7. Click **"Create Web Service"**
8. Wait 5-10 minutes

## Step 3: Update Frontend

Once deployed, you'll get: `https://media-utility.onrender.com`

Edit `frontend/config.js`:
```javascript
const PROD_API_URL = 'https://media-utility.onrender.com/api';
```

Or update `frontend/app.js` directly:
```javascript
const API_BASE_URL = 'https://media-utility.onrender.com/api';
```

## Step 4: Redeploy Frontend (if separate)

If deploying frontend separately:
- Push updated frontend files
- Render will auto-redeploy

## Done! 🎉

Your site is live at: `https://media-utility.onrender.com`

**Note:** Free tier spins down after 15min idle. First request takes ~30s to wake up.

