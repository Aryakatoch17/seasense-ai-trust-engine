"""
Pydantic models for SeaSense AI Trust Engine
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator
import uuid


class HazardType(str, Enum):
    """Types of ocean hazards."""
    TSUNAMI = "tsunami"
    STORM = "storm"
    HIGH_WAVES = "high_waves"
    POLLUTION = "pollution"
    DEBRIS = "debris"
    UNUSUAL_CURRENT = "unusual_current"
    TEMPERATURE_ANOMALY = "temperature_anomaly"
    OTHER = "other"


class ReportSource(str, Enum):
    """Source of the report."""
    CITIZEN = "citizen"
    SOCIAL_MEDIA = "social_media"
    OFFICIAL = "official"
    SENSOR = "sensor"
    SATELLITE = "satellite"


class Priority(str, Enum):
    """Priority levels for reports."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GPSCoordinates(BaseModel):
    """GPS coordinates with validation."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")
    accuracy: Optional[float] = Field(None, ge=0, description="GPS accuracy in meters")


class ImageData(BaseModel):
    """Image data model."""
    base64_data: str = Field(..., description="Base64 encoded image data")
    filename: Optional[str] = Field(None, description="Original filename")
    content_type: str = Field(default="image/jpeg", description="MIME type")
    
    @validator('base64_data')
    def validate_base64(cls, v):
        """Validate base64 data format."""
        import base64
        try:
            base64.b64decode(v)
            return v
        except Exception:
            raise ValueError("Invalid base64 data")


class CitizenReport(BaseModel):
    """Model for citizen-submitted reports."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique report ID")
    
    # Content
    description: str = Field(..., min_length=10, max_length=5000, description="Report description")
    hazard_type: HazardType = Field(..., description="Type of hazard reported")
    
    # Location and Time
    location: GPSCoordinates = Field(..., description="GPS coordinates")
    location_name: Optional[str] = Field(None, description="Human-readable location name")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Report timestamp")
    
    # Media
    images: Optional[List[ImageData]] = Field(default=[], description="Associated images")
    
    # Reporter Information
    reporter_id: Optional[str] = Field(None, description="Anonymous reporter identifier")
    reporter_reputation: Optional[float] = Field(None, ge=0, le=1, description="Reporter's reputation score")
    
    # Metadata
    source: ReportSource = Field(default=ReportSource.CITIZEN, description="Report source")
    device_info: Optional[Dict[str, Any]] = Field(default={}, description="Device information")
    language: str = Field(default="en", description="Report language")


class SocialMediaPost(BaseModel):
    """Model for social media posts."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique post ID")
    
    # Content
    text: str = Field(..., description="Post text content")
    platform: str = Field(..., description="Social media platform")
    original_url: Optional[str] = Field(None, description="Original post URL")
    
    # Author
    author_id: str = Field(..., description="Author identifier")
    author_followers: Optional[int] = Field(None, ge=0, description="Author follower count")
    author_verified: bool = Field(default=False, description="Author verification status")
    
    # Engagement
    likes: Optional[int] = Field(None, ge=0, description="Number of likes")
    shares: Optional[int] = Field(None, ge=0, description="Number of shares")
    comments: Optional[int] = Field(None, ge=0, description="Number of comments")
    
    # Media and Location
    images: Optional[List[ImageData]] = Field(default=[], description="Post images")
    location: Optional[GPSCoordinates] = Field(None, description="Post location")
    hashtags: List[str] = Field(default=[], description="Post hashtags")
    
    # Timing
    posted_at: datetime = Field(..., description="Post creation time")
    scraped_at: datetime = Field(default_factory=datetime.utcnow, description="Data collection time")


class TrustScore(BaseModel):
    """Trust score breakdown."""
    overall_score: float = Field(..., ge=0, le=1, description="Overall trust score (0-1)")
    
    # Component scores
    content_credibility: float = Field(..., ge=0, le=1, description="Content analysis score")
    source_reliability: float = Field(..., ge=0, le=1, description="Source reliability score")
    temporal_consistency: float = Field(..., ge=0, le=1, description="Temporal pattern score")
    spatial_consistency: float = Field(..., ge=0, le=1, description="Spatial pattern score")
    cross_verification: float = Field(..., ge=0, le=1, description="Cross-verification score")
    
    # Confidence and metadata
    confidence: float = Field(..., ge=0, le=1, description="Confidence in the score")
    processing_time: float = Field(..., description="Processing time in seconds")
    model_version: str = Field(..., description="AI model version used")
    
    # Explanations
    factors: Dict[str, float] = Field(default={}, description="Contributing factors")
    warnings: List[str] = Field(default=[], description="Potential issues detected")


class ProcessedReport(BaseModel):
    """Fully processed report with trust score."""
    # Original report
    original_report: CitizenReport = Field(..., description="Original citizen report")
    
    # Processing results
    trust_score: TrustScore = Field(..., description="Calculated trust score")
    priority: Priority = Field(..., description="Assigned priority level")
    
    # AI Analysis
    detected_hazards: List[HazardType] = Field(default=[], description="AI-detected hazards")
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1, description="Sentiment analysis")
    language_confidence: Optional[float] = Field(None, ge=0, le=1, description="Language detection confidence")
    
    # Duplicate Detection
    similar_reports: List[str] = Field(default=[], description="IDs of similar reports")
    is_duplicate: bool = Field(default=False, description="Flagged as duplicate")
    cluster_id: Optional[str] = Field(None, description="Cluster identifier")
    
    # Verification
    verified_by_officials: bool = Field(default=False, description="Official verification status")
    verification_notes: Optional[str] = Field(None, description="Verification comments")
    
    # Processing metadata
    processed_at: datetime = Field(default_factory=datetime.utcnow, description="Processing completion time")
    processing_version: str = Field(..., description="Processing pipeline version")


class APIResponse(BaseModel):
    """Standard API response format."""
    success: bool = Field(..., description="Request success status")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(None, description="Response data")
    errors: Optional[List[str]] = Field(default=[], description="Error messages")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")


class BatchProcessRequest(BaseModel):
    """Batch processing request."""
    reports: List[CitizenReport] = Field(..., description="Reports to process")
    priority_processing: bool = Field(default=False, description="High-priority processing")
    include_duplicates: bool = Field(default=True, description="Include duplicate detection")


class TrustScoreRequest(BaseModel):
    """Request for trust score calculation."""
    report: CitizenReport = Field(..., description="Report to analyze")
    social_media_posts: Optional[List[SocialMediaPost]] = Field(default=[], description="Related social media posts")
    historical_context: bool = Field(default=True, description="Include historical analysis")


class DuplicateDetectionResult(BaseModel):
    """Duplicate detection results."""
    is_duplicate: bool = Field(..., description="Is this report a duplicate")
    similarity_score: float = Field(..., ge=0, le=1, description="Similarity score")
    similar_reports: List[str] = Field(default=[], description="Similar report IDs")
    cluster_id: Optional[str] = Field(None, description="Cluster identifier")
    confidence: float = Field(..., ge=0, le=1, description="Detection confidence")
