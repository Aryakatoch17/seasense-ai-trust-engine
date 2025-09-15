# 🌊 SeaSense AI Trust Engine - Complete Integration Guide

## 🎯 Integration Overview

This integration connects the **SeaSense AI Trust Engine** (backend) with the **SeaSense Dashboard** (frontend) to create a complete ocean hazard monitoring and trust scoring system.

## 🚀 Quick Start - Integrated System

### Option 1: Automated Integration (Recommended)
```bash
# Start both backend and frontend with integration
python start_integrated_system.py
```

### Option 2: Manual Integration Setup
```bash
# Terminal 1: Start Backend
cd ai_trust_engine
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload

# Terminal 2: Start Frontend
cd seasense-dashboard
npm install
npm run dev
```

## 🔗 Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SeaSense Integration                     │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Next.js Dashboard)                              │
│  ├── Interactive Maps & Analytics                          │
│  ├── Real-time Data Visualization                          │
│  ├── Report Management Interface                           │
│  └── Social Media Monitoring                               │
│                        │                                   │
│                   API Calls                                │
│                        │                                   │
│  Backend (FastAPI Trust Engine)                            │
│  ├── /api/v1/reports/* - Citizen Reports                  │
│  ├── /api/v1/trust-scores/* - Trust Scoring               │
│  ├── /api/v1/social-media/* - Social Media Processing     │
│  └── /health - System Health                               │
│                        │                                   │
│  AI Pipeline                                               │
│  ├── Hazard Classification                                 │
│  ├── Trust Score Calculation                               │
│  ├── Duplicate Detection                                   │
│  └── Content Analysis                                      │
└─────────────────────────────────────────────────────────────┘
```

## 📡 API Integration Points

### ✅ Active Integrations

#### 1. Health Monitoring
- **Endpoint**: `GET /health`
- **Purpose**: System status and connectivity check
- **Integration**: Dashboard connection indicator

#### 2. Citizen Reports
- **Submit**: `POST /api/v1/reports/citizen`
- **Status**: `GET /api/v1/reports/status/{report_id}`
- **Integration**: Report submission form in dashboard

#### 3. Trust Scoring
- **Get Score**: `GET /api/v1/trust-scores/{report_id}`
- **Calculate**: `POST /api/v1/trust-scores/calculate`
- **Integration**: Real-time trust score display

#### 4. Social Media Processing
- **Ingest**: `POST /api/v1/social-media/ingest`
- **Integration**: Social media feed analysis

### 🔄 Automatic Fallbacks

When the backend is unavailable, the dashboard automatically falls back to:
- Mock data for development/demo purposes
- Graceful error handling
- Offline-capable interface

## 🎛️ Configuration

### Backend Configuration (`ai_trust_engine/config/settings.py`)
```python
# API Settings
HOST = "127.0.0.1"
PORT = 8005
DEBUG = True

# CORS Settings (allows dashboard connection)
ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```

### Frontend Configuration (`seasense-dashboard/.env.local`)
```bash
# Backend API URL
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8005

# Dashboard Settings
NEXT_PUBLIC_APP_NAME=SeaSense AI Trust Engine Dashboard
NEXT_PUBLIC_VERSION=1.0.0

# Real-time Updates
NEXT_PUBLIC_UPDATE_INTERVAL=30000
```

## 🔧 Integration Features

### 1. Real-time Dashboard
- **Live Updates**: Every 30 seconds
- **Connection Status**: Visual indicator
- **Health Monitoring**: Automatic backend status checks

### 2. Trust Score Integration
- **Automatic Calculation**: On report submission
- **Visual Indicators**: Color-coded trust scores
- **Detailed Analysis**: Comprehensive trust factors

### 3. Interactive Maps
- **Hazard Markers**: Real-time hazard locations
- **Trust-based Colors**: Visual trust score representation
- **Click Details**: Detailed report information

### 4. Social Media Monitoring
- **Live Feed**: Recent social media posts
- **Hazard Detection**: AI-powered content analysis
- **Trust Scoring**: Social media trust assessment

### 5. Analytics & Reporting
- **Trust Score Distribution**: Visual analytics
- **Hazard Type Analysis**: Category breakdowns
- **Temporal Trends**: Time-based analysis

## 📊 Data Flow

### Report Submission Flow
```
User Input → Dashboard Form → API Call → AI Processing → Trust Score → Database → Dashboard Update
```

### Real-time Monitoring Flow
```
Polling Timer → API Requests → Data Processing → State Update → UI Refresh
```

### Trust Score Calculation Flow
```
Report Data → Content Analysis → Source Verification → Cross-reference → Trust Score → Explanation
```

## 🛠️ Development Integration

### Adding New Features

#### Backend (AI Trust Engine)
1. **New Endpoint**: Add to `app/api/endpoints/`
2. **Data Models**: Define in `app/models/schemas.py`
3. **AI Logic**: Implement in `app/services/`
4. **Testing**: Add to Postman collection

#### Frontend (Dashboard)
1. **API Client**: Add to `lib/api.ts`
2. **Components**: Create in `components/`
3. **Hooks**: Add to `hooks/`
4. **Integration**: Update `lib/integration.ts`

### Example: Adding New Hazard Type

#### Backend
```python
# In app/models/schemas.py
class HazardType(str, Enum):
    HIGH_WAVES = "high_waves"
    POLLUTION = "pollution"
    DANGEROUS_CURRENTS = "dangerous_currents"
    MARINE_LIFE = "marine_life"
    NEW_HAZARD = "new_hazard"  # Add new type
```

#### Frontend
```typescript
// In lib/integration.ts
formatHazardType: (type: string): string => {
  const types = {
    'high_waves': 'High Waves',
    'pollution': 'Pollution',
    'dangerous_currents': 'Dangerous Currents',
    'marine_life': 'Marine Life',
    'new_hazard': 'New Hazard Type'  // Add new type
  }
  return types[type] || type
}
```

## 🔒 Security Integration

### CORS Configuration
- Frontend origin whitelisted in backend
- Secure headers in API responses
- Input validation on all endpoints

### Data Validation
- Pydantic models for backend validation
- TypeScript types for frontend validation
- Sanitization of user inputs

## 📈 Performance Optimization

### Caching Strategy
- API response caching
- Static asset optimization
- Database query optimization

### Real-time Updates
- Efficient polling intervals
- WebSocket ready (future enhancement)
- Background processing for large reports

## 🐛 Troubleshooting

### Common Issues

#### "API not available" in Dashboard
```bash
# Check backend status
curl http://127.0.0.1:8005/health

# Restart backend
cd ai_trust_engine
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload
```

#### Frontend Build Errors
```bash
# Clear cache and reinstall
cd seasense-dashboard
rm -rf node_modules package-lock.json
npm install
npm run dev
```

#### CORS Errors
- Ensure frontend URL is in `ALLOWED_ORIGINS`
- Check that ports match configuration
- Verify backend is running before starting frontend

## 🚀 Deployment Integration

### Production Setup
1. **Backend**: Deploy on cloud service (AWS, GCP, Azure)
2. **Frontend**: Deploy on Vercel/Netlify
3. **Environment**: Update API URLs for production
4. **Database**: Add persistent storage
5. **Monitoring**: Add logging and analytics

### Environment Variables
```bash
# Production Backend
HOST=0.0.0.0
PORT=8005
DEBUG=False
DATABASE_URL=postgresql://...

# Production Frontend
NEXT_PUBLIC_API_BASE_URL=https://api.seasense.ai
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

## 📋 Testing Integration

### Manual Testing
1. Start integrated system: `python start_integrated_system.py`
2. Open dashboard: http://localhost:3000
3. Submit test report through dashboard
4. Verify in API docs: http://127.0.0.1:8005/docs
5. Check trust score calculation

### Automated Testing
```bash
# Backend tests
cd ai_trust_engine
python -m pytest

# Frontend tests (when added)
cd seasense-dashboard
npm test
```

## 🎯 Future Enhancements

### Planned Integrations
- [ ] WebSocket for real-time updates
- [ ] Database persistence
- [ ] User authentication
- [ ] Email notifications
- [ ] Mobile app integration
- [ ] Machine learning model updates
- [ ] Advanced analytics

### Scalability Considerations
- Load balancing for backend
- CDN for frontend assets
- Database sharding
- Microservices architecture
- Caching layers

---

## 📞 Support

For integration issues:
1. Check logs in `ai_trust_engine/ai_trust_engine.log`
2. Verify API endpoints at http://127.0.0.1:8005/docs
3. Test with Postman collection
4. Check browser console for frontend errors

**🌊 Successfully Integrated SeaSense AI Trust Engine! 🌊**
