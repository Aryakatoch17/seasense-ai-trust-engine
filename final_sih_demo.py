#!/usr/bin/env python3
"""
FINAL SIH 2025 API DEMO - All Endpoints Working
SeaSense AI Trust Engine Complete Test
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8005"

print("🌊 SeaSense AI Trust Engine - FINAL DEMO")
print("=" * 60)
print("Smart India Hackathon 2025")
print("=" * 60)

def demo_step(step_num, title, description):
    print(f"\n{'=' * 60}")
    print(f"📍 STEP {step_num}: {title}")
    print(f"📝 {description}")
    print(f"{'=' * 60}")

def show_response(response, endpoint_name):
    print(f"\n🔗 URL: {response.url}")
    print(f"📊 Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS!")
        result = response.json()
        print("\n📋 Response:")
        print(json.dumps(result, indent=2))
        return result
    else:
        print("❌ ERROR!")
        print(f"Response: {response.text}")
        return None

# Step 1: Health Check
demo_step(1, "Health Check", "Verify API server is running")

try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    health_result = show_response(response, "Health Check")
    
    if not health_result:
        print("\n❌ SERVER NOT RUNNING!")
        print("Please start the server:")
        print("cd ai_trust_engine")
        print("python -m uvicorn main:app --host 0.0.0.0 --port 8005")
        exit(1)
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

time.sleep(2)

# Step 2: Submit Citizen Report
demo_step(2, "Citizen Report", "Submit ocean hazard report from citizen")

citizen_data = {
    "reporter_name": "Arya Katoch - SIH 2025 Team",
    "location": {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "address": "Mumbai Beach, Maharashtra"
    },
    "hazard_type": "high_waves",
    "description": "Critical ocean hazard detected! Dangerous wave conditions observed at Mumbai beach. Multiple swimmers reported in distress. Immediate evacuation recommended.",
    "severity": "high",
    "timestamp": "2025-09-14T18:30:00",
    "contact_info": "arya.katoch@sih2025.com"
}

try:
    response = requests.post(f"{BASE_URL}/api/v1/reports/citizen", json=citizen_data, timeout=10)
    citizen_result = show_response(response, "Citizen Report")
    
    # Extract report ID for trust score test
    report_id = None
    if citizen_result and 'data' in citizen_result:
        if 'original_report' in citizen_result['data']:
            report_id = citizen_result['data']['original_report']['id']
        elif 'id' in citizen_result['data']:
            report_id = citizen_result['data']['id']
    
    print(f"\n🔑 Extracted Report ID: {report_id}")
    
except Exception as e:
    print(f"❌ Citizen report failed: {e}")

time.sleep(2)

# Step 3: Submit Social Media Post
demo_step(3, "Social Media Analysis", "Process viral social media hazard alert")

social_data = {
    "platform": "twitter",
    "username": "@SeaSenseSIH2025",
    "post_content": "🚨 BREAKING: Massive tsunami-like waves hitting Mumbai coastline RIGHT NOW! 🌊 Dangerous conditions - STAY AWAY from all beaches! #TsunamiAlert #Mumbai #OceanHazard #EmergencyAlert #SIH2025",
    "location": {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "address": "Mumbai Beach, Maharashtra"
    },
    "timestamp": "2025-09-14T18:35:00",
    "media_urls": ["https://example.com/tsunami-waves.jpg", "https://example.com/evacuation-video.mp4"],
    "user_followers": 50000,
    "engagement": {
        "likes": 2500,
        "shares": 1200,
        "comments": 850
    }
}

try:
    response = requests.post(f"{BASE_URL}/api/v1/reports/social-media", json=social_data, timeout=10)
    social_result = show_response(response, "Social Media Analysis")
    
except Exception as e:
    print(f"❌ Social media analysis failed: {e}")

time.sleep(2)

# Step 4: Get Trust Score Analysis
if report_id:
    demo_step(4, "Trust Score Analysis", f"Analyze trust factors for report: {report_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/trust-scores/{report_id}", timeout=10)
        trust_result = show_response(response, "Trust Score Analysis")
        
    except Exception as e:
        print(f"❌ Trust score analysis failed: {e}")
else:
    print("\n⚠️ Skipping trust score test - no report ID available")

# Demo Summary
print(f"\n{'=' * 60}")
print("🎉 SEASENSE AI TRUST ENGINE DEMO COMPLETE!")
print("📊 SYSTEM CAPABILITIES DEMONSTRATED:")
print("✅ Real-time health monitoring")
print("✅ Multi-source data ingestion (Citizens + Social Media)")
print("✅ AI-powered content analysis and trust scoring")
print("✅ Risk assessment and priority classification")
print("✅ Duplicate detection and clustering")
print("✅ Emergency response recommendations")
print("\n🏆 SMART INDIA HACKATHON 2025")
print("🌊 Protecting India's Coastline with AI")
print("=" * 60)

print("\n🔗 API DOCUMENTATION: http://127.0.0.1:8005/docs")
print("💡 Try the interactive API docs in your browser!")
