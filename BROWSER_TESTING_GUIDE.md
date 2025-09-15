# 🌐 SeaSense Dashboard - Browser Testing Guide

## 🚀 Getting Started

### Prerequisites
1. **Backend Running:** `http://127.0.0.1:8005`
2. **Frontend Running:** `http://localhost:3000`
3. **Browser:** Chrome, Firefox, or Safari

---

## 📋 **Dashboard Component Testing**

### 1. **Main Dashboard Page**
**URL:** `http://localhost:3000`

#### Visual Checklist:
- [ ] Page loads without errors
- [ ] Navigation bar appears
- [ ] All components render properly
- [ ] No console errors (press F12 → Console)
- [ ] Responsive design (try different window sizes)

#### Interactive Elements:
- [ ] Navigation links work
- [ ] Mobile menu works (if on mobile)
- [ ] Theme switching (if available)
- [ ] Connection status indicator

---

### 2. **Interactive Map Component**

#### Visual Tests:
- [ ] Map renders correctly
- [ ] Map tiles load properly
- [ ] Zoom controls work
- [ ] Pan/drag functionality works

#### Data Tests:
- [ ] Hazard markers appear (red/yellow/green dots)
- [ ] Marker colors represent trust scores
- [ ] Click on markers shows popups
- [ ] Popup shows report details

#### Test Data Creation:
1. Submit a report via API or form
2. Check if marker appears on map
3. Click marker to see details
4. Verify location accuracy

---

### 3. **Reports Table/List**

#### Display Tests:
- [ ] Table shows report data
- [ ] Columns are properly formatted
- [ ] Trust scores display with colors
- [ ] Timestamps are readable
- [ ] Status indicators work

#### Interaction Tests:
- [ ] Sort by clicking column headers
- [ ] Filter by hazard type (if available)
- [ ] Filter by status (if available)
- [ ] Click on report for details
- [ ] Pagination works (if applicable)

#### Test Steps:
1. Look for reports table
2. Try sorting by different columns
3. Click on a report to see details
4. Test any filter options

---

### 4. **Analytics/Charts Section**

#### Chart Types to Test:
- [ ] Trust score distribution chart
- [ ] Hazard type breakdown (pie/bar chart)
- [ ] Timeline/trend charts
- [ ] System metrics

#### Interactive Features:
- [ ] Hover effects show details
- [ ] Click to filter data
- [ ] Zoom in/out on charts
- [ ] Legend interactions

#### Test Steps:
1. Locate analytics section
2. Hover over chart elements
3. Try clicking on chart segments
4. Check for tooltips and legends

---

### 5. **Social Media Feed**

#### Display Elements:
- [ ] Social media posts appear
- [ ] Platform icons (Twitter, Instagram, Facebook)
- [ ] Trust scores for posts
- [ ] Post content readable
- [ ] Timestamps displayed

#### Interactive Features:
- [ ] Scroll through posts
- [ ] Click for post details
- [ ] Trust score indicators work
- [ ] Real-time updates (new posts appear)

---

### 6. **Report Submission Form** (if available)

#### Form Fields:
- [ ] Reporter name input
- [ ] Location input (address)
- [ ] Latitude/longitude inputs
- [ ] Hazard type dropdown
- [ ] Description textarea
- [ ] Severity selection
- [ ] Contact information

#### Validation Tests:
- [ ] Submit empty form (should show errors)
- [ ] Invalid email format
- [ ] Invalid coordinates
- [ ] Required field validation
- [ ] Character limits

#### Successful Submission:
1. Fill all required fields with valid data
2. Submit form
3. Check for success message
4. Verify report appears in table/map

---

### 7. **Real-time Updates**

#### WebSocket Connection:
- [ ] Connection status indicator (green = connected)
- [ ] Real-time data updates
- [ ] No connection errors in console

#### Test Steps:
1. Keep dashboard open
2. Submit data via API in terminal
3. Watch for automatic updates
4. Check timestamp of last update

---

## 🔧 **Browser Developer Tools Testing**

### Console Tab (F12 → Console)
**Look for:**
- [ ] No JavaScript errors
- [ ] No failed network requests
- [ ] WebSocket connection messages
- [ ] API response logs

### Network Tab (F12 → Network)
**Check:**
- [ ] API requests succeed (200 status)
- [ ] Response times reasonable (<2s)
- [ ] No CORS errors
- [ ] WebSocket connection established

