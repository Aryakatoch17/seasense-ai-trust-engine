# 🌊 SeaSense AI Trust Engine - FINAL DEMO GUIDE
## Smart India Hackathon 2025

### 📋 **COMPLETE ENDPOINT REFERENCE**

---

## 🚀 **How to Start & Test**

### **Step 1: Start Server**
```bash
cd "C:/Users/aryak/OneDrive/Desktop/sih_trust engine/ai_trust_engine"
"C:/Users/aryak/OneDrive/Desktop/sih_trust engine/.venv/Scripts/python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8005
```

### **Step 2: Verify Server is Running**
- Open browser: `http://127.0.0.1:8005/docs`
- Or test: `curl -X GET "http://127.0.0.1:8005/health"`

---

## 🎯 **ALL 4 ENDPOINTS EXPLAINED**

### **1. Health Check** ✅
**Purpose**: Verify API is running  
**URL**: `GET /health`

```bash
curl -X GET "http://127.0.0.1:8005/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-14T18:47:29.327Z"
}
```

---

### **2. Citizen Report Submission** 👤
**Purpose**: Citizens report ocean hazards  
**URL**: `POST /api/v1/reports/citizen`

#### **CORRECT Input Format:**
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{
    "reporter_name": "Arya Katoch",
    "location": {
      "latitude": 19.0760,
      "longitude": 72.8777,
      "address": "Mumbai Beach, Maharashtra"
    },
    "hazard_type": "high_waves",
    "description": "Dangerous wave conditions observed. Multiple swimmers in distress.",
    "severity": "high",
    "timestamp": "2025-09-14T15:30:00",
    "contact_info": "arya@sih2025.com"
  }'
```

#### **Input Requirements:**
- `hazard_type`: Must be one of `tsunami`, `storm`, `high_waves`, `pollution`, `debris`, `unusual_current`, `temperature_anomaly`, `other`
- `severity`: Must be `low`, `medium`, `high`, `critical`
- `location`: Must be object with `latitude`, `longitude`, `address`

#### **Response:**
```json
{
  "report_id": "citizen_1726341449327",
  "status": "received",
  "trust_score": 75.5,
  "message": "Citizen report processed successfully",
  "analysis": {
    "keywords": ["dangerous", "wave", "swimmers", "distress"],
    "risk_level": "high",
    "credibility": "good"
  }
}
```

---

### **3. Social Media Analysis** 📱
**Purpose**: Analyze social media posts for hazard detection  
**URL**: `POST /api/v1/reports/social-media`

#### **CORRECT Input Format:**
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/social-media" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "twitter",
    "username": "@SIH2025Demo",
    "post_content": "🚨 ALERT: Massive waves hitting Mumbai coastline! Stay safe everyone! #OceanHazard #Mumbai #Safety",
    "location": {
      "latitude": 19.0760,
      "longitude": 72.8777,
      "address": "Mumbai Beach, Maharashtra"
    },
    "timestamp": "2025-09-14T15:32:00",
    "media_urls": ["https://example.com/wave-image.jpg"],
    "user_followers": 1000,
    "engagement": {
      "likes": 50,
      "shares": 25,
      "comments": 15
    }
  }'
```

#### **Input Requirements:**
- `platform`: Must be `twitter`, `facebook`, `instagram`, `youtube`, `tiktok`, `other`
- `engagement`: Object with `likes`, `shares`, `comments` numbers

#### **Response:**
```json
{
  "post_id": "social_1726341461327",
  "status": "processed",
  "trust_score": 68.2,
  "message": "Social media post analyzed successfully",
  "analysis": {
    "keywords": ["alert", "massive", "waves", "safety"],
    "sentiment": "warning",
    "viral_potential": "medium"
  }
}
```

---

### **4. Trust Score Analysis** 🧠
**Purpose**: Get detailed trust analysis for any report  
**URL**: `GET /api/v1/trust-scores/{report_id}`

#### **Example:**
```bash
# Use report_id from previous submissions
curl -X GET "http://127.0.0.1:8005/api/v1/trust-scores/citizen_1726341449327"
```

#### **Response:**
```json
{
  "report_id": "citizen_1726341449327",
  "trust_score": 75.5,
  "confidence": 0.85,
  "factors": {
    "source_credibility": 0.8,
    "content_quality": 0.9,
    "temporal_consistency": 0.7,
    "location_accuracy": 0.95
  },
  "risk_assessment": "high",
  "recommendations": [
    "Monitor for corroborating reports",
    "Issue public warning",
    "Alert relevant authorities"
  ]
}
```

---

## 🎬 **SIH 2025 DEMO SCRIPT**

### **Demo Flow:**

1. **Show Health Check** → Proves system is live
2. **Submit Citizen Report** → Shows public engagement
3. **Submit Social Media** → Shows multi-source analysis  
4. **Get Trust Scores** → Shows AI decision making
5. **Explain Results** → Show keyword extraction, risk levels

### **Key Demo Points:**
- ✅ **Real-time processing** - Instant responses
- ✅ **Multi-source intelligence** - Citizens + Social Media
- ✅ **AI-powered analysis** - Keyword extraction, sentiment
- ✅ **Trust scoring** - Credibility assessment
- ✅ **Risk categorization** - From low to critical
- ✅ **Actionable recommendations** - Alert authorities

---

## 🔧 **Testing Tools Available**

### **1. Browser Interface**
- **API Docs**: `http://127.0.0.1:8005/docs` (Interactive testing)
- **Health**: `http://127.0.0.1:8005/health`

### **2. Postman Collection**
- Import `SeaSense_API_Collection.json`
- Pre-configured with correct data formats

### **3. Python Scripts**
- `quick_demo.py` - Full endpoint testing
- `live_demo.py` - Complete SIH demo script

### **4. Curl Commands**
- Copy-paste ready commands above
- All formats validated and working

---

## ❌ **COMMON ERRORS & FIXES**

### **Error: 422 Validation Error**
❌ **Wrong hazard_type:**
```json
"hazard_type": "High waves and strong currents"
```
✅ **Correct:**
```json
"hazard_type": "high_waves"
```

❌ **Wrong location format:**
```json
"location": "Mumbai Beach"
```
✅ **Correct:**
```json
"location": {
  "latitude": 19.0760,
  "longitude": 72.8777,
  "address": "Mumbai Beach"
}
```

### **Error: Connection Refused**
- ✅ Check server is running on port 8005
- ✅ Use correct URL: `http://127.0.0.1:8005`

---

## 🎯 **FOR SIH JUDGES**

### **Key Message:**
"Our SeaSense AI Trust Engine processes multiple data sources - citizen reports and social media - to provide real-time, AI-powered ocean hazard intelligence with trust scoring for emergency response."

### **Technical Highlights:**
- **FastAPI** - High-performance web framework
- **Multi-source ingestion** - Citizens + Social platforms
- **AI Analysis** - NLP keyword extraction, sentiment analysis
- **Trust Scoring** - Credibility-based decision support
- **Real-time Processing** - Instant hazard detection
- **Scalable Architecture** - Ready for production deployment

### **Impact:**
- 🚨 **Faster emergency response** through automated detection
- 🤖 **Reduced false alarms** via AI trust scoring
- 👥 **Citizen engagement** in coastal safety
- 📊 **Data-driven decisions** for authorities
- 🌊 **Protecting India's coastline** with technology

---

## ✅ **READY FOR DEMO!**

Your SeaSense AI Trust Engine is fully functional and ready for Smart India Hackathon 2025 demonstration!
