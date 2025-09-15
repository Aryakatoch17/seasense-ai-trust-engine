# 🌊 SeaSense AI Trust Engine Dashboard Setup

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Make the start script executable
chmod +x start_dashboard.py

# Start both backend and frontend
python start_dashboard.py
```

### Option 2: Manual Setup

#### 1. Start Backend API
```bash
cd ai_trust_engine
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload
```

#### 2. Start Frontend Dashboard
```bash
cd seasense-dashboard
npm install
npm run dev
```

## Access Points

- **📊 Dashboard**: http://localhost:3000
- **🔧 API**: http://127.0.0.1:8005
- **📚 API Documentation**: http://127.0.0.1:8005/docs

## Features

### ✅ Working Features
- **Real-time Dashboard**: Live updates every 30 seconds
- **Interactive Map**: Shows hazard locations with markers
- **Reports Table**: Filterable, sortable reports management
- **Analytics Charts**: Trust score distribution, hazard types
- **Social Media Feed**: Live social media monitoring
- **Trust Scoring**: AI-powered credibility assessment

### 🔧 Backend Integration
- **API Endpoints**: Connected to SeaSense AI Trust Engine
- **Mock Data**: Fallback data when API is unavailable
- **Error Handling**: Graceful degradation with mock data
- **Real-time Updates**: WebSocket support (when available)

### 🎨 Frontend Features
- **Responsive Design**: Works on desktop and mobile
- **Ocean Theme**: Beautiful ocean-inspired UI
- **Interactive Components**: Clickable maps, sortable tables
- **Real-time Indicators**: Live status indicators
- **Filtering & Search**: Advanced filtering capabilities

## Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://127.0.0.1:8005/health

# Check backend logs
cd ai_trust_engine
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload
```

### Frontend Issues
```bash
# Install dependencies
cd seasense-dashboard
npm install

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Start development server
npm run dev
```

### Port Conflicts
- Backend runs on port 8005
- Frontend runs on port 3000
- If ports are busy, change them in the respective configs

## Development

### Backend Development
- Edit files in `ai_trust_engine/`
- API auto-reloads on changes
- Check logs in terminal

### Frontend Development
- Edit files in `seasense-dashboard/`
- Hot reload enabled
- Check browser console for errors

## Production Deployment

### Backend
```bash
cd ai_trust_engine
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8005
```

### Frontend
```bash
cd seasense-dashboard
npm run build
npm start
```

## API Integration

The dashboard connects to these backend endpoints:
- `GET /health` - System health check
- `GET /api/v1/reports/nearby` - Get nearby reports
- `GET /api/v1/trust-scores/analytics/distribution` - Trust score analytics
- `GET /api/v1/social-media/trending` - Trending topics
- `POST /api/v1/reports/citizen` - Submit new reports

## Mock Data

When the backend is unavailable, the dashboard uses mock data to ensure it remains functional for demonstration purposes.

## Support

For issues or questions:
1. Check the console logs
2. Verify both services are running
3. Check network connectivity
4. Review the API documentation at `/docs`
