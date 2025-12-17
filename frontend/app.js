// Media Utility Platform - Frontend JavaScript
// Handles all UI interactions and API communication

// Load config first
let API_BASE_URL = 'http://127.0.0.1:5000/api';

// Use config if available, otherwise use default
if (typeof window !== 'undefined' && window.API_BASE_URL) {
    API_BASE_URL = window.API_BASE_URL;
} else {
    // Fallback: auto-detect
    const isDev = window.location.hostname === 'localhost' || 
                  window.location.hostname === '127.0.0.1';
    API_BASE_URL = isDev ? 'http://127.0.0.1:5000/api' : '/api';
}

// DOM Elements
const urlInput = document.getElementById('url-input');
const validateBtn = document.getElementById('validate-btn');
const downloadBtn = document.getElementById('download-btn');
const urlError = document.getElementById('url-error');
const videoInfo = document.getElementById('video-info');
const videoTitle = document.getElementById('video-title');
const videoMeta = document.getElementById('video-meta');
const videoThumbnail = document.getElementById('video-thumbnail');
const formatSelect = document.getElementById('format-select');
const statusSection = document.getElementById('status-section');
const statusMessage = document.getElementById('status-message');
const progressBar = document.getElementById('progress-bar');
const progressFill = document.getElementById('progress-fill');
const downloadTypeRadios = document.querySelectorAll('input[name="download-type"]');

let currentVideoInfo = null;
let currentUrl = '';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkServerHealth();
});

function setupEventListeners() {
    validateBtn.addEventListener('click', handleValidate);
    downloadBtn.addEventListener('click', handleDownload);
    
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleValidate();
        }
    });

    downloadTypeRadios.forEach(radio => {
        radio.addEventListener('change', handleDownloadTypeChange);
    });

    formatSelect.addEventListener('change', () => {
        // Format selection changed
    });
}

async function checkServerHealth() {
    try {
        console.log('Checking server health at:', API_BASE_URL.replace('/api', '/api/health'));
        const response = await fetch(`${API_BASE_URL.replace('/api', '/api/health')}`);
        const data = await response.json();
        if (data.status === 'healthy') {
            console.log('✅ Server is online');
        } else {
            console.warn('Server health check returned:', data);
        }
    } catch (error) {
        console.error('❌ Server health check failed:', error);
        console.error('API Base URL was:', API_BASE_URL);
        // Don't show error to user on page load, just log it
    }
}

async function handleValidate() {
    const url = urlInput.value.trim();
    
    if (!url) {
        showUrlError('Please enter a URL');
        return;
    }

    // Basic URL validation
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        showUrlError('URL must start with http:// or https://');
        return;
    }

    currentUrl = url;
    validateBtn.disabled = true;
    validateBtn.textContent = 'Validating...';
    clearUrlError();
    hideVideoInfo();

    try {
        console.log('Validating URL:', url);
        console.log('API Base URL:', API_BASE_URL);
        
        const response = await fetch(`${API_BASE_URL}/validate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            throw new Error(`Server error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log('Response data:', data);

        if (data.valid) {
            currentVideoInfo = data.video_info;
            showVideoInfo(data.video_info);
            populateFormatSelect(data.video_info.formats || []);
            downloadBtn.disabled = false;
            showUrlError('');
        } else {
            showUrlError(data.message || 'Invalid URL');
            downloadBtn.disabled = true;
        }
    } catch (error) {
        console.error('Validation error:', error);
        let errorMsg = 'Failed to validate URL. ';
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMsg += 'Cannot connect to server. Make sure the backend is running and the API URL is correct.';
        } else {
            errorMsg += error.message;
        }
        showUrlError(errorMsg);
        downloadBtn.disabled = true;
    } finally {
        validateBtn.disabled = false;
        validateBtn.textContent = 'Validate';
    }
}

