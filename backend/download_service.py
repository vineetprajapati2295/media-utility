"""
Download Service Module

This module handles all yt-dlp operations.
Why separate? Keeps the main app.py clean and makes testing easier.
"""

import yt_dlp
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from backend.config import DOWNLOADS_DIR, YTDLP_OPTIONS, MAX_DOWNLOAD_SIZE_BYTES, MAX_DOWNLOAD_SIZE_MB


class DownloadService:
    """
    Service class for handling media downloads.
    
    Why a class? Encapsulates download logic and makes it reusable.
    """
    
    def __init__(self):
        """Initialize the download service."""
        self.downloads_dir = DOWNLOADS_DIR
    
    def validate_url(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate if the URL is supported by yt-dlp.
        
        Args:
            url: The URL to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url or not isinstance(url, str):
            return False, "URL is required and must be a string"
        
        url = url.strip()
        
        # Basic URL format check
        if not url.startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"
        
        # Check if yt-dlp can extract info (without downloading)
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,  # Need full extraction to check properly
                # YouTube bot detection bypass - try ios first (most reliable)
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'android', 'web'],  # Try ios first
                        'player_skip': ['webpage'],
                    }
                },
                # Retry options
                'retries': 5,
                'fragment_retries': 5,
                'file_access_retries': 3,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=False)
            
            return True, None
            
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            # Handle YouTube bot detection errors
            if "Sign in to confirm" in error_msg or "bot" in error_msg.lower():
                return False, "YouTube is blocking automated requests. Please try again in a few minutes or use a different video."
            elif "Private video" in error_msg:
                return False, "This video is private and cannot be downloaded"
            elif "Video unavailable" in error_msg:
                return False, "Video is unavailable or has been removed"
            elif "Unsupported URL" in error_msg:
                return False, "This URL is not supported"
            else:
                # Return a cleaner error message
                if "ERROR:" in error_msg:
                    # Extract just the error part
                    error_part = error_msg.split("ERROR:")[-1].strip()
                    if len(error_part) > 200:
                        error_part = error_part[:200] + "..."
                    return False, f"URL validation failed: {error_part}"
                return False, f"URL validation failed: {error_msg[:200]}"
        
        except Exception as e:
            error_msg = str(e)
            if "bot" in error_msg.lower() or "Sign in" in error_msg:
                return False, "YouTube is blocking automated requests. Please try again later."
            return False, f"Error validating URL: {error_msg[:200]}"
    
    def get_video_info(self, url: str) -> Dict:
        """
        Get video information without downloading.
        
        Args:
            url: The video URL
            
        Returns:
            Dictionary with video information (title, duration, formats, etc.)
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            # YouTube bot detection bypass - try ios first (most reliable)
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web'],  # Try ios first
                    'player_skip': ['webpage'],
                }
            },
            'retries': 5,
            'fragment_retries': 5,
            'file_access_retries': 3,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extract relevant information
                video_info = {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'formats': self._extract_formats(info),
                }
                
                return video_info
                
        except Exception as e:
            error_msg = str(e)
            if "bot" in error_msg.lower() or "Sign in" in error_msg:
                raise Exception("YouTube is blocking automated requests. Please try again in a few minutes.")
            raise Exception(f"Failed to get video info: {error_msg[:200]}")
    
    def _extract_formats(self, info: Dict) -> list:
        """
        Extract available formats from video info.
        
        Args:
            info: Raw yt-dlp info dictionary
            
        Returns:
            List of available formats
        """
        formats = []
        
        # Get available formats
        available_formats = info.get('formats', [])
        
        # Extract unique video formats
        seen_resolutions = set()
        for fmt in available_formats:
            if fmt.get('vcodec') != 'none':  # Has video
                resolution = fmt.get('resolution', 'unknown')
                if resolution not in seen_resolutions:
                    formats.append({
                        'format_id': fmt.get('format_id'),
                        'resolution': resolution,
                        'ext': fmt.get('ext', 'mp4'),
                        'filesize': fmt.get('filesize', 0),
                    })
                    seen_resolutions.add(resolution)
        
        # Add audio-only option
        audio_formats = [f for f in available_formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
        if audio_formats:
            best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))
            formats.append({
                'format_id': best_audio.get('format_id'),
                'resolution': 'audio only',
                'ext': best_audio.get('ext', 'mp3'),
                'filesize': best_audio.get('filesize', 0),
            })
        
        return formats
    
    def download_video(self, url: str, format_id: Optional[str] = None, audio_only: bool = False) -> Dict:
        """
        Download video or audio from URL.
        
        Args:
            url: The video URL
            format_id: Specific format ID to download (optional)
            audio_only: If True, download audio only
            
        Returns:
            Dictionary with download status and file path
        """
        # Prepare yt-dlp options
        ydl_opts = YTDLP_OPTIONS.copy()
        
        if audio_only:
            # Audio-only download
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif format_id:
            # Specific format
            ydl_opts['format'] = format_id
        else:
            # Best quality (default)
            ydl_opts['format'] = 'best'
        
        # Progress hook to track download
        download_info = {'status': 'downloading', 'progress': 0}
        
        def progress_hook(d):
            """Callback function for download progress."""
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    download_info['progress'] = int((downloaded / total) * 100)
                    download_info['downloaded'] = downloaded
                    download_info['total'] = total
            elif d['status'] == 'finished':
                download_info['status'] = 'finished'
                download_info['filename'] = d.get('filename')
        
        ydl_opts['progress_hooks'] = [progress_hook]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first to get filename
                info = ydl.extract_info(url, download=True)
                
                # Get the actual downloaded file
                filename = ydl.prepare_filename(info)
                
                # If audio, the file might have different extension
                if audio_only and not filename.endswith('.mp3'):
                    # Find the actual mp3 file
                    base_name = Path(filename).stem
                    mp3_file = self.downloads_dir / f"{base_name}.mp3"
                    if mp3_file.exists():
                        filename = str(mp3_file)
                
                # Check file size
                file_path = Path(filename)
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    if file_size > MAX_DOWNLOAD_SIZE_BYTES:
                        file_path.unlink()  # Delete oversized file
                        raise Exception(f"File too large: {file_size / 1024 / 1024:.2f}MB (max: {MAX_DOWNLOAD_SIZE_MB}MB)")
                    
                    return {
                        'status': 'success',
                        'filename': file_path.name,
                        'filepath': str(file_path),
                        'filesize': file_size,
                        'title': info.get('title', 'Unknown'),
                    }
                else:
                    raise Exception("Downloaded file not found")
                    
        except yt_dlp.utils.DownloadError as e:
            raise Exception(f"Download failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Download error: {str(e)}")

