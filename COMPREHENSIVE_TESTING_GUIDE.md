# 🧪 SeaSense AI Trust Engine - Complete Testing Guide

## 📋 **Testing Overview**

This guide covers comprehensive testing for the SeaSense AI Trust Engine, including:
- **Backend API Testing** (AI Trust Engine)
- **Frontend Testing** (Dashboard)
- **Integration Testing** (End-to-End)
- **Manual Feature Testing**
- **Performance Testing**
- **Error Handling Testing**

---

## 🚀 **Quick Start Testing**

### 1. Setup and Start Both Systems
```bash
# Option 1: Use the automated script
python start_integrated_system.py

# Option 2: Manual setup
# Terminal 1 - Backend
cd ai_trust_engine
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload

# Terminal 2 - Frontend  
cd seasense-dashboard
npm run dev
```

### 2. Run Integration Tests
```bash
# Run the automated integration test
python test_integration.py

# Run dashboard connectivity test
python test_dashboard.py
```

---

## 🔧 **Backend API Testing**

### A. Health and System Tests

#### 1. Health Check
```bash
curl -X GET "http://127.0.0.1:8005/health"
```
**Expected Result:**
```json
{"status": "healthy", "ai_pipeline": "operational", "timestamp": "..."}
```

#### 2. API Documentation
- Open: `http://127.0.0.1:8005/docs`
- Verify interactive Swagger UI loads
- Test endpoints directly from Swagger

#### 3. Root Endpoint
```bash
curl -X GET "http://127.0.0.1:8005/"
```

### B. Citizen Reports Testing

#### 1. Submit Valid Report
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

#### 2. Test All Hazard Types
```bash
# High Waves
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{"reporter_name": "Tester", "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Test Location"}, "hazard_type": "high_waves", "description": "High waves test", "severity": "medium", "timestamp": "2025-09-15T10:30:00", "contact_info": "test@example.com"}'

# Pollution
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{"reporter_name": "Tester", "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Test Location"}, "hazard_type": "pollution", "description": "Oil spill detected", "severity": "high", "timestamp": "2025-09-15T10:30:00", "contact_info": "test@example.com"}'

# Dangerous Currents
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{"reporter_name": "Tester", "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Test Location"}, "hazard_type": "dangerous_currents", "description": "Strong undertow", "severity": "critical", "timestamp": "2025-09-15T10:30:00", "contact_info": "test@example.com"}'

# Marine Life
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{"reporter_name": "Tester", "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Test Location"}, "hazard_type": "marine_life", "description": "Jellyfish swarm", "severity": "medium", "timestamp": "2025-09-15T10:30:00", "contact_info": "test@example.com"}'
```

#### 3. Test Invalid Data
```bash
# Missing required fields
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{"reporter_name": "Test"}'

# Invalid hazard type
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{"reporter_name": "Test", "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Test"}, "hazard_type": "invalid_type", "description": "Test", "severity": "medium", "timestamp": "2025-09-15T10:30:00", "contact_info": "test@example.com"}'
```

#### 4. Check Report Status
```bash
# First submit a report and get the report_id, then:
curl -X GET "http://127.0.0.1:8005/api/v1/reports/status/citizen_1726423800000"
```

### C. Social Media Testing

