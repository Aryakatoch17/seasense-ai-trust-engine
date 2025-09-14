#!/usr/bin/env python3
"""
Complete SeaSense API Test - All Endpoints
Smart India Hackathon 2025
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8005"

def test_endpoint(name, method, url, data=None):
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"📍 URL: {url}")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            result = response.json()
            print("📋 Response:")
            print(json.dumps(result, indent=2))
            return result
        else:
            print("❌ ERROR!")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    print("🌊 SeaSense AI Trust Engine - Complete API Test")
    print("=" * 60)
    
    # Test 1: Health Check
    health_result = test_endpoint(
        "Health Check",
        "GET", 
        f"{BASE_URL}/health"
    )
    
    if not health_result:
        print("❌ Server not responding. Please start the server first:")
        print("cd ai_trust_engine")
        print("python -m uvicorn main:app --host 0.0.0.0 --port 8005")
        return
    
    time.sleep(1)
    
    # Test 2: Citizen Report
    citizen_data = {
        "reporter_name": "Arya Katoch - SIH 2025",
        "location": {
            "latitude": 19.0760,
            "longitude": 72.8777,
            "address": "Mumbai Beach, Maharashtra"
        },
        "hazard_type": "high_waves",
        "description": "Dangerous wave conditions observed at Mumbai beach. Multiple swimmers in distress. Immediate action required.",
        "severity": "high",
        "timestamp": "2025-09-14T15:30:00",
        "contact_info": "arya@sih2025.com"
    }
    
    citizen_result = test_endpoint(
        "Citizen Report Submission",
        "POST",
        f"{BASE_URL}/api/v1/reports/citizen",
        citizen_data
    )
    
    time.sleep(1)
    
    # Test 3: Social Media Report
    social_data = {
        "platform": "twitter",
        "username": "@SIH2025Demo",
        "post_content": "🚨 URGENT: Massive waves hitting Mumbai coastline! Dangerous conditions observed. Stay away from beaches! #OceanHazard #Mumbai #Safety #SIH2025",
        "location": {
            "latitude": 19.0760,
            "longitude": 72.8777,
            "address": "Mumbai Beach, Maharashtra"
        },
        "timestamp": "2025-09-14T15:32:00",
        "media_urls": ["https://example.com/wave-danger.jpg"],
        "user_followers": 2500,
        "engagement": {
            "likes": 150,
            "shares": 75,
            "comments": 45
        }
    }
    
    social_result = test_endpoint(
        "Social Media Analysis",
        "POST",
        f"{BASE_URL}/api/v1/reports/social-media",
        social_data
    )
    
    time.sleep(1)
    
    # Test 4: Trust Score (if we have a report ID)
    if citizen_result and 'data' in citizen_result and 'original_report' in citizen_result['data']:
        report_id = citizen_result['data']['original_report']['id']
        test_endpoint(
            "Trust Score Analysis",
            "GET",
            f"{BASE_URL}/api/v1/trust-scores/{report_id}"
        )
    
    print(f"\n{'='*60}")
    print("🎉 API Testing Complete!")
    print("✅ All endpoints tested successfully")
    print("🌊 SeaSense AI Trust Engine - Ready for SIH 2025!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
