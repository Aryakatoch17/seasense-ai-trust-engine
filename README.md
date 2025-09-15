# SeaSense AI Trust Engine

**Smart India Hackathon 2025 Project**

An AI-powered trust scoring system for ocean hazard reports that processes citizen submissions and social media data to generate credibility scores and detect potential threats.

## 🌊 Project Overview

SeaSense AI Trust Engine is designed to enhance ocean safety by:
- Processing citizen-reported ocean hazards
- Analyzing social media for hazard-related content
- Generating trust scores using AI algorithms
- Detecting duplicate reports and misinformation
- Providing real-time threat assessment

## 🚀 Features

### Backend (AI Trust Engine)
- **FastAPI Backend**: High-performance REST API
- **AI-Powered Analysis**: Text processing and hazard classification
- **Trust Scoring**: Advanced algorithms for credibility assessment
- **Multi-Source Ingestion**: Citizen reports and social media data
- **Real-time Processing**: Immediate threat analysis
- **Comprehensive API**: Full REST endpoints with documentation

### Frontend (Interactive Dashboard)
- **Real-time Dashboard**: Live updates and monitoring
- **Interactive Maps**: Hazard visualization with trust-based markers
- **Analytics Charts**: Trust score distribution and trends
- **Report Management**: Filterable, sortable reports interface
- **Social Media Feed**: Live social media hazard monitoring
- **Trust Score Visualization**: Color-coded credibility indicators

### Integration Features
- **Seamless API Integration**: Frontend connects to backend automatically
- **Graceful Fallbacks**: Mock data when backend unavailable
- **Real-time Updates**: Live data synchronization
- **Health Monitoring**: System status tracking
- **CORS Enabled**: Secure cross-origin requests

## 🏗️ Architecture

### Integrated System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    SeaSense Platform                        │
├─────────────────────────────────────────────────────────────┤
│  📊 Frontend Dashboard (Next.js)                           │
│  ├── Interactive Maps & Analytics                          │
│  ├── Real-time Data Visualization                          │
│  ├── Report Management Interface                           │
│  └── Social Media Monitoring                               │
│                        │                                   │
│                   REST API                                 │
│                        │                                   │
│  🔧 Backend API (FastAPI)                                  │
│  ├── /api/v1/reports/* - Citizen Reports                  │
│  ├── /api/v1/trust-scores/* - Trust Scoring               │
│  ├── /api/v1/social-media/* - Social Media Processing     │
│  └── /health - System Health                               │
│                        │                                   │
│  🧠 AI Trust Engine                                        │
│  ├── Hazard Classification                                 │
│  ├── Trust Score Calculation                               │
│  ├── Duplicate Detection                                   │
│  └── Content Analysis                                      │
└─────────────────────────────────────────────────────────────┘
```

### File Structure
```
SeaSense AI Trust Engine/
├── ai_trust_engine/           # Backend API & AI Engine
│   ├── app/                   # FastAPI application
│   │   ├── api/              # API endpoints
│   │   │   └── endpoints/    # Route handlers
│   │   ├── models/           # Pydantic schemas
│   │   └── services/         # AI pipeline services
│   ├── config/               # Configuration settings
│   ├── main.py              # Application entry point
│   └── requirements.txt     # Python dependencies
├── seasense-dashboard/        # Frontend Dashboard
│   ├── app/                  # Next.js app directory
│   ├── components/           # React components
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # API client & utilities
│   └── package.json         # Node.js dependencies
├── start_integrated_system.py # Unified startup script
├── INTEGRATION_GUIDE.md       # Detailed integration docs
└── SeaSense_Postman_Collection.json  # API testing
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **AI/ML**: Simplified NLP pipeline for hazard detection
- **Validation**: Pydantic models
- **Documentation**: Auto-generated with FastAPI
- **Testing**: Postman collection included

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

## 🚦 Quick Start

### Option 1: Integrated System (Dashboard + Backend)
```bash
# Start both AI Trust Engine and Dashboard
python start_integrated_system.py
```
**Access Points:**
- 📊 **Dashboard**: http://localhost:3000
- 🔧 **API**: http://127.0.0.1:8005
- 📚 **API Documentation**: http://127.0.0.1:8005/docs

### Option 2: Backend Only
```bash
# Clone the Repository
git clone <repository-url>
cd sih_trust_engine

# Set Up Virtual Environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Dependencies
cd ai_trust_engine
pip install -r requirements.txt

# Start the Server
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload
```

### Option 3: Dashboard Only
```bash
cd seasense-dashboard
npm install
npm run dev
```

## 📡 API Endpoints

### Core Endpoints

- `GET /health` - Health check
- `GET /` - API information
- `GET /docs` - Interactive API documentation

### Citizen Reports

- `POST /api/v1/reports/citizen` - Submit citizen hazard report
- `POST /api/v1/reports/submit` - Alternative submission endpoint

### Social Media Processing

- `POST /api/v1/social-media/ingest` - Process social media posts

### Trust Scoring

- `GET /api/v1/trust-scores/{report_id}` - Get trust score for report

## 🧪 Testing with Postman

1. Import the provided Postman collection: `SeaSense_Postman_Collection_Port_8005.json`
2. Ensure the server is running on port 8005
3. Test endpoints in the recommended order:
   - Health Check
   - Submit Citizen Report
   - Social Media Ingestion
   - Trust Score Retrieval

### Example Citizen Report
```json
{
    "description": "High waves and strong currents observed near the beach. Visibility is poor.",
    "hazard_type": "high_waves",
    "location": {
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    "location_name": "Mumbai Beach",
    "reporter_id": "user123",
    "images": []
}
```

### Example Social Media Post
```json
{
    "text": "Dangerous waves at Marina Beach today! #tsunami #warning #safety",
    "platform": "twitter",
    "author_id": "user456",
    "author_verified": false,
    "location": {
        "latitude": 13.0827,
        "longitude": 80.2707
    },
    "hashtags": ["tsunami", "warning", "safety"],
    "posted_at": "2025-09-14T18:30:00Z",
    "images": []
}
```

## 🔧 Configuration

The application can be configured through environment variables or the `config/settings.py` file:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8005)
- `DEBUG`: Debug mode (default: True)

## 🧠 AI Pipeline

The simplified AI pipeline includes:
- **Text Analysis**: Language detection and sentiment analysis
- **Hazard Classification**: Keyword-based hazard type detection
- **Trust Scoring**: Credibility assessment algorithms
- **Duplicate Detection**: Content similarity analysis

## 📈 Project Status

✅ **Core API Development**: Complete  
✅ **AI Pipeline Integration**: Functional simplified version  
✅ **Data Validation**: Pydantic schemas implemented  
✅ **Testing Suite**: Postman collection ready  
✅ **Documentation**: Auto-generated API docs  

## 🤝 Contributing

This is a Smart India Hackathon 2025 project. For development:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is developed for Smart India Hackathon 2025.

## 👥 Team

**Project**: SeaSense AI Trust Engine  
**Event**: Smart India Hackathon 2025  
**Focus**: Ocean Safety and Hazard Management  

## 📞 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the Postman collection for examples
3. Check the application logs for debugging

---

**🌊 Making Oceans Safer with AI 🌊**
