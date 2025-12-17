# Phase 2: Backend API - Complete Guide

## 📚 What We Built

In Phase 2, we created a complete Flask backend API with the following components:

### Files Created/Modified:

1. **`backend/config.py`** - Configuration management
2. **`backend/download_service.py`** - yt-dlp integration and download logic
3. **`backend/app.py`** - Flask server with API endpoints
4. **`backend/test_api.py`** - Simple testing script

---

## 🏗️ Architecture Explanation

### 1. **Configuration (`config.py`)**

**Why separate config?**
- Easy to change settings without touching code
- Environment-specific settings (dev vs production)
- Security: Keep secrets out of code

**Key Settings:**
- `FLASK_PORT`: Server port (default: 5000)
- `DOWNLOADS_DIR`: Where files are saved
- `MAX_DOWNLOAD_SIZE_MB`: Size limit (default: 500MB)
- `MAX_REQUESTS_PER_HOUR`: Rate limiting (default: 10)

**How to customize:**
- Edit `config.py` directly, OR
- Use environment variables (`.env` file)

---

### 2. **Download Service (`download_service.py`)**

**Why a separate service class?**
- **Separation of concerns**: Business logic separate from API routes
- **Reusability**: Can be used by other parts of the app
- **Testability**: Easy to test download logic independently
- **Maintainability**: Changes to download logic don't affect API structure

**Key Methods:**

#### `validate_url(url)`
- Checks if URL is valid and downloadable
- Returns `(is_valid, error_message)`
- **Why validate first?** Prevents wasting time on invalid URLs

#### `get_video_info(url)`
- Gets video metadata without downloading
- Returns title, duration, formats, thumbnail
- **Why useful?** Frontend can show video info before download

#### `download_video(url, format_id, audio_only)`
- Actually downloads the video/audio
- Handles progress tracking
- Returns file path and metadata
- **Why progress hooks?** Can track download progress (Phase 4)

---

### 3. **Flask App (`app.py`)**

**What is Flask?**
- Lightweight Python web framework
- Perfect for REST APIs
- Easy to learn and deploy

**Key Concepts:**

#### **Routes (Endpoints)**
Routes define what URLs the server responds to:

```python
@app.route('/api/download', methods=['POST'])
def download():
    # This function runs when POST /api/download is called
```

**HTTP Methods:**
- `GET`: Retrieve data (safe, no side effects)
- `POST`: Create/submit data (has side effects)
- `PUT`: Update data
- `DELETE`: Delete data

#### **CORS (Cross-Origin Resource Sharing)**
```python
CORS(app)
```
**Why needed?** Frontend (port 3000) and backend (port 5000) are different origins.
Without CORS, browsers block requests between different origins.

#### **JSON Responses**
```python
return jsonify({'status': 'success', 'data': ...})
```
**Why JSON?** Standard format for API communication. Easy for frontend to parse.

---

## 🔌 API Endpoints Explained

### 1. **GET `/`** - Root
- **Purpose**: Basic server info
- **Use case**: Testing if server is running
- **Response**: `{"status": "online", ...}`

### 2. **POST `/api/validate`** - Validate URL
- **Purpose**: Check if URL is downloadable
- **Request body**: `{"url": "https://..."}`
- **Response**: 
  ```json
  {
    "valid": true,
    "message": "URL is valid",
    "video_info": {...}
  }
  ```
- **Why separate endpoint?** Frontend can validate before showing download button

### 3. **POST `/api/download`** - Download Video
- **Purpose**: Download video/audio
- **Request body**: 
  ```json
  {
    "url": "https://...",
    "format_id": "optional",
    "audio_only": false
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "filename": "video.mp4",
    "download_url": "/api/file/video.mp4"
  }
  ```
- **How it works**:
  1. Validates URL
  2. Checks rate limit
  3. Downloads using yt-dlp
  4. Returns file info

### 4. **GET `/api/file/<filename>`** - Serve File
- **Purpose**: Download the actual file
- **Security**: Only serves files from `downloads/` directory
- **Why separate?** Files can be large, better to serve separately

### 5. **GET `/api/health`** - Health Check
- **Purpose**: Check if server is healthy
- **Use case**: Monitoring, deployment checks
- **Response**: `{"status": "healthy", ...}`

---

## 🔒 Security Features

