#!/usr/bin/env python3
"""
SeaSense AI Trust Engine - Live Demo Script
Smart India Hackathon 2025
"""

import requests
import json
import time
from datetime import datetime

# API Configuration
BASE_URL = "http://127.0.0.1:8005"

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🌊 {title}")
    print(f"{'='*50}")

def print_response(response, description):
    print(f"\n📋 {description}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ SUCCESS")
        print(json.dumps(response.json(), indent=2))
    else:
        print("❌ ERROR")
        print(response.text)

def main():
    print_header("SeaSense AI Trust Engine - Live Demo")
    print("🚀 Starting comprehensive API demonstration...")
    
    # 1. Health Check
    print_header("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "System Health Status")
    
    # 2. Citizen Report - High Waves
    print_header("2. Citizen Report - High Waves Alert")
    citizen_data = {
        "reporter_name": "Priya Sharma",
        "location": {
            "latitude": 19.0760,
            "longitude": 72.8777,
            "address": "Mumbai Beach, Maharashtra"
        },
        "hazard_type": "high_waves",
        "description": "Observed dangerous wave conditions at the beach. Several people were struggling in the water. Lifeguards are warning everyone to stay out.",
        "severity": "high",
        "timestamp": "2025-09-14T14:30:00",
        "contact_info": "priya.sharma@gmail.com"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/reports/citizen", json=citizen_data)
    print_response(response, "Citizen Report Submission")
    
    citizen_report_id = None
    if response.status_code == 200:
        citizen_report_id = response.json().get("report_id")
        print(f"📝 Report ID saved: {citizen_report_id}")
    
    time.sleep(1)
    
    # 3. Citizen Report - Tsunami Warning
    print_header("3. Citizen Report - CRITICAL Tsunami Alert")
    tsunami_data = {
        "reporter_name": "Rajesh Kumar",
        "location": {
            "latitude": 15.2993,
            "longitude": 74.1240,
            "address": "Calangute Beach, Goa"
        },
        "hazard_type": "tsunami",
        "description": "URGENT! Water suddenly receded from the beach exposing the sea floor completely. This is a clear tsunami warning sign! People are running inland.",
        "severity": "critical",
        "timestamp": "2025-09-14T14:35:00",
        "contact_info": "rajesh.kumar@emergency.gov.in"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/reports/citizen", json=tsunami_data)
    print_response(response, "CRITICAL Tsunami Report")
    
    tsunami_report_id = None
    if response.status_code == 200:
        tsunami_report_id = response.json().get("report_id")
        print(f"🚨 CRITICAL Report ID: {tsunami_report_id}")
    
    time.sleep(1)
    
    # 4. Social Media Report - Corroborating Evidence
    print_header("4. Social Media Analysis - Viral Alert")
    social_data = {
        "platform": "twitter",
        "username": "@CoastalGuardIndia",
        "post_content": "🚨 EMERGENCY ALERT: Tsunami warning for Goa coastline! Sea water receding rapidly at multiple beaches. EVACUATE IMMEDIATELY! Share to save lives. #TsunamiAlert #GoaEmergency #IndianCoast",
        "location": {
            "latitude": 15.2993,
            "longitude": 74.1240,
            "address": "Goa Coastline, India"
        },
        "timestamp": "2025-09-14T14:37:00",
        "media_urls": ["https://example.com/tsunami-evidence.jpg", "https://example.com/evacuation-video.mp4"],
        "user_followers": 50000,
        "engagement": {
            "likes": 1250,
            "shares": 890,
            "comments": 445
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/reports/social-media", json=social_data)
    print_response(response, "Viral Social Media Analysis")
    
    social_report_id = None
    if response.status_code == 200:
        social_report_id = response.json().get("post_id")
        print(f"📱 Social Media ID: {social_report_id}")
    
    time.sleep(1)
    
    # 5. Trust Score Analysis - Citizen Report
    if citizen_report_id:
        print_header("5. Trust Score Analysis - Citizen Report")
        response = requests.get(f"{BASE_URL}/api/v1/trust-scores/{citizen_report_id}")
        print_response(response, "Citizen Report Trust Analysis")
    
    time.sleep(1)
    
    # 6. Trust Score Analysis - Tsunami Report
    if tsunami_report_id:
        print_header("6. Trust Score Analysis - CRITICAL Tsunami")
        response = requests.get(f"{BASE_URL}/api/v1/trust-scores/{tsunami_report_id}")
        print_response(response, "CRITICAL Tsunami Trust Analysis")
    
    time.sleep(1)
    
    # 7. Additional Social Media - False Alarm Detection
    print_header("7. Social Media Analysis - Potential False Alarm")
    false_alarm_data = {
        "platform": "instagram",
        "username": "@beachparty_goa",
        "post_content": "OMG guys the water is so weird today!! Like totally going out super far! Perfect time for beach volleyball though 🏐🏖️ #beachday #weirdwaves #volleyball",
        "location": {
            "latitude": 15.2993,
            "longitude": 74.1240,
            "address": "Calangute Beach, Goa"
        },
        "timestamp": "2025-09-14T14:40:00",
        "media_urls": ["https://example.com/volleyball-pic.jpg"],
        "user_followers": 250,
        "engagement": {
            "likes": 15,
            "shares": 2,
            "comments": 8
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/reports/social-media", json=false_alarm_data)
    print_response(response, "Casual Social Media Analysis")
    
    # Final Summary
    print_header("Demo Complete - AI Trust Engine Summary")
    print("🎯 Demonstrated Capabilities:")
    print("✅ Multi-source data ingestion (Citizens + Social Media)")
    print("✅ Real-time AI analysis and keyword extraction")
    print("✅ Trust scoring based on content quality and source credibility")
    print("✅ Severity assessment and risk categorization")
    print("✅ Automatic duplicate detection and correlation")
    print("✅ Emergency alert prioritization")
    print("\n🌊 SeaSense AI Trust Engine - Protecting India's Coastline")
    print("📧 Contact: Smart India Hackathon 2025 Team")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API server")
        print("🔧 Please ensure the server is running:")
        print("   cd ai_trust_engine")
        print("   python -m uvicorn main:app --host 0.0.0.0 --port 8005")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
