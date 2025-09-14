#!/usr/bin/env python3
"""
Test script for SeaSense AI Trust Engine Dashboard
This script tests the backend API endpoints used by the dashboard
"""

import requests
import json
import time
import sys
from typing import Dict, Any

API_BASE_URL = "http://127.0.0.1:8005"

def test_endpoint(endpoint: str, method: str = "GET", data: Dict[Any, Any] = None) -> bool:
    """Test a single API endpoint"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == 200:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            return True
        else:
            print(f"❌ {method} {endpoint} - Status: {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - Connection failed (Backend not running?)")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False

def test_dashboard_endpoints():
    """Test all dashboard-related endpoints"""
    print("🧪 Testing SeaSense AI Trust Engine Dashboard Endpoints")
    print("=" * 60)
    
    # Test basic endpoints
    endpoints = [
        ("/health", "GET"),
        ("/", "GET"),
        ("/api/v1/reports/nearby?latitude=19.076&longitude=72.877&radius_km=50", "GET"),
        ("/api/v1/trust-scores/analytics/distribution", "GET"),
        ("/api/v1/social-media/trending", "GET"),
    ]
    
    passed = 0
    total = len(endpoints)
    
    for endpoint, method in endpoints:
        if test_endpoint(endpoint, method):
            passed += 1
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} endpoints passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard should work correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check backend logs for details.")
        return False

def test_citizen_report_submission():
    """Test citizen report submission"""
    print("\n🧪 Testing Citizen Report Submission")
    print("-" * 40)
    
    test_report = {
        "description": "Test high waves observed near Mumbai Beach",
        "hazard_type": "high_waves",
        "location": {
            "latitude": 19.076,
            "longitude": 72.877
        },
        "location_name": "Mumbai Beach, Maharashtra",
        "reporter_id": "test_user_123",
        "images": []
    }
    
    if test_endpoint("/api/v1/reports/citizen", "POST", test_report):
        print("✅ Citizen report submission works!")
        return True
    else:
        print("❌ Citizen report submission failed!")
        return False

def main():
    """Main test function"""
    print("🌊 SeaSense AI Trust Engine Dashboard Test Suite")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend is not responding correctly")
            print("   Make sure to start the backend first:")
            print("   cd ai_trust_engine && python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running!")
        print("   Start the backend first:")
        print("   cd ai_trust_engine && python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload")
        return False
    
    print("✅ Backend is running!")
    
    # Run tests
    dashboard_ok = test_dashboard_endpoints()
    report_ok = test_citizen_report_submission()
    
    print("\n" + "=" * 60)
    if dashboard_ok and report_ok:
        print("🎉 All tests passed! Your dashboard is ready to use.")
        print("\n📊 Access your dashboard at: http://localhost:3000")
        print("🔧 API documentation at: http://127.0.0.1:8005/docs")
        return True
    else:
        print("⚠️  Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