function showVideoInfo(info) {
    videoTitle.textContent = info.title || 'Unknown Title';
    
    const duration = formatDuration(info.duration);
    const uploader = info.uploader || 'Unknown';
    videoMeta.textContent = `${uploader} • ${duration}`;
    
    if (info.thumbnail) {
        videoThumbnail.src = info.thumbnail;
        videoThumbnail.style.display = 'block';
    } else {
        videoThumbnail.style.display = 'none';
    }
    
    videoInfo.classList.remove('hidden');
}

function hideVideoInfo() {
    videoInfo.classList.add('hidden');
}

function populateFormatSelect(formats) {
    formatSelect.innerHTML = '';
    
    if (formats.length === 0) {
        formatSelect.innerHTML = '<option value="best">Best Quality</option>';
        return;
    }

    formats.forEach(format => {
        const option = document.createElement('option');
        option.value = format.format_id || 'best';
        
        const size = format.filesize ? ` (${formatFileSize(format.filesize)})` : '';
        option.textContent = `${format.resolution || 'Unknown'}${size}`;
        
        formatSelect.appendChild(option);
    });
}

function handleDownloadTypeChange() {
    const isAudio = document.querySelector('input[name="download-type"]:checked').value === 'audio';
    
    if (isAudio) {
        formatSelect.style.display = 'none';
        document.querySelector('#format-selector').style.display = 'none';
    } else {
        formatSelect.style.display = 'block';
        document.querySelector('#format-selector').style.display = 'block';
    }
}

async function handleDownload() {
    if (!currentUrl) {
        showError('Please validate a URL first');
        return;
    }

    const downloadType = document.querySelector('input[name="download-type"]:checked').value;
    const audioOnly = downloadType === 'audio';
    const formatId = audioOnly ? null : formatSelect.value;

    downloadBtn.disabled = true;
    downloadBtn.textContent = 'Downloading...';
    
    showStatus('waiting', 'Preparing download...');
    progressBar.classList.add('hidden');
    progressFill.style.width = '0%';

    try {
        const response = await fetch(`${API_BASE_URL}/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: currentUrl,
                format_id: formatId,
                audio_only: audioOnly,
            }),
        });

        const data = await response.json();

        if (data.status === 'success') {
            showStatus('downloading', `Downloading: ${data.filename}...`);
            
            // Simulate progress (yt-dlp doesn't provide real-time progress via API)
            simulateProgress();
            
            // Wait a bit then show success
            setTimeout(() => {
                showStatus('success', `Download complete! File: ${data.filename}`);
                downloadFile(data.download_url, data.filename);
                downloadBtn.disabled = false;
                downloadBtn.textContent = 'Download';
            }, 2000);
        } else {
            showStatus('error', data.message || 'Download failed');
            downloadBtn.disabled = false;
            downloadBtn.textContent = 'Download';
        }
    } catch (error) {
        console.error('Download error:', error);
        showStatus('error', 'Download failed. Check your connection.');
        downloadBtn.disabled = false;
        downloadBtn.textContent = 'Download';
    }
}

function simulateProgress() {
    progressBar.classList.remove('hidden');
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 95) {
            progress = 95;
            clearInterval(interval);
        }
        progressFill.style.width = `${progress}%`;
    }, 200);
}

function downloadFile(downloadUrl, filename) {
    const link = document.createElement('a');
    link.href = `${API_BASE_URL.replace('/api', '')}${downloadUrl}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function showStatus(type, message) {
    statusSection.classList.remove('hidden');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
}

function showUrlError(message) {
    urlError.textContent = message;
    urlError.style.display = message ? 'block' : 'none';
}

function clearUrlError() {
    urlError.textContent = '';
    urlError.style.display = 'none';
}

function showError(message) {
    showStatus('error', message);
}

function formatDuration(seconds) {
    if (!seconds) return 'Unknown duration';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function formatFileSize(bytes) {
    if (!bytes) return '';
    const mb = bytes / (1024 * 1024);
    return `${mb.toFixed(1)} MB`;
}
