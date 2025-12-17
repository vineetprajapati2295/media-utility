"""
Simple API Test Script

This script tests the backend API endpoints.
Run this after starting the server to verify everything works.

Usage:
    python backend/test_api.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test health check endpoint."""
    print("Testing /api/health...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_validate():
    """Test URL validation endpoint."""
    print("Testing /api/validate...")
    # Replace with a real test URL
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    response = requests.post(
        f"{BASE_URL}/api/validate",
        json={"url": test_url}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("API Test Script")
    print("=" * 50)
    print()
    
    try:
        test_health()
        # Uncomment to test validation (requires valid URL)
        # test_validate()
        
        print("✅ Tests completed!")
        print("\nNote: Full download test requires a valid video URL.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server.")
        print("Make sure the Flask server is running:")
        print("  cd backend && python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

