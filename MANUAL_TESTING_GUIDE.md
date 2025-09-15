# 🚀 SeaSense Testing - Step-by-Step Manual Guide

## 🎯 Quick Testing Setup

### Step 1: Start Both Systems

**Terminal 1 - Backend:**
```bash
cd /Users/user46/dev/seasense-ai-trust-engine/ai_trust_engine
python3 -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload
```

**Terminal 2 - Frontend:**
```bash
cd /Users/user46/dev/seasense-ai-trust-engine/seasense-dashboard
npm run dev
```

### Step 2: Verify Basic Connectivity

**Browser Tests:**
1. Open `http://localhost:3000` - Dashboard should load
2. Open `http://127.0.0.1:8005/docs` - API documentation should load
3. Open `http://127.0.0.1:8005/health` - Should show health status

---

## 🧪 **Functionality Testing Checklist**

### ✅ **Backend API Testing**

#### A. Health Check
```bash
curl -X GET "http://127.0.0.1:8005/health"
```
**Expected:** `{"status": "healthy", "ai_pipeline": "operational", ...}`

#### B. Citizen Report Submission
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
  -H "Content-Type: application/json" \
  -d '{
    "reporter_name": "John Doe",
    "location": {
      "latitude": 19.0760,
      "longitude": 72.8777,
      "address": "Mumbai Beach"
    },
    "hazard_type": "high_waves",
    "description": "Dangerous wave conditions observed",
    "severity": "high",
    "timestamp": "2025-09-15T10:30:00",
    "contact_info": "john@example.com"
  }'
```
**Expected:** JSON response with `report_id`, `trust_score`, and analysis

#### C. Social Media Ingestion
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Huge waves at Mumbai beach! #safety #mumbai",
    "platform": "twitter",
    "author_id": "@user123",
    "author_followers": 1000,
    "author_verified": true,
    "likes": 50,
    "shares": 10,
    "comments": 5,
    "location": {"latitude": 19.0760, "longitude": 72.8777},
    "hashtags": ["safety", "mumbai"],
    "posted_at": "2025-09-15T11:00:00"
  }'
```
**Expected:** JSON response with social media analysis and trust score

#### D. Trust Score Calculation
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/trust-scores/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "report": {
      "id": "test_report",
      "description": "High waves test",
      "hazard_type": "high_waves",
      "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Mumbai"},
      "trust_score": 0,
      "priority": "high",
      "timestamp": "2025-09-15T10:30:00",
      "status": "pending",
      "source": "citizen"
    },
    "social_media_posts": []
  }'
```
**Expected:** Detailed trust score breakdown

---

### ✅ **Frontend Dashboard Testing**

#### A. Dashboard Loading Test
1. **Open:** `http://localhost:3000`
2. **Check:** 
   - Dashboard loads without errors
   - Navigation works
   - All components visible

#### B. Interactive Map Test
1. **Location:** Find the interactive map component
2. **Check:**
   - Map renders properly
   - Markers appear (if any data exists)
   - Click interactions work
   - Zoom functionality works

#### C. Reports Table Test
1. **Location:** Find the reports table/list
2. **Check:**
   - Table displays data (real or mock)
   - Sorting works (click column headers)
   - Filtering works (if available)
   - Details view works (click on report)

#### D. Analytics Charts Test
1. **Location:** Find analytics/charts section
2. **Check:**
   - Charts render properly
   - Data visualization works
   - Interactive elements work
   - Responsive design

#### E. Social Media Feed Test
1. **Location:** Find social media feed component
2. **Check:**
   - Posts display properly
   - Trust scores show
   - Platform icons appear
   - Scrolling works

#### F. Real-time Updates Test
1. **Check:** Connection status indicator
2. **Wait:** 30 seconds for automatic updates
3. **Submit:** New report via API
4. **Verify:** Dashboard updates with new data

---

### ✅ **Integration Testing**