### Performance Tab (F12 → Performance)
**Test:**
- [ ] Page load time reasonable
- [ ] No memory leaks
- [ ] Smooth animations
- [ ] Efficient rendering

---

## 📱 **Mobile Testing**

### Responsive Design:
- [ ] Mobile layout works
- [ ] Touch interactions work
- [ ] Maps work on mobile
- [ ] Forms usable on mobile
- [ ] Navigation accessible

### Test Different Sizes:
1. Desktop (1920x1080)
2. Tablet (768x1024)
3. Mobile (375x667)
4. Large screen (2560x1440)

---

## 🧪 **Feature-Specific Tests**

### Test Scenario 1: End-to-End Report Flow
1. **Submit Report:**
   ```bash
   curl -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
     -H "Content-Type: application/json" \
     -d '{
       "reporter_name": "Browser Test User",
       "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Mumbai Test"},
       "hazard_type": "high_waves",
       "description": "Browser testing dangerous wave conditions",
       "severity": "high",
       "timestamp": "2025-09-15T10:30:00",
       "contact_info": "test@browser.com"
     }'
   ```

2. **Check Dashboard:**
   - [ ] Report appears in table
   - [ ] Marker appears on map
   - [ ] Charts update
   - [ ] Real-time update happens

### Test Scenario 2: Social Media Integration
1. **Submit Social Post:**
   ```bash
   curl -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Browser test: Big waves at Mumbai! #test #mumbai",
       "platform": "twitter",
       "author_id": "@browsertest",
       "author_followers": 100,
       "author_verified": false,
       "likes": 5,
       "shares": 1,
       "comments": 0,
       "location": {"latitude": 19.0760, "longitude": 72.8777},
       "hashtags": ["test", "mumbai"],
       "posted_at": "2025-09-15T12:00:00"
     }'
   ```

2. **Check Dashboard:**
   - [ ] Post appears in social feed
   - [ ] Trust score displayed
   - [ ] Platform icon correct

### Test Scenario 3: Error Handling
1. **Stop Backend Server**
2. **Use Dashboard:**
   - [ ] Shows connection error
   - [ ] Falls back to mock data
   - [ ] No crashes or white screens
   - [ ] Graceful error messages

3. **Restart Backend:**
   - [ ] Automatically reconnects
   - [ ] Data updates resume
   - [ ] No need to refresh page

---

## 🎯 **Success Criteria**

### ✅ **Dashboard is Working When:**
- All components load without errors
- Interactive map displays and responds
- Reports table shows data and sorts
- Charts render and update
- Social media feed displays posts
- Real-time updates work
- Forms submit successfully
- Mobile layout is usable
- No console errors
- Performance is acceptable

### ⚠️ **Common Issues:**
- **Blank page:** Check console for errors
- **No data:** Verify backend connection
- **Map not loading:** Check network requests
- **Charts not rendering:** Check for JavaScript errors
- **Forms not submitting:** Check API connectivity

---

## 📊 **Test Results Template**

```
SeaSense Dashboard Test Results
==============================
Date: ___________
Browser: ___________
Screen Size: ___________

✅ ❌ Page Loading
✅ ❌ Navigation
✅ ❌ Interactive Map
✅ ❌ Reports Table
✅ ❌ Analytics Charts
✅ ❌ Social Media Feed
✅ ❌ Forms
✅ ❌ Real-time Updates
✅ ❌ Mobile Responsive
✅ ❌ Error Handling

Issues Found:
- ___________________
- ___________________

Performance Notes:
- Load time: ______
- Responsiveness: ______
- Memory usage: ______
```

---

## 🚀 **Quick Testing Commands**

### Test Data for Manual Entry:
```
Reporter: "Dashboard Tester"
Location: "Mumbai Marine Drive"
Latitude: 19.0760
Longitude: 72.8777
Hazard: High Waves
Description: "Manual testing of dashboard functionality"
Severity: High
Contact: "tester@dashboard.com"
```

### Browser Console Commands:
```javascript
// Check for errors
console.clear();

// Monitor WebSocket
console.log('WebSocket status:', window.WebSocket);

// Check API connectivity
fetch('http://127.0.0.1:8005/health')
  .then(r => r.json())
  .then(console.log);
```

---

**Start with opening `http://localhost:3000` and work through each section systematically!** 🌊
