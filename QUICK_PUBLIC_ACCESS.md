# 🚀 INSTANT PUBLIC ACCESS - Ngrok Setup

## ⚡ **Fastest Solution: Ngrok (5 minutes)**

Get your API publicly accessible in 5 minutes!

### **Step 1: Download Ngrok**
1. Go to [ngrok.com](https://ngrok.com/download)
2. Download for Windows
3. Extract to a folder (e.g., `C:\ngrok\`)

### **Step 2: Setup Ngrok**
```bash
# Add ngrok to your PATH or run from the folder
# Sign up for free account and get auth token
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### **Step 3: Start Your API**
```bash
# Terminal 1: Start your FastAPI server
cd "C:/Users/aryak/OneDrive/Desktop/sih_trust engine/ai_trust_engine"
"C:/Users/aryak/OneDrive/Desktop/sih_trust engine/.venv/Scripts/python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8005
```

### **Step 4: Create Public Tunnel**
```bash
# Terminal 2: Create public tunnel
ngrok http 8005
```

### **Step 5: Get Your Public URL**
Ngrok will show something like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8005
```

### **Step 6: Test Publicly**
✅ **Your API is now public!**
- **Health**: `https://abc123.ngrok.io/health`
- **Docs**: `https://abc123.ngrok.io/docs`
- **Reports**: `POST https://abc123.ngrok.io/api/v1/reports/citizen`

### **Step 7: Update Postman Collection**
Replace all instances of `127.0.0.1:8005` with your ngrok URL in the Postman collection.

## 🎯 **Alternative: Render.com (Permanent)**

### **For permanent hosting:**
1. Push your code to GitHub
2. Go to [render.com](https://render.com)
3. Connect your GitHub repository
4. Deploy as a web service
5. Use the `render.yaml` file I created

### **Render Settings:**
- **Build Command**: `cd ai_trust_engine && pip install -r requirements.txt`
- **Start Command**: `cd ai_trust_engine && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

## ✅ **Which Option Should You Choose?**

### **For SIH Demo/Testing:**
- **Ngrok**: Instant, free, perfect for demos
- Takes 5 minutes to setup
- Great for sharing with team/judges

### **For Production/Portfolio:**
- **Render**: Permanent hosting, free tier
- Takes 15 minutes to setup
- Better for long-term use

Would you like me to help you set up either option?
