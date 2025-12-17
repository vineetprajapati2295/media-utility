# Free Deployment Guide

## ⚠️ Important: Netlify Limitation

**Netlify is for static sites only.** Your Flask backend needs a different hosting solution.

## ✅ Best Free Options

### Option 1: Render.com (Recommended - Easiest)

**Free tier includes:**
- 750 hours/month (enough for 24/7)
- Automatic deployments from GitHub
- Free SSL
- Custom domains

#### Steps:

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/media-utility.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Name**: media-utility
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt && pip install gunicorn`
     - **Start Command**: `gunicorn -c gunicorn_config.py backend.app:app`
     - **Plan**: Free
   - Add Environment Variables:
     ```
     FLASK_ENV=production
     FLASK_DEBUG=False
     SECRET_KEY=your-secret-key-here
     PORT=5000
     ```
   - Click "Create Web Service"

3. **Get Your URL:**
   - Render gives you: `https://media-utility.onrender.com`
   - Update frontend `app.js`:
     ```javascript
     const API_BASE_URL = 'https://media-utility.onrender.com/api';
     ```

4. **Done!** Your site is live.

---

### Option 2: Railway.app (Alternative)

**Free tier:**
- $5 credit/month (usually enough for small apps)
- Easy deployment

#### Steps:

1. **Push to GitHub** (same as above)

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Railway auto-detects Python
   - Add environment variables (same as Render)
   - Deploy!

3. **Get URL and update frontend**

---

### Option 3: Fly.io (Another Option)

**Free tier:**
- 3 shared VMs
- Good for Flask apps

#### Steps:

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Deploy:**
   ```bash
   fly launch
   ```

4. **Follow prompts**

---

### Option 4: Split Deployment (Netlify Frontend + Backend Elsewhere)

If you really want to use Netlify:

1. **Deploy Backend** on Render/Railway (free)
2. **Deploy Frontend** on Netlify (free):
   - Update `frontend/app.js` with backend URL
   - Push frontend folder to GitHub
   - Connect to Netlify
   - Deploy!

---

## Quick Start: Render.com (Recommended)

### Step 1: Prepare for GitHub

```bash
# Make sure .gitignore is good
cat .gitignore

# Initialize git (if not done)
git init
git add .
git commit -m "Ready for deployment"
```

### Step 2: Push to GitHub

```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/media-utility.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to https://render.com
2. Sign up (use GitHub)
3. "New +" → "Web Service"
4. Connect repo
5. Settings:
   - **Name**: `media-utility` (or your choice)
   - **Region**: Choose closest
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && pip install gunicorn`
   - **Start Command**: `gunicorn -c gunicorn_config.py backend.app:app`
   - **Plan**: Free

6. **Environment Variables:**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=change-this-to-random-string
   PORT=5000
   MAX_REQUESTS_PER_HOUR=10
   MAX_DOWNLOAD_SIZE_MB=500
   ```

7. Click "Create Web Service"

8. Wait 5-10 minutes for first deployment

### Step 4: Update Frontend

Once deployed, you'll get a URL like: `https://media-utility.onrender.com`

Update `frontend/app.js`:
```javascript
// Change this line:
const API_BASE_URL = 'http://127.0.0.1:5000/api';

// To:
const API_BASE_URL = 'https://media-utility.onrender.com/api';
```

### Step 5: Deploy Frontend (Optional)

**Option A: Keep frontend on Render** (served by Flask - already done!)

**Option B: Deploy frontend separately on Netlify:**

1. Create `netlify.toml`:
   ```toml
   [build]
     publish = "frontend"
   
   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

2. Push to GitHub

3. Connect to Netlify:
   - Go to https://netlify.com
   - "Add new site" → "Import from Git"
   - Select repo
   - Build settings:
     - Build command: (leave empty)
     - Publish directory: `frontend`
   - Deploy!

---

## Environment Variables Reference

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-random-secret-key-here
PORT=5000
MAX_REQUESTS_PER_HOUR=10
MAX_DOWNLOAD_SIZE_MB=500
```

Generate SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Troubleshooting

### Build Fails
- Check build logs on Render
- Ensure `requirements.txt` is correct
- Make sure `gunicorn` is in requirements or install in build command

### App Crashes
- Check logs on Render dashboard
- Verify environment variables
- Check PORT is set correctly

### CORS Errors
- Backend URL must match frontend API_BASE_URL
- Check CORS is enabled in `backend/app.py`

### Slow First Request
- Render free tier spins down after inactivity
- First request after 15min idle takes ~30s to wake up
- This is normal for free tier

---

## Custom Domain (Optional)

1. On Render dashboard → Settings → Custom Domain
2. Add your domain
3. Follow DNS instructions
4. SSL auto-provisioned

---

## Cost Comparison

| Service | Free Tier | Best For |
|---------|-----------|----------|
| **Render** | 750 hrs/month | Easiest, best docs |
| **Railway** | $5 credit/month | Simple, fast |
| **Fly.io** | 3 VMs | More control |
| **Netlify** | Static only | Frontend only |

**Recommendation: Use Render.com** - easiest and most reliable for Flask apps.

---

## Next Steps After Deployment

1. ✅ Get your live URL
2. ✅ Update frontend API URL
3. ✅ Test the site
4. ✅ Get Site ID from ad networks
5. ✅ Configure ads
6. ✅ Add custom domain (optional)

Your site will be live at: `https://your-app.onrender.com`

