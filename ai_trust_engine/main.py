"""
SeaSense AI Trust Engine - Main FastAPI Application
Smart India Hackathon 2025 Project

This is the core AI Trust Engine that processes citizen reports and social media data
to generate trust scores for ocean hazard reports.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from app.api.endpoints import reports, social_media, trust_scores
from app.services.ai_pipeline_simple import AIPipeline
from config.settings import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ai_trust_engine.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    logger.info("Starting SeaSense AI Trust Engine...")
    
    # Initialize AI Pipeline
    try:
        app.state.ai_pipeline = AIPipeline()
        await app.state.ai_pipeline.initialize()
        logger.info("AI Pipeline initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI Pipeline: {e}")
        raise
    
    yield
    
    # Cleanup
    logger.info("Shutting down SeaSense AI Trust Engine...")
    if hasattr(app.state, 'ai_pipeline'):
        await app.state.ai_pipeline.cleanup()


# Create FastAPI application
app = FastAPI(
    title="SeaSense AI Trust Engine",
    description="AI-powered trust scoring system for ocean hazard reports",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Get settings
settings = get_settings()

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include routers
app.include_router(
    reports.router,
    prefix="/api/v1/reports",
    tags=["Citizen Reports"]
)

app.include_router(
    social_media.router,
    prefix="/api/v1/social-media",
    tags=["Social Media Processing"]
)

app.include_router(
    trust_scores.router,
    prefix="/api/v1/trust-scores",
    tags=["Trust Scoring"]
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "SeaSense AI Trust Engine",
        "version": "1.0.0",
        "description": "AI-powered trust scoring for ocean hazard reports",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "reports": "/api/v1/reports",
            "social": "/api/v1/social",
            "trust": "/api/v1/trust"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check if AI pipeline is available
        if hasattr(app.state, 'ai_pipeline'):
            pipeline_status = "healthy"
        else:
            pipeline_status = "unavailable"
        
        return {
            "status": "healthy",
            "ai_pipeline": pipeline_status,
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")


def get_ai_pipeline():
    """Dependency to get AI Pipeline instance."""
    if not hasattr(app.state, 'ai_pipeline'):
        raise HTTPException(status_code=503, detail="AI Pipeline not available")
    return app.state.ai_pipeline


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
