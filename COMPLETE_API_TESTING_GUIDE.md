# 🚀 Complete API Testing Guide - SeaSense AI Trust Engine

## 📋 **Quick Overview**
Your AI Trust Engine has **4 main endpoints** for processing ocean hazard data:

| Endpoint | Purpose | Input | Output |
|----------|---------|-------|--------|
| `/health` | Server status | None | Health check |
| `/api/v1/reports/citizen` | Process citizen reports | Report data | Trust score + analysis |
| `/api/v1/reports/social-media` | Process social media posts | Post data | Trust score + analysis |
| `/api/v1/trust-scores/{id}` | Get trust score by ID | Report ID | Detailed trust analysis |

---

## 🏥 **1. Health Check Endpoint**

### **Purpose:** Verify server is running
### **URL:** `GET /health`

### **Test:**
```bash
curl -X GET "http://127.0.0.1:8005/health"
```

### **Expected Response:**
```json
{
  "status": "healthy",
  "message": "AI Trust Engine is running",
  "timestamp": "2025-09-14T10:30:45.123456"
}
```

---

## 📱 **2. Citizen Report Endpoint**

### **Purpose:** Process citizen-submitted ocean hazard reports
### **URL:** `POST /api/v1/reports/citizen`

### **Input Format:**
```json
{
  "reporter_name": "John Doe",
  "location": "Mumbai Beach, Maharashtra",
  "hazard_type": "High waves and strong currents",
  "description": "Observed dangerous wave conditions at the beach. Several people were struggling in the water.",
  "severity": "high",
  "timestamp": "2025-09-14T10:30:00",
  "contact_info": "john.doe@email.com"
}
```

### **Test with curl:**
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{
    "reporter_name": "John Doe",
    "location": "Mumbai Beach, Maharashtra", 
    "hazard_type": "High waves and strong currents",
    "description": "Observed dangerous wave conditions at the beach. Several people were struggling in the water.",
    "severity": "high",
    "timestamp": "2025-09-14T10:30:00",
    "contact_info": "john.doe@email.com"
  }'
```

### **Expected Response:**
```json
{
  "report_id": "citizen_report_20250914103045",
  "trust_score": 0.85,
  "confidence_level": "high",
  "risk_assessment": "high",
  "analysis": {
    "sentiment": "concerned",
    "keywords_found": ["dangerous", "waves", "currents", "struggling"],
    "location_verified": true,
    "urgency_level": "immediate"
  },
  "status": "processed",
  "processed_at": "2025-09-14T10:30:45.123456"
}
```

---

## 📱 **3. Social Media Endpoint**

### **Purpose:** Process social media posts about ocean hazards
### **URL:** `POST /api/v1/reports/social-media`

### **Input Format:**
```json
{
  "platform": "twitter",
  "username": "beachsafety_mumbai",
  "content": "WARNING: Extremely rough seas at Juhu Beach today. Coast Guard advising all swimmers to stay out of water. Multiple rescue operations ongoing. #MumbaiBeach #Safety",
  "location": "Juhu Beach, Mumbai",
  "timestamp": "2025-09-14T09:15:00",
  "engagement_metrics": {
    "likes": 150,
    "shares": 45,
    "comments": 23
  }
}
```

### **Test with curl:**
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/social-media" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "twitter",
    "username": "beachsafety_mumbai",
    "content": "WARNING: Extremely rough seas at Juhu Beach today. Coast Guard advising all swimmers to stay out of water. Multiple rescue operations ongoing. #MumbaiBeach #Safety",
    "location": "Juhu Beach, Mumbai",
    "timestamp": "2025-09-14T09:15:00",
    "engagement_metrics": {
      "likes": 150,
      "shares": 45,
      "comments": 23
    }
  }'
```

### **Expected Response:**
```json
{
  "post_id": "social_post_20250914091545",
  "trust_score": 0.92,
  "confidence_level": "very_high",
  "risk_assessment": "critical",
  "analysis": {
    "sentiment": "urgent_warning",
    "keywords_found": ["WARNING", "rough seas", "Coast Guard", "rescue"],
    "credibility_score": 0.95,
    "engagement_impact": "high",
    "source_reliability": "official"
  },
  "status": "processed",
  "processed_at": "2025-09-14T09:15:45.123456"
}
```

---

## 🔍 **4. Trust Score Lookup Endpoint**

### **Purpose:** Get detailed trust analysis for a specific report
### **URL:** `GET /api/v1/trust-scores/{report_id}`

### **Test with curl:**
```bash
curl -X GET "http://127.0.0.1:8005/api/v1/trust-scores/citizen_report_20250914103045"
```

### **Expected Response:**
```json
{
  "report_id": "citizen_report_20250914103045",
  "trust_score": 0.85,
  "confidence_level": "high",
  "detailed_analysis": {
    "content_analysis": {
      "sentiment": "concerned",
      "keywords_found": ["dangerous", "waves", "currents", "struggling"],
      "emotional_indicators": ["fear", "urgency"]
    },
    "source_analysis": {
      "reporter_credibility": 0.8,
      "location_verification": true,
      "timestamp_consistency": true
    },
    "risk_factors": {
      "severity_level": "high",
      "immediate_danger": true,
      "requires_action": true
    }
  },
  "recommendations": [
    "Immediate coast guard notification",
    "Beach closure advisory",
    "Public safety alert"
  ],
  "processed_at": "2025-09-14T10:30:45.123456"
}
```

---

## 🧪 **Quick Test Script**

Let me create a comprehensive test script for you:
