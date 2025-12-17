# GitHub Repository Setup

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `media-utility` (or your choice)
3. Description: "Media Utility Platform - Video Downloader"
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 2: Update Remote URL

After creating the repo, GitHub will show you the URL. It will look like:
```
https://github.com/YOUR_USERNAME/media-utility.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

Then run:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/media-utility.git
git push -u origin main
```

## Step 3: Verify

```bash
git remote -v
```

Should show your GitHub URL.

## Alternative: Using SSH

If you prefer SSH:
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/media-utility.git
```