### 1. **Directory Traversal Protection**
```python
# Only allow files from downloads directory
if not str(file_path).startswith(str(DOWNLOADS_DIR)):
    return error
```
**Why?** Prevents attackers from accessing files outside downloads folder.

### 2. **Rate Limiting (Basic)**
- Limits requests per hour per IP
- Prevents abuse
- **Note**: Current implementation is basic (in-memory)
- **Production**: Use Redis or flask-limiter

### 3. **File Size Limits**
- Max download size: 500MB (configurable)
- Prevents server overload
- **Why?** Large files consume disk space and bandwidth

### 4. **URL Validation**
- Validates URLs before downloading
- Prevents invalid requests
- **Why?** Saves server resources

---

## 🐛 Common Beginner Mistakes

### 1. **Forgetting CORS**
```python
# ❌ Bad: Frontend can't connect
app = Flask(__name__)

# ✅ Good: CORS enabled
CORS(app)
```

### 2. **Not Handling Errors**
```python
# ❌ Bad: Crashes on error
result = download_service.download_video(url)

# ✅ Good: Try/except
try:
    result = download_service.download_video(url)
except Exception as e:
    return jsonify({'error': str(e)}), 500
```

### 3. **Hardcoding Paths**
```python
# ❌ Bad: Hardcoded path
file_path = "/home/user/downloads/video.mp4"

# ✅ Good: Use config
file_path = DOWNLOADS_DIR / "video.mp4"
```

### 4. **Not Validating Input**
```python
# ❌ Bad: Trusts user input
url = request.json['url']
download(url)

# ✅ Good: Validate first
url = request.json.get('url')
if not url:
    return error
is_valid, msg = validate_url(url)
```

---

## 🚀 How to Run

### Step 1: Install Dependencies
```bash
cd /home/vineet/yout
pip install -r requirements.txt
```

**What this installs:**
- `flask`: Web framework
- `flask-cors`: CORS support
- `yt-dlp`: Video downloader
- `python-dotenv`: Environment variables

### Step 2: Start the Server
```bash
cd backend
python app.py
```

**Expected output:**
```
╔═══════════════════════════════════════════════════════╗
║   Media Utility Platform - Backend Server             ║
╠═══════════════════════════════════════════════════════╣
║   Server running at: http://127.0.0.1:5000            ║
║   Environment: development                            ║
║   Debug mode: True                                    ║
╚═══════════════════════════════════════════════════════╝
```

### Step 3: Test the API

**Option A: Using test script**
```bash
python backend/test_api.py
```

**Option B: Using curl**
```bash
# Health check
curl http://127.0.0.1:5000/api/health

# Validate URL
curl -X POST http://127.0.0.1:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

**Option C: Using browser**
- Open: `http://127.0.0.1:5000/api/health`

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'backend'"
**Solution:** Run from project root, not from backend directory:
```bash
cd /home/vineet/yout
python backend/app.py
```

### Problem: "Port 5000 already in use"
**Solution:** Change port in `config.py` or kill the process:
```bash
# Find process
lsof -i :5000

# Kill it
kill <PID>
```

### Problem: "yt-dlp not found"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Problem: "Permission denied" when creating downloads folder
**Solution:** Check folder permissions:
```bash
chmod 755 downloads
```

---

## 📈 How to Extend

### Add More Endpoints
```python
@app.route('/api/custom', methods=['POST'])
def custom_endpoint():
    # Your code here
    return jsonify({'status': 'success'})
```

### Add Database
```python
# Install: pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    # ...
```

### Add Authentication
```python
# Install: pip install flask-jwt-extended
from flask_jwt_extended import JWTManager, jwt_required

jwt = JWTManager(app)

@app.route('/api/protected')
@jwt_required()
def protected():
    return jsonify({'message': 'Protected route'})
```

---

## ✅ Phase 2 Checklist

- [x] Flask server setup
- [x] Configuration management
- [x] yt-dlp integration
- [x] URL validation
- [x] Download functionality
- [x] File serving
- [x] Error handling
- [x] Basic security
- [x] API documentation

---

## 🎯 Next Steps (Phase 3)

In Phase 3, we will build:
- Modern dark-themed UI
- URL input field
- Download buttons
- Status displays
- Progress indicators
- Responsive design

**Ready?** Say "Yes, continue" to proceed to Phase 3!

