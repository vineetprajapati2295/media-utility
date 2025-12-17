# Troubleshooting Guide

## Validate Button Not Working

### Issue: Button does nothing when clicked

**Check 1: Browser Console**
1. Open browser (F12 or Right-click → Inspect)
2. Go to "Console" tab
3. Look for errors (red text)
4. Check what API_BASE_URL is set to

**Check 2: API URL Configuration**

If you see errors like "Failed to fetch" or "NetworkError":

1. **If frontend is served from Render backend** (same URL):
   - Should work automatically
   - API_BASE_URL should be: `https://your-app.onrender.com/api`
   - Check browser console to confirm

2. **If frontend is separate** (different URL):
   - Edit `frontend/config.js`
   - Update `PROD_API_URL` with your actual Render URL:
     ```javascript
     const PROD_API_URL = 'https://your-actual-app.onrender.com/api';
     ```

**Check 3: CORS Issues**

If you see CORS errors:
- Backend already has CORS enabled
- If still having issues, check Render logs

**Check 4: Backend is Running**

1. Go to your Render dashboard
2. Check if service is "Live" (green)
3. Check logs for errors
4. Test API directly:
   ```bash
   curl https://your-app.onrender.com/api/health
   ```

**Check 5: Network Tab**

1. Open browser DevTools (F12)
2. Go to "Network" tab
3. Click Validate button
4. Look for the `/api/validate` request
5. Check:
   - Status code (should be 200)
   - Request URL (should be correct)
   - Response (should be JSON)

### Common Errors

**Error: "Failed to fetch"**
- Backend is down or URL is wrong
- Check Render dashboard
- Verify API_BASE_URL in console

**Error: "CORS policy"**
- Backend CORS should be enabled (already done)
- Check if request is going to correct URL

**Error: "404 Not Found"**
- API endpoint doesn't exist
- Check if URL path is correct: `/api/validate`

**Error: "500 Internal Server Error"**
- Backend error
- Check Render logs
- May be yt-dlp issue or missing dependencies

### Quick Fixes

1. **Clear browser cache** (Ctrl+Shift+Delete)

2. **Hard refresh** (Ctrl+F5 or Cmd+Shift+R)

3. **Check Render logs:**
   - Go to Render dashboard
   - Click on your service
   - Go to "Logs" tab
   - Look for errors

4. **Test API directly:**
   ```bash
   # Health check
   curl https://your-app.onrender.com/api/health
   
   # Validate test
   curl -X POST https://your-app.onrender.com/api/validate \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
   ```

5. **Update frontend config:**
   - Edit `frontend/config.js`
   - Set correct PROD_API_URL
   - Redeploy or refresh page

### Still Not Working?

1. **Check Render service status**
2. **Check browser console for exact error**
3. **Check Render logs for backend errors**
4. **Verify API URL in browser console:**
   ```javascript
   console.log(window.API_BASE_URL);
   ```
5. **Test API endpoint directly in browser:**
   ```
   https://your-app.onrender.com/api/health
   ```

### Debug Mode

Add this to browser console to see what's happening:
```javascript
// Check current API URL
console.log('API Base URL:', window.API_BASE_URL);

// Test health endpoint
fetch(window.API_BASE_URL.replace('/api', '/api/health'))
  .then(r => r.json())
  .then(d => console.log('Health:', d))
  .catch(e => console.error('Error:', e));
```

