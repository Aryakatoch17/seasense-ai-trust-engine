"""
Social Media Processing API Endpoints
Handles ingestion and analysis of social media posts for cross-verification
"""

import logging
import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.models.schemas import (
    SocialMediaPost, APIResponse, TrustScore, CitizenReport
)
from app.services.ai_pipeline_simple import AIPipeline

logger = logging.getLogger(__name__)

router = APIRouter()


def get_ai_pipeline():
    """Dependency to get AI Pipeline instance."""
    from main import app
    if not hasattr(app.state, 'ai_pipeline'):
        raise HTTPException(status_code=503, detail="AI Pipeline not available")
    return app.state.ai_pipeline


@router.post("/ingest", response_model=APIResponse)
@router.post("/social-media", response_model=APIResponse)  # Add alias for Postman
async def ingest_social_media_post(
    post: SocialMediaPost,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Ingest and process a social media post.
    
    This endpoint accepts social media posts and processes them to extract
    hazard-related information that can be used for cross-verification.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Received social media post: {post.id} from {post.platform}")
        
        # Validate post data
        if not post.text.strip():
            raise HTTPException(status_code=400, detail="Post text cannot be empty")
        
        # Process the post through AI pipeline
        processing_results = await process_social_media_post(post, ai_pipeline)
        
        return APIResponse(
            success=True,
            message="Social media post processed successfully",
            data={
                "post_id": post.id,
                "platform": post.platform,
                "analysis": processing_results
            },
            processing_time=time.time() - start_time
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing social media post {post.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/batch", response_model=APIResponse)
async def ingest_batch_posts(
    posts: List[SocialMediaPost],
    background_tasks: BackgroundTasks,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Ingest multiple social media posts in batch.
    
    This endpoint accepts multiple social media posts for efficient
    batch processing and analysis.
    """
    start_time = time.time()
    
    try:
        if len(posts) > 200:
            raise HTTPException(status_code=400, detail="Batch size cannot exceed 200 posts")
        
        logger.info(f"Received batch of {len(posts)} social media posts")
        
        # Add to background processing
        background_tasks.add_task(process_social_batch_background, posts, ai_pipeline)
        
        batch_id = f"social_batch_{int(time.time())}"
        
        return APIResponse(
            success=True,
            message=f"Batch of {len(posts)} posts submitted for processing",
            data={
                "batch_id": batch_id,
                "post_count": len(posts),
                "status": "processing"
            },
            processing_time=time.time() - start_time
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing batch social media posts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analyze/{post_id}")
async def analyze_social_post(
    post_id: str,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Get detailed analysis of a social media post.
    
    This endpoint returns comprehensive analysis results for a specific
    social media post, including hazard detection and credibility assessment.
    """
    try:
        # In a real implementation, this would retrieve from database
        analysis_result = {
            "post_id": post_id,
            "hazard_detected": False,
            "hazard_types": [],
            "credibility_score": 0.6,
            "sentiment": "neutral",
            "language": "en",
            "engagement_score": 0.4
        }
        
        return APIResponse(
            success=True,
            message="Social media post analysis retrieved",
            data=analysis_result
        )
    
    except Exception as e:
        logger.error(f"Error analyzing social post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/correlate")
async def correlate_with_reports(
    latitude: float,
    longitude: float,
    radius_km: float = 20.0,
    time_window_hours: int = 24,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Correlate social media posts with citizen reports.
    
    This endpoint finds social media posts that correlate with citizen reports
    in a specific geographic area and time window for cross-verification.
    """
    try:
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            raise HTTPException(status_code=400, detail="Invalid latitude")
        
        if not (-180 <= longitude <= 180):
            raise HTTPException(status_code=400, detail="Invalid longitude")
        
        if radius_km <= 0 or radius_km > 500:
            raise HTTPException(status_code=400, detail="Radius must be between 0 and 500 km")
        
        # In a real implementation, this would perform spatial-temporal correlation
        correlation_result = {
            "location": {"latitude": latitude, "longitude": longitude},
            "radius_km": radius_km,
            "time_window_hours": time_window_hours,
            "correlations": [],
            "total_posts": 0,
            "matching_posts": 0
        }
        
        return APIResponse(
            success=True,
            message="Social media correlation analysis completed",
            data=correlation_result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error correlating social media posts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/trending")
async def get_trending_topics(
    platform: Optional[str] = None,
    time_window_hours: int = 24,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Get trending ocean hazard topics from social media.
    
    This endpoint analyzes social media posts to identify trending
    topics related to ocean hazards and emergencies.
    """
    try:
        # In a real implementation, this would analyze trending topics
        trending_result = {
            "time_window_hours": time_window_hours,
            "platform": platform,
            "trending_topics": [
                {
                    "topic": "high waves",
                    "frequency": 156,
                    "sentiment": "negative",
                    "locations": ["Mumbai", "Goa", "Chennai"]
                },
                {
                    "topic": "storm warning",
                    "frequency": 89,
                    "sentiment": "concerned",
                    "locations": ["Kolkata", "Visakhapatnam"]
                }
            ],
            "total_posts_analyzed": 2500
        }
        
        return APIResponse(
            success=True,
            message="Trending topics analysis completed",
            data=trending_result
        )
    
    except Exception as e:
        logger.error(f"Error getting trending topics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def process_social_media_post(post: SocialMediaPost, ai_pipeline: AIPipeline) -> dict:
    """Process a single social media post through the AI pipeline."""
    try:
        # Process text content using simplified methods
        text_features = await ai_pipeline._process_text_simple(post.text, "en")
        
        # Process images if available using simplified methods
        image_features = {}
        if post.images:
            image_features = await ai_pipeline._process_images_simple(post.images)
        
        # Classify potential hazards using simplified methods
        hazard_classification = await ai_pipeline._classify_hazards_simple(post.text)
        
        # Calculate engagement score
        engagement_score = calculate_engagement_score(post)
        
        # Calculate credibility score based on author and content
        credibility_score = calculate_social_credibility(post, text_features)
        
        return {
            "text_analysis": {
                "language": text_features.get('detected_language', 'en'),
                "language_confidence": text_features.get('language_confidence', 0.9),
                "sentiment": text_features.get('sentiment_scores', {}),
                "word_count": text_features.get('word_count', 0)
            },
            "hazard_analysis": hazard_classification,
            "image_analysis": image_features,
            "engagement_score": engagement_score,
            "credibility_score": credibility_score,
            "has_location": post.location is not None
        }
    
    except Exception as e:
        logger.error(f"Error processing social media post {post.id}: {e}")
        raise


def calculate_engagement_score(post: SocialMediaPost) -> float:
    """Calculate engagement score based on likes, shares, comments."""
    try:
        total_engagement = (post.likes or 0) + (post.shares or 0) + (post.comments or 0)
        
        # Normalize based on follower count
        if post.author_followers and post.author_followers > 0:
            engagement_rate = total_engagement / post.author_followers
            # Cap at 1.0 and normalize to 0-1 scale
            return min(1.0, engagement_rate * 100)
        else:
            # Fallback to absolute engagement
            return min(1.0, total_engagement / 1000.0)
    
    except Exception:
        return 0.0


def calculate_social_credibility(post: SocialMediaPost, text_features: dict) -> float:
    """Calculate credibility score for social media post."""
    try:
        score = 0.0
        
        # Author verification
        if post.author_verified:
            score += 0.3
        
        # Follower count (normalized)
        if post.author_followers:
            follower_score = min(1.0, (post.author_followers / 10000))
            score += 0.2 * follower_score
        
        # Text quality
        lang_confidence = text_features.get('language_confidence', 0.5)
        score += 0.2 * lang_confidence
        
        # Content length (not too short, not too long)
        word_count = text_features.get('word_count', 0)
        if 10 <= word_count <= 100:
            length_score = 1.0
        elif word_count < 10:
            length_score = word_count / 10.0
        else:
            length_score = max(0.5, 1.0 - (word_count - 100) / 200.0)
        score += 0.2 * length_score
        
        # Has location data
        if hasattr(post, 'location') and post.location:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    except Exception:
        return 0.5


async def process_social_batch_background(posts: List[SocialMediaPost], ai_pipeline: AIPipeline):
    """Background task for batch processing social media posts."""
    try:
        processed_count = 0
        
        for post in posts:
            try:
                await process_social_media_post(post, ai_pipeline)
                processed_count += 1
                
                if processed_count % 20 == 0:
                    logger.info(f"Social batch processing: {processed_count}/{len(posts)} completed")
            
            except Exception as e:
                logger.error(f"Failed to process social post {post.id} in batch: {e}")
                continue
        
        logger.info(f"Social batch processing completed: {processed_count}/{len(posts)} posts processed")
        
    except Exception as e:
        logger.error(f"Social batch processing failed: {e}")
