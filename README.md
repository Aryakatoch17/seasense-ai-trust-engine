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

- **FastAPI Backend**: High-performance REST API
- **AI-Powered Analysis**: Text processing and hazard classification
- **Trust Scoring**: Advanced algorithms for credibility assessment
- **Multi-Source Ingestion**: Citizen reports and social media data
- **Real-time Processing**: Immediate threat analysis
- **Comprehensive API**: Full REST endpoints with documentation

## 🏗️ Architecture

```
SeaSense AI Trust Engine/
├── ai_trust_engine/           # Main application directory
│   ├── app/                   # FastAPI application
│   │   ├── api/              # API endpoints
│   │   │   └── endpoints/    # Route handlers
│   │   ├── models/           # Pydantic schemas
│   │   └── services/         # AI pipeline services
│   ├── config/               # Configuration settings
│   ├── tests/                # Test suite
│   ├── main.py              # Application entry point
│   └── requirements.txt     # Python dependencies
└── SeaSense_Postman_Collection_Port_8005.json  # API testing collection
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

### 1. Clone the Repository
```bash
git clone <repository-url>
cd sih_trust_engine
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
cd ai_trust_engine
pip install -r requirements.txt
```

### 4. Start the Server
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload
```

### 5. Access the API
- **API Server**: http://127.0.0.1:8005
- **Interactive Docs**: http://127.0.0.1:8005/docs
- **Health Check**: http://127.0.0.1:8005/health

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
