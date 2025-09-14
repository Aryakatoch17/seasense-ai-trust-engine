"""
Configuration settings for SeaSense AI Trust Engine
"""

import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8002
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./seasense.db"
    
    # AI Models Configuration
    HUGGINGFACE_TOKEN: str = ""
    MBERT_MODEL: str = "bert-base-multilingual-cased"
    CLIP_MODEL: str = "openai/clip-vit-base-patch32"
    YOLO_MODEL: str = "yolov8n.pt"
    
    # Trust Scoring Parameters
    MIN_TRUST_SCORE: float = 0.0
    MAX_TRUST_SCORE: float = 1.0
    DEFAULT_TRUST_SCORE: float = 0.5
    
    # Duplicate Detection
    SIMILARITY_THRESHOLD: float = 0.8
    CLUSTERING_EPS: float = 0.3
    MIN_SAMPLES: int = 2
    
    # Social Media API Keys (Optional)
    TWITTER_API_KEY: str = ""
    TWITTER_API_SECRET: str = ""
    TWITTER_ACCESS_TOKEN: str = ""
    TWITTER_ACCESS_TOKEN_SECRET: str = ""
    FACEBOOK_ACCESS_TOKEN: str = ""
    
    # Processing Limits
    MAX_IMAGE_SIZE_MB: int = 10
    MAX_TEXT_LENGTH: int = 5000
    MAX_BATCH_SIZE: int = 100
    
    # Cache Configuration
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "ai_trust_engine.log"
    
    # Model Paths
    MODEL_CACHE_DIR: str = "./models"
    EMBEDDINGS_CACHE_DIR: str = "./embeddings"
    
    # Performance Settings
    MAX_WORKERS: int = 4
    BATCH_PROCESSING_INTERVAL: int = 60
    CLEANUP_INTERVAL: int = 3600
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