#### A. End-to-End Report Flow
1. **Submit Report:** Use dashboard form OR API
2. **Check Table:** Verify report appears in table
3. **Check Map:** Verify marker appears on map
4. **Check Trust Score:** Verify score calculation
5. **Check Analytics:** Verify charts update

#### B. Real-time Data Flow
1. **Open Dashboard:** Keep browser tab open
2. **Submit Data:** Via API in another terminal
3. **Watch Dashboard:** Should update automatically
4. **Check Console:** No errors in browser dev tools

#### C. Error Handling Test
1. **Stop Backend:** Kill backend server
2. **Use Dashboard:** Should show graceful error handling
3. **Check Mock Data:** Should fall back to mock data
4. **Restart Backend:** Should reconnect automatically

---

## 🔧 **Manual Testing Workflows**

### Workflow 1: Complete Citizen Report Submission
1. Open dashboard at `http://localhost:3000`
2. Find report submission form
3. Fill in test data:
   - Reporter: "Test User"
   - Location: "Mumbai Beach"
   - Coordinates: 19.0760, 72.8777
   - Hazard: "High Waves"
   - Description: "Test dangerous conditions"
   - Severity: "High"
4. Submit form
5. Check if report appears in:
   - Reports table
   - Map markers
   - Analytics charts

### Workflow 2: Social Media Analysis
1. Submit social media post via API (see commands above)
2. Check dashboard social media feed
3. Verify trust score appears
4. Check if related to any reports

### Workflow 3: Trust Score Analysis
1. Submit report with detailed description
2. Wait for AI processing
3. Check trust score in dashboard
4. View detailed trust factors (if available)
5. Test with different hazard types

### Workflow 4: Real-time Monitoring
1. Open dashboard
2. Open browser dev tools → Console
3. Watch for WebSocket messages
4. Submit new data via API
5. Verify dashboard updates automatically

---

## 🐛 **Common Issues & Solutions**

### Backend Issues
- **Port 8005 in use:** Kill existing process or use different port
- **Module not found:** Run `pip install -r requirements.txt`
- **CORS errors:** Check ALLOWED_ORIGINS in settings

### Frontend Issues
- **Port 3000 in use:** Kill existing Next.js process
- **Dependencies missing:** Run `npm install`
- **Build errors:** Check for TypeScript errors

### Integration Issues
- **API not connecting:** Verify backend URL in frontend config
- **Data not updating:** Check WebSocket connection
- **CORS blocking:** Ensure backend allows frontend origin

---

## 📊 **Success Criteria**

### ✅ **All Tests Pass When:**
- Backend health endpoint responds ✅
- API documentation loads ✅
- Citizen reports submit successfully ✅
- Social media ingestion works ✅
- Trust scores calculate properly ✅
- Dashboard loads without errors ✅
- Map displays correctly ✅
- Charts render properly ✅
- Real-time updates work ✅
- Form submissions work ✅
- Error handling graceful ✅

### 📈 **Performance Benchmarks:**
- API response time < 2 seconds
- Dashboard load time < 3 seconds
- Real-time updates < 5 seconds
- No memory leaks in browser
- No console errors

---

## 🎯 **Advanced Testing**

### Load Testing
```bash
# Install apache bench
brew install httpd

# Test API endpoints
ab -n 100 -c 10 http://127.0.0.1:8005/health
```

### Security Testing
- Test with invalid JSON
- Test with missing fields
- Test with XSS payloads
- Test CORS headers
- Test authentication (if implemented)

### Browser Compatibility
- Test in Chrome, Firefox, Safari
- Test mobile responsiveness
- Test different screen sizes
- Test with disabled JavaScript

---

## 📝 **Test Results Documentation**

Keep track of:
- ✅ Working features
- ❌ Broken features  
- ⚠️ Partial functionality
- 🐛 Bugs found
- 📈 Performance metrics
- 🔄 Areas needing improvement

---

**Ready to test? Start with Step 1 and work through each section systematically!** 🚀
