#!/usr/bin/env python3
"""
SeaSense Integration Test Script
Tests the integration between the AI Trust Engine backend and Dashboard frontend
"""

import requests
import time
import sys
from pathlib import Path

def test_backend_health():
    """Test if backend is responding"""
    try:
        response = requests.get("http://127.0.0.1:8005/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Health: {data.get('status', 'unknown')}")
            print(f"   AI Pipeline: {data.get('ai_pipeline', 'unknown')}")
            return True
        else:
            print(f"❌ Backend Health Check Failed: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Backend Not Accessible: {e}")
        return False

def test_frontend_health():
    """Test if frontend is responding"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code in [200, 404]:  # 404 is OK for Next.js dev
            print("✅ Frontend is responding")
            return True
        else:
            print(f"❌ Frontend Health Check Failed: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Frontend Not Accessible: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    print("\n🔍 Testing API Endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get("http://127.0.0.1:8005/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except:
        print("❌ Root endpoint not accessible")
    
    # Test docs endpoint
    try:
        response = requests.get("http://127.0.0.1:8005/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation accessible")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except:
        print("❌ API docs not accessible")

def test_integration():
    """Test the complete integration"""
    print("🌊 SeaSense Integration Test\n")
    
    backend_ok = test_backend_health()
    frontend_ok = test_frontend_health()
    
    if backend_ok:
        test_api_endpoints()
    
    print(f"\n📊 Integration Status:")
    print(f"   Backend: {'🟢 Healthy' if backend_ok else '🔴 Failed'}")
    print(f"   Frontend: {'🟢 Healthy' if frontend_ok else '🔴 Failed'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Integration Successful!")
        print("   📊 Dashboard: http://localhost:3000")
        print("   🔧 Backend API: http://127.0.0.1:8005")
        print("   📚 API Docs: http://127.0.0.1:8005/docs")
        return True
    else:
        print("\n⚠️  Integration Issues Detected")
        if not backend_ok:
            print("   💡 Start backend: cd ai_trust_engine && python -m uvicorn main:app --port 8005 --reload")
        if not frontend_ok:
            print("   💡 Start frontend: cd seasense-dashboard && npm run dev")
        return False

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
