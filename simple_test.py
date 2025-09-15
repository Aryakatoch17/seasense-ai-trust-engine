#!/usr/bin/env python3
"""
SeaSense Simple Test Runner
Run this script to test individual components step by step
"""

import requests
import json
import time
import sys

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print('='*50)

def print_result(test_name, success, message=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"    {message}")

def test_backend_health():
    print_header("Backend Health Check")
    try:
        response = requests.get("http://127.0.0.1:8005/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_result("Backend Health", True, f"Status: {data.get('status')}")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_result("Backend Health", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        print_result("Backend Health", False, str(e))
        return False

def test_api_docs():
    print_header("API Documentation")
    try:
        response = requests.get("http://127.0.0.1:8005/docs", timeout=5)
        success = response.status_code == 200
        print_result("API Documentation", success)
        if success:
            print("    Available at: http://127.0.0.1:8005/docs")
        return success
    except Exception as e:
        print_result("API Documentation", False, str(e))
        return False

def test_citizen_report():
    print_header("Citizen Report Submission")
    test_data = {
        "reporter_name": "Test User",
        "location": {
            "latitude": 19.0760,
            "longitude": 72.8777,
            "address": "Mumbai Beach, Maharashtra"
        },
        "hazard_type": "high_waves",
        "description": "Testing dangerous wave conditions with detailed description for AI analysis",
        "severity": "high",
        "timestamp": "2025-09-15T10:30:00",
        "contact_info": "test@example.com"
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8005/api/v1/reports/citizen",
            json=test_data,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print_result("Citizen Report", True, f"Report ID: {data.get('report_id')}")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True, data.get('report_id')
        else:
            print_result("Citizen Report", False, f"HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
    except Exception as e:
        print_result("Citizen Report", False, str(e))
        return False, None

def test_social_media():
    print_header("Social Media Ingestion")
    test_data = {
        "text": "Massive waves hitting Mumbai coastline! Everyone stay safe 🌊 #tsunami #mumbai #waves",
        "platform": "twitter",
        "author_id": "@oceanwatcher",
        "author_followers": 1500,
        "author_verified": True,
        "likes": 45,
        "shares": 12,
        "comments": 8,
        "location": {
            "latitude": 19.0760,
            "longitude": 72.8777
        },
        "hashtags": ["tsunami", "mumbai", "waves"],
        "posted_at": "2025-09-15T11:00:00"
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8005/api/v1/social-media/ingest",
            json=test_data,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print_result("Social Media", True, f"Post ID: {data.get('post_id')}")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_result("Social Media", False, f"HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print_result("Social Media", False, str(e))
        return False

def test_trust_score():
    print_header("Trust Score Calculation")
    test_data = {
        "report": {
            "id": "test_report",
            "description": "High waves and dangerous conditions for trust score testing",
            "hazard_type": "high_waves",
            "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Mumbai"},
            "trust_score": 0,
            "priority": "high",
            "timestamp": "2025-09-15T10:30:00",
            "status": "pending",
            "source": "citizen"
        },
        "social_media_posts": []
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8005/api/v1/trust-scores/calculate",
            json=test_data,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print_result("Trust Score", True, f"Score: {data.get('trust_score', 'N/A')}")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_result("Trust Score", False, f"HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print_result("Trust Score", False, str(e))
        return False

def test_frontend():
    print_header("Frontend Connectivity")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        success = response.status_code in [200, 404]  # 404 is OK for Next.js
        print_result("Frontend", success)
        if success:
            print("    Dashboard available at: http://localhost:3000")
        return success
    except Exception as e:
        print_result("Frontend", False, str(e))
        return False

def main():
    print("🌊 SeaSense AI Trust Engine - Simple Test Runner")
    print("=" * 60)
    
    # Test each component
    results = {}
    
    results['backend'] = test_backend_health()
    results['api_docs'] = test_api_docs()
    results['frontend'] = test_frontend()
    results['citizen_report'], report_id = test_citizen_report()
    results['social_media'] = test_social_media()
    results['trust_score'] = test_trust_score()
    
    # Summary
    print_header("Test Summary")
    passed = sum(results.values())
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    print("\n📋 Individual Results:")
    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {test.replace('_', ' ').title()}")
    
    print("\n🔗 Quick Links:")
    print("  Dashboard: http://localhost:3000")
    print("  API Docs:  http://127.0.0.1:8005/docs")
    print("  Health:    http://127.0.0.1:8005/health")
    
    if passed < total:
        print(f"\n⚠️  {total - passed} tests failed. Check the output above for details.")
        print("Make sure both backend and frontend are running:")
        print("  Backend: cd ai_trust_engine && python3 -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload")
        print("  Frontend: cd seasense-dashboard && npm run dev")
    else:
        print("\n🎉 All tests passed! The system is working correctly.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