#### 1. Submit Social Media Posts
```bash
# Twitter Post
curl -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Massive waves hitting Mumbai coastline! Everyone stay safe #tsunami #mumbai #waves",
    "platform": "twitter",
    "author_id": "@testuser",
    "author_followers": 1500,
    "author_verified": true,
    "likes": 45,
    "shares": 12,
    "comments": 8,
    "location": {"latitude": 19.0760, "longitude": 72.8777},
    "hashtags": ["tsunami", "mumbai", "waves"],
    "posted_at": "2025-09-15T11:00:00"
  }'

# Instagram Post
curl -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Oil spill at Goa beach 😢 Save our oceans! #pollution #goa #environment",
    "platform": "instagram",
    "author_id": "oceanlover123",
    "author_followers": 5000,
    "author_verified": false,
    "likes": 200,
    "shares": 50,
    "comments": 25,
    "location": {"latitude": 15.2993, "longitude": 74.124},
    "hashtags": ["pollution", "goa", "environment"],
    "posted_at": "2025-09-15T12:00:00"
  }'

# Facebook Post
curl -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Strong currents at Chennai Marina Beach today. Coast guard advisory issued. Stay safe everyone!",
    "platform": "facebook",
    "author_id": "chennai_coast_watch",
    "author_followers": 10000,
    "author_verified": true,
    "likes": 150,
    "shares": 75,
    "comments": 40,
    "location": {"latitude": 13.0827, "longitude": 80.2707},
    "hashtags": ["chennai", "safety", "coastguard"],
    "posted_at": "2025-09-15T13:00:00"
  }'
```

### D. Trust Score Testing

#### 1. Get Trust Score for Report
```bash
# Use a report_id from previous tests
curl -X GET "http://127.0.0.1:8005/api/v1/trust-scores/citizen_1726423800000"
```

#### 2. Calculate Trust Score
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/trust-scores/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "report": {
      "id": "test_report",
      "description": "High waves and dangerous conditions",
      "hazard_type": "high_waves",
      "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Mumbai"},
      "trust_score": 0,
      "priority": "high",
      "timestamp": "2025-09-15T10:30:00",
      "status": "pending",
      "source": "citizen"
    },
    "social_media_posts": [
      {
        "id": "sm1",
        "text": "Big waves at Mumbai beach #waves #mumbai",
        "platform": "twitter",
        "author_id": "@user1",
        "author_verified": true,
        "location": {"latitude": 19.0760, "longitude": 72.8777},
        "hashtags": ["waves", "mumbai"],
        "posted_at": "2025-09-15T10:00:00",
        "engagement_score": 0.8
      }
    ]
  }'
```

---

## 🖥️ **Frontend Dashboard Testing**

### A. Basic Functionality Tests

#### 1. Dashboard Loading
- Open: `http://localhost:3000`
- Check if all components load without errors
- Verify responsive design on different screen sizes

#### 2. Navigation Testing
- Test all navigation links
- Verify active states
- Check mobile menu functionality

#### 3. Real-time Updates
- Watch for automatic data refreshes (every 30 seconds)
- Check WebSocket connection status indicator
- Verify live data updates

### B. Component-Specific Tests

#### 1. Interactive Map
- **Location**: Check if map loads correctly
- **Markers**: Verify hazard markers appear
- **Colors**: Confirm trust-score-based color coding
- **Popups**: Click markers to see report details
- **Zoom**: Test zoom in/out functionality

#### 2. Reports Table
- **Data Display**: Check if reports are shown
- **Filtering**: Test filter by hazard type, status, priority
- **Sorting**: Test sorting by different columns
- **Pagination**: If applicable, test page navigation
- **Details**: Click on reports for detailed view

#### 3. Analytics Charts
- **Trust Score Distribution**: Verify chart displays
- **Hazard Type Breakdown**: Check pie/bar charts
- **Timeline**: Test temporal data visualization
- **Interactions**: Hover effects and tooltips

#### 4. Social Media Feed
- **Posts Display**: Check if social media posts appear
- **Trust Scores**: Verify trust score indicators
- **Platform Icons**: Confirm platform-specific styling
- **Real-time Updates**: Watch for new posts

#### 5. System Health Panel
- **Connection Status**: Green/Red indicator
- **API Status**: Backend connection health
- **Statistics**: Real-time metrics display

### C. Form Testing

#### 1. Report Submission Form
```javascript
// Test data for manual form entry:
{
  "Reporter Name": "John Doe",
  "Hazard Type": "High Waves",
  "Location": "Mumbai Beach, Maharashtra",
  "Latitude": "19.0760",
  "Longitude": "72.8777",
  "Description": "Dangerous wave conditions observed with strong currents",
  "Severity": "High",
  "Contact": "john@example.com"
}
```

