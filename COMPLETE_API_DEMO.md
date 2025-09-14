# 🚀 SeaSense AI Trust Engine - Complete API Demo Guide

## 📋 **Quick Reference**

**Base URL**: `http://127.0.0.1:8005`  
**API Documentation**: `http://127.0.0.1:8005/docs`  
**Health Check**: `http://127.0.0.1:8005/health`

---

## 🎯 **All API Endpoints**

### **1. Health Check**
```bash
curl -X GET "http://127.0.0.1:8005/health"
```
**Expected Response:**
```json
{"status": "healthy", "timestamp": "2025-09-14T18:14:11.481Z"}
```

---

### **2. Submit Citizen Report**
**Endpoint**: `POST /api/v1/reports/citizen`

#### ✅ **CORRECT Format:**
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{
    "reporter_name": "John Doe",
    "location": {
      "latitude": 19.0760,
      "longitude": 72.8777,
      "address": "Mumbai Beach, Maharashtra"
    },
    "hazard_type": "high_waves",
    "description": "Observed dangerous wave conditions at the beach. Several people were struggling in the water.",
    "severity": "high",
    "timestamp": "2025-09-14T10:30:00",
    "contact_info": "john.doe@email.com"
  }'
```

#### 🎯 **Key Requirements:**
- **hazard_type** must be one of: `tsunami`, `storm`, `high_waves`, `pollution`, `debris`, `unusual_current`, `temperature_anomaly`, `other`
- **location** must be an object with `latitude`, `longitude`, `address`
- **severity** must be: `low`, `medium`, `high`, `critical`

#### 📝 **Expected Response:**
```json
{
  "report_id": "citizen_1726340651481",
  "status": "received",
  "trust_score": 75.5,
  "message": "Citizen report processed successfully",
  "analysis": {
    "keywords": ["dangerous", "wave", "water"],
    "risk_level": "high",
    "credibility": "good"
  }
}
```

---

### **3. Submit Social Media Post**
**Endpoint**: `POST /api/v1/social-media/ingest`

#### ✅ **CORRECT Format:**
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Massive waves hitting the Mumbai coastline! Everyone stay away from the beach today. #safety #tsunami #mumbai",
    "platform": "twitter",
    "author_id": "@oceanwatcher",
    "author_followers": 1500,
    "author_verified": false,
    "likes": 45,
    "shares": 12,
    "comments": 8,
    "location": {
      "latitude": 19.0760,
      "longitude": 72.8777
    },
    "hashtags": ["safety", "tsunami", "mumbai"],
    "posted_at": "2025-09-14T11:00:00"
  }'
```

#### 🎯 **Key Requirements:**
- **platform** must be a string (e.g., "twitter", "facebook", "instagram")
- **text** is the post content
- **author_id** is the user identifier 
- **posted_at** must be ISO datetime format
- **likes**, **shares**, **comments** are separate fields (not nested in engagement)

#### 📝 **Expected Response:**
```json
{
  "success": true,
  "message": "Social media post processed successfully",
  "data": {
    "post_id": "e6a4555e-de9f-47ea-b5e3-6bee130fc630",
    "platform": "twitter",
    "analysis": {
      "text_analysis": {
        "language": "en",
        "language_confidence": 0.9,
        "sentiment": {
          "POSITIVE": 0.0,
          "NEGATIVE": 1.0,
          "NEUTRAL": 0.0
        },
        "word_count": 16
      },
      "hazard_analysis": {
        "predicted_hazard": "tsunami",
        "confidence": 0.25,
        "all_scores": {
          "tsunami": 0.25,
          "storm": 0.0,
          "high_waves": 0.2,
          "pollution": 0.0,
          "debris": 0.0,
          "unusual_current": 0.0,
          "temperature_anomaly": 0.0,
          "other": 0.0
        }
      },
      "image_analysis": {},
      "engagement_score": 1.0,
      "credibility_score": 0.51,
      "has_location": true
    }
  },
  "errors": [],
  "processing_time": 0.0
}
```

---

### **4. Get Trust Score**
**Endpoint**: `GET /api/v1/trust-scores/{report_id}`

#### ✅ **Example:**
```bash
curl -X GET "http://127.0.0.1:8005/api/v1/trust-scores/9a870f17-6025-4557-9b1f-a6824e246b00"
```

#### 📝 **Expected Response:**
```json
{
  "report_id": "citizen_1726340651481",
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

## 🚨 **Common Errors & Fixes**

### **Error 1: Invalid hazard_type**
❌ **Wrong:**
```json
"hazard_type": "High waves and strong currents"
```
✅ **Correct:**
```json
"hazard_type": "high_waves"
```

### **Error 2: Invalid location format**
❌ **Wrong:**
```json
"location": "Mumbai Beach, Maharashtra"
```
✅ **Correct:**
```json
"location": {
  "latitude": 19.0760,
  "longitude": 72.8777,
  "address": "Mumbai Beach, Maharashtra"
}
```

### **Error 3: JSON Syntax Error**
❌ **Wrong:**
```json
{
  "severity": "high",
}"contact_info": "john.doe@email.com"
```
✅ **Correct:**
```json
{
  "severity": "high",
  "contact_info": "john.doe@email.com"
}
```

---

## 🎬 **Demo Script for SIH 2025**

### **Step 1: Start Demo**
```bash
# Check if server is running
curl -X GET "http://127.0.0.1:8005/health"
```

### **Step 2: Citizen Report Demo**
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{
    "reporter_name": "Priya Sharma",
    "location": {
      "latitude": 15.2993,
      "longitude": 74.1240,
      "address": "Goa Beach, Goa"
    },
    "hazard_type": "tsunami",
    "description": "Urgent! Water suddenly receded from the beach exposing the sea floor. This is a clear tsunami warning sign!",
    "severity": "critical",
    "timestamp": "2025-09-14T14:30:00",
    "contact_info": "priya.sharma@gmail.com"
  }'
```

### **Step 3: Social Media Demo**
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "BREAKING: Sea water receding rapidly at Goa beach! This could be tsunami warning! Evacuate immediately! #TsunamiAlert #GoaEmergency",
    "platform": "twitter",
    "author_id": "@CoastalAlert",
    "author_followers": 50000,
    "author_verified": true,
    "likes": 250,
    "shares": 89,
    "comments": 45,
    "location": {
      "latitude": 15.2993,
      "longitude": 74.1240
    },
    "hashtags": ["TsunamiAlert", "GoaEmergency"],
    "posted_at": "2025-09-14T14:32:00"
  }'
```

### **Step 4: Trust Score Analysis**
```bash
# Use the report_id from previous responses
curl -X GET "http://127.0.0.1:8005/api/v1/trust-scores/citizen_[REPORT_ID]"
```

---

## 🔧 **Testing Tools**

### **1. Browser Testing**
- **API Docs**: `http://127.0.0.1:8005/docs`
- **Health**: `http://127.0.0.1:8005/health`

### **2. Postman Collection**
Import the `SeaSense_API_Collection.json` file for one-click testing.

### **3. Python Testing**
```python
import requests

# Test citizen report
response = requests.post("http://127.0.0.1:8005/api/v1/reports/citizen", json={
    "reporter_name": "Test User",
    "location": {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "address": "Mumbai Beach"
    },
    "hazard_type": "high_waves",
    "description": "Test report",
    "severity": "medium",
    "timestamp": "2025-09-14T15:00:00",
    "contact_info": "test@example.com"
})
print(response.json())
```

---

## ✅ **Success Indicators**

- ✅ **Status Code 200**: Request successful
- ✅ **Trust Score Generated**: AI analysis working
- ✅ **Report ID Returned**: Data stored correctly
- ✅ **Keywords Extracted**: NLP processing active
- ✅ **Risk Assessment**: Decision engine functioning

---

## 🎯 **For SIH Judges Demo**

1. **Show Health Check** - Proves system is live
2. **Submit Citizen Report** - Shows citizen engagement
3. **Submit Social Media** - Shows multi-source analysis
4. **Get Trust Scores** - Shows AI decision making
5. **Explain Analysis** - Shows keyword extraction, risk assessment

**Key Message**: "Our AI Trust Engine processes multiple data sources, analyzes credibility, and provides actionable intelligence for ocean hazard management."
