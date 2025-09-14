#!/usr/bin/env python3
"""
Start script for SeaSense AI Trust Engine Dashboard
This script starts both the backend API and frontend dashboard
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("🌊 Starting SeaSense AI Trust Engine Backend...")
    backend_dir = Path("ai_trust_engine")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return None
    
    try:
        # Start the backend server
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8005", "--reload"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ Backend server started on http://127.0.0.1:8005")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend dashboard"""
    print("🎨 Starting SeaSense Dashboard Frontend...")
    frontend_dir = Path("seasense-dashboard")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return None
    
    try:
        # Check if node_modules exists, if not install dependencies
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Start the frontend server
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ Frontend dashboard started on http://localhost:3000")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def monitor_process(process, name):
    """Monitor a process and print its output"""
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[{name}] {line.strip()}")
    except Exception as e:
        print(f"Error monitoring {name}: {e}")

def main():
    """Main function to start both services"""
    print("🚀 Starting SeaSense AI Trust Engine Dashboard")
    print("=" * 50)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Stopping backend.")
        backend_process.terminate()
        return
    
    print("\n🎉 Both services are running!")
    print("📊 Dashboard: http://localhost:3000")
    print("🔧 API: http://127.0.0.1:8005")
    print("📚 API Docs: http://127.0.0.1:8005/docs")
    print("\nPress Ctrl+C to stop both services")
    
    # Start monitoring threads
    backend_thread = threading.Thread(target=monitor_process, args=(backend_process, "BACKEND"))
    frontend_thread = threading.Thread(target=monitor_process, args=(frontend_process, "FRONTEND"))
    
    backend_thread.daemon = True
    frontend_thread.daemon = True
    
    backend_thread.start()
    frontend_thread.start()
    
    try:
        # Wait for processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        # Wait for processes to terminate
        time.sleep(2)
        
        # Force kill if still running
        if backend_process and backend_process.poll() is None:
            backend_process.kill()
        if frontend_process and frontend_process.poll() is None:
            frontend_process.kill()
        
        print("✅ Services stopped successfully")

if __name__ == "__main__":
    main()