#### 2. Form Validation
- Submit empty form (should show validation errors)
- Enter invalid coordinates (should show error)
- Try invalid email format
- Test required field validation

---

## 🔗 **Integration Testing**

### A. End-to-End Workflow Tests

#### 1. Complete Report Flow
1. **Submit Report**: Use dashboard form
2. **View in Table**: Check if report appears
3. **Check Map**: Verify marker on map
4. **Trust Score**: Confirm score calculation
5. **Backend Verification**: Check via API

#### 2. Social Media Integration
1. **Submit via API**: Post social media content
2. **Dashboard Update**: Check if appears in feed
3. **Trust Analysis**: Verify trust score
4. **Cross-Reference**: Check against reports

#### 3. Real-time Data Flow
1. **Submit Report**: Via API or form
2. **Live Update**: Watch dashboard update
3. **WebSocket**: Verify real-time connectivity
4. **Data Consistency**: Check data matches

### B. API Integration Tests

#### 1. Dashboard ↔ Backend Communication
```bash
# Run this while dashboard is open
python test_integration.py
```

#### 2. CORS Testing
- Open browser dev tools
- Submit forms from dashboard
- Check for CORS errors in console

#### 3. Error Handling
- Stop backend server
- Test dashboard graceful degradation
- Verify mock data fallback

---

## 🚨 **Error Testing & Edge Cases**

### A. Backend Error Testing

#### 1. Invalid JSON
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d 'invalid json'
```

#### 2. Wrong Content Type
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: text/plain" \
  -d 'some data'
```

#### 3. Large Payload
```bash
# Create a very long description
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{
    "reporter_name": "Test",
    "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Test"},
    "hazard_type": "high_waves",
    "description": "'$(printf 'A%.0s' {1..10000})'",
    "severity": "medium",
    "timestamp": "2025-09-15T10:30:00",
    "contact_info": "test@example.com"
  }'
```

### B. Frontend Error Testing

#### 1. Network Errors
- Disconnect internet
- Test offline behavior
- Check error messages

#### 2. Backend Unavailable
- Stop backend server
- Use dashboard
- Verify graceful fallback

#### 3. Invalid Data
- Manipulate browser storage
- Test with corrupted data
- Check error recovery

---

## ⚡ **Performance Testing**

### A. Backend Performance

#### 1. Load Testing
```bash
# Install apache bench
brew install httpd  # macOS

# Test health endpoint
ab -n 1000 -c 10 http://127.0.0.1:8005/health

# Test report submission
ab -n 100 -c 5 -T 'application/json' -p report_data.json http://127.0.0.1:8005/api/v1/reports/citizen
```

#### 2. Response Time Testing
```bash
# Time individual requests
time curl -X GET "http://127.0.0.1:8005/health"
time curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" -H "Content-Type: application/json" -d '@report_data.json'
```

### B. Frontend Performance

#### 1. Browser Performance
- Open Chrome DevTools → Performance
- Record dashboard usage
- Check for performance issues
- Monitor memory usage

#### 2. Network Performance
- Open DevTools → Network
- Check request/response times
- Monitor data transfer sizes
- Test on slow connections

---

## 📝 **Manual Testing Checklist**

### ✅ **Backend API Tests**
- [ ] Health check responds
- [ ] API documentation loads
- [ ] Citizen report submission works
- [ ] All hazard types accepted
- [ ] Social media ingestion works
- [ ] Trust score calculation works
- [ ] Error handling works
- [ ] CORS headers present

### ✅ **Frontend Dashboard Tests**
- [ ] Dashboard loads without errors
- [ ] Navigation works
- [ ] Interactive map displays
- [ ] Reports table shows data
- [ ] Analytics charts render
- [ ] Social media feed works
- [ ] Forms submit successfully
- [ ] Real-time updates work
- [ ] Mobile responsive design
- [ ] Error states display properly

### ✅ **Integration Tests**
- [ ] Dashboard connects to backend
- [ ] Report submission end-to-end
- [ ] Real-time data synchronization
- [ ] Trust scores update live
- [ ] Social media integration works
- [ ] Error handling graceful
- [ ] Performance acceptable

### ✅ **Edge Cases**
- [ ] Backend offline handling
- [ ] Invalid data handling
- [ ] Network error recovery
- [ ] Large data payloads
- [ ] Concurrent user simulation
- [ ] Data consistency checks

---

## 🔍 **Debugging & Troubleshooting**

### Common Issues and Solutions

#### 1. Backend Not Starting
```bash
# Check Python environment
python --version
pip list | grep -E "(fastapi|uvicorn)"

# Install dependencies
pip install -r ai_trust_engine/requirements.txt

# Start with verbose logging
cd ai_trust_engine
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload --log-level debug
```

#### 2. Frontend Not Loading
```bash
# Check Node.js and npm
node --version
npm --version

# Install dependencies
cd seasense-dashboard
npm install

# Clear cache and restart
rm -rf .next node_modules
npm install
npm run dev
```

#### 3. CORS Issues
- Check browser console for CORS errors
- Verify `ALLOWED_ORIGINS` in backend settings
- Ensure frontend URL matches allowed origins

#### 4. WebSocket Connection Issues
- Check browser console for WebSocket errors
- Verify WebSocket URL configuration
- Test with WebSocket simulation mode

#### 5. API Response Issues
- Check backend logs for errors
- Verify request format matches API schema
- Test with Postman or curl first

---

## 📊 **Test Data Sets**

### Sample Report Data
```json
{
  "high_severity_reports": [
    {
      "reporter_name": "Coast Guard Officer",
      "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Mumbai Marine Drive"},
      "hazard_type": "high_waves",
      "description": "Extremely dangerous wave conditions. Multiple rescue operations in progress. Immediate evacuation advised.",
      "severity": "critical",
      "timestamp": "2025-09-15T10:30:00",
      "contact_info": "coastguard@mumbai.gov.in"
    }
  ],
  "medium_severity_reports": [
    {
      "reporter_name": "Local Fisherman",
      "location": {"latitude": 15.2993, "longitude": 74.124, "address": "Goa Fishing Harbor"},
      "hazard_type": "pollution",
      "description": "Oil spill detected near fishing area. Fish population affected.",
      "severity": "medium",
      "timestamp": "2025-09-15T11:00:00",
      "contact_info": "fisherman@goa.com"
    }
  ]
}
```

### Sample Social Media Data
```json
{
  "twitter_posts": [
    {
      "text": "Huge waves at Mumbai beach! Stay safe everyone 🌊 #MumbaiWeather #SafetyFirst",
      "platform": "twitter",
      "author_id": "@mumbai_weather",
      "author_followers": 50000,
      "author_verified": true,
      "likes": 500,
      "shares": 200,
      "comments": 100,
      "location": {"latitude": 19.0760, "longitude": 72.8777},
      "hashtags": ["MumbaiWeather", "SafetyFirst"],
      "posted_at": "2025-09-15T09:30:00"
    }
  ]
}
```

---

## 🎯 **Testing Automation**

### Create Test Scripts

#### 1. Backend Test Script
```bash
# Create comprehensive_backend_test.sh
#!/bin/bash
echo "Testing SeaSense Backend..."

# Health check
curl -s -X GET "http://127.0.0.1:8005/health" | jq '.'

# Submit test reports
curl -s -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d @test_data/citizen_report.json | jq '.'

# Submit social media
curl -s -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
  -H "Content-Type: application/json" \
  -d @test_data/social_media.json | jq '.'

echo "Backend testing complete!"
```

#### 2. Frontend Test Commands
```bash
# Dashboard accessibility test
npm run build
npm run start

# Component testing (if using testing framework)
npm test

# E2E testing (if Playwright/Cypress configured)
npm run test:e2e
```

---

This comprehensive testing guide covers every aspect of the SeaSense AI Trust Engine. Start with the Quick Start section, then work through each category based on what you want to test. The manual testing checklist ensures you don't miss any critical functionality.
