"""
Trust Scoring API Endpoints
Handles trust score calculation and retrieval
"""

import logging
import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.models.schemas import (
    CitizenReport, SocialMediaPost, TrustScore, 
    TrustScoreRequest, APIResponse
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


@router.post("/calculate", response_model=APIResponse)
async def calculate_trust_score(
    request: TrustScoreRequest,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Calculate trust score for a citizen report.
    
    This endpoint performs comprehensive trust scoring by analyzing
    the report content, cross-referencing with social media posts,
    and applying various credibility algorithms.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Calculating trust score for report: {request.report.id}")
        
        # Process the report through AI pipeline
        processing_results = await ai_pipeline.process_citizen_report(request.report)
        
        # Calculate trust score with social media context
        trust_score = await ai_pipeline.calculate_trust_score(
            request.report, 
            processing_results,
            request.social_media_posts
        )
        
        # Generate explanation
        explanation = generate_trust_explanation(trust_score, processing_results)
        
        return APIResponse(
            success=True,
            message="Trust score calculated successfully",
            data={
                "trust_score": trust_score.dict(),
                "explanation": explanation,
                "report_id": request.report.id
            },
            processing_time=time.time() - start_time
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating trust score for {request.report.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/score/{report_id}")
@router.get("/{report_id}")  # Add alias for Postman
async def get_trust_score(
    report_id: str,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Retrieve existing trust score for a report.
    
    This endpoint returns the previously calculated trust score
    and analysis results for a specific report.
    """
    try:
        # In a real implementation, this would retrieve from database
        # For now, return a mock trust score
        mock_trust_score = {
            "overall_score": 0.75,
            "content_credibility": 0.8,
            "source_reliability": 0.7,
            "temporal_consistency": 0.75,
            "spatial_consistency": 0.8,
            "cross_verification": 0.6,
            "confidence": 0.85,
            "processing_time": 2.3,
            "model_version": "v1.0.0",
            "factors": {
                "language_confidence": 0.95,
                "image_quality": 0.8,
                "clip_alignment": 0.7,
                "hazard_confidence": 0.82
            },
            "warnings": []
        }
        
        return APIResponse(
            success=True,
            message="Trust score retrieved successfully",
            data={
                "report_id": report_id,
                "trust_score": mock_trust_score
            }
        )
    
    except Exception as e:
        logger.error(f"Error retrieving trust score for {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/bulk-calculate")
async def calculate_bulk_trust_scores(
    reports: List[CitizenReport],
    social_media_posts: Optional[List[SocialMediaPost]] = None,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Calculate trust scores for multiple reports in bulk.
    
    This endpoint efficiently processes multiple reports to generate
    trust scores, useful for batch analysis and historical data processing.
    """
    start_time = time.time()
    
    try:
        if len(reports) > 50:
            raise HTTPException(status_code=400, detail="Bulk processing limited to 50 reports")
        
        logger.info(f"Calculating trust scores for {len(reports)} reports")
        
        results = []
        social_posts = social_media_posts or []
        
        for report in reports:
            try:
                # Process each report
                processing_results = await ai_pipeline.process_citizen_report(report)
                
                # Calculate trust score
                trust_score = await ai_pipeline.calculate_trust_score(
                    report, processing_results, social_posts
                )
                
                results.append({
                    "report_id": report.id,
                    "trust_score": trust_score.dict(),
                    "status": "success"
                })
                
            except Exception as e:
                logger.error(f"Error processing report {report.id}: {e}")
                results.append({
                    "report_id": report.id,
                    "trust_score": None,
                    "status": "failed",
                    "error": str(e)
                })
        
        successful_count = sum(1 for r in results if r["status"] == "success")
        
        return APIResponse(
            success=True,
            message=f"Bulk trust score calculation completed. {successful_count}/{len(reports)} successful.",
            data={
                "results": results,
                "total_reports": len(reports),
                "successful": successful_count,
                "failed": len(reports) - successful_count
            },
            processing_time=time.time() - start_time
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk trust score calculation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/distribution")
async def get_trust_score_distribution(
    time_period: str = "24h",  # 24h, 7d, 30d
    hazard_type: Optional[str] = None
):
    """
    Get trust score distribution analytics.
    
    This endpoint provides statistical analysis of trust scores
    across different time periods and hazard types.
    """
    try:
        # In a real implementation, this would query the database
        # Mock distribution data
        distribution_data = {
            "time_period": time_period,
            "hazard_type": hazard_type,
            "total_reports": 1500,
            "score_distribution": {
                "0.0-0.2": 120,
                "0.2-0.4": 180,
                "0.4-0.6": 450,
                "0.6-0.8": 520,
                "0.8-1.0": 230
            },
            "average_score": 0.62,
            "median_score": 0.65,
            "high_trust_reports": 750,  # Score > 0.6
            "low_trust_reports": 300    # Score < 0.4
        }
        
        return APIResponse(
            success=True,
            message="Trust score distribution retrieved",
            data=distribution_data
        )
    
    except Exception as e:
        logger.error(f"Error getting trust score distribution: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/trends")
async def get_trust_score_trends(
    days: int = 7,
    hazard_type: Optional[str] = None
):
    """
    Get trust score trends over time.
    
    This endpoint provides time-series analysis of trust scores
    to identify patterns and trends in report credibility.
    """
    try:
        if days < 1 or days > 365:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
        
        # Mock trend data
        trend_data = {
            "days": days,
            "hazard_type": hazard_type,
            "daily_averages": [
                {"date": "2024-12-07", "avg_score": 0.68, "count": 45},
                {"date": "2024-12-08", "avg_score": 0.72, "count": 52},
                {"date": "2024-12-09", "avg_score": 0.65, "count": 38},
                {"date": "2024-12-10", "avg_score": 0.70, "count": 41},
                {"date": "2024-12-11", "avg_score": 0.74, "count": 47},
                {"date": "2024-12-12", "avg_score": 0.69, "count": 39},
                {"date": "2024-12-13", "avg_score": 0.71, "count": 44}
            ],
            "overall_trend": "stable",  # improving, declining, stable
            "trend_score": 0.02  # Change rate
        }
        
        return APIResponse(
            success=True,
            message="Trust score trends retrieved",
            data=trend_data
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trust score trends: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/model/metrics")
async def get_model_metrics(
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Get AI model performance metrics.
    
    This endpoint provides insights into the AI models' performance,
    including accuracy, processing times, and resource usage.
    """
    try:
        # Mock model metrics
        metrics_data = {
            "model_version": "v1.0.0",
            "uptime_hours": 72.5,
            "total_reports_processed": 5420,
            "average_processing_time": 2.1,
            "model_performance": {
                "nlp_accuracy": 0.87,
                "image_classification_accuracy": 0.83,
                "duplicate_detection_precision": 0.91,
                "duplicate_detection_recall": 0.78
            },
            "resource_usage": {
                "cpu_usage_percent": 45,
                "memory_usage_gb": 3.2,
                "gpu_usage_percent": 72
            },
            "error_rates": {
                "total_errors": 23,
                "error_rate_percent": 0.42
            }
        }
        
        return APIResponse(
            success=True,
            message="Model metrics retrieved",
            data=metrics_data
        )
    
    except Exception as e:
        logger.error(f"Error getting model metrics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def generate_trust_explanation(trust_score: TrustScore, processing_results: dict) -> dict:
    """Generate human-readable explanation for trust score."""
    try:
        explanations = []
        
        # Overall score interpretation
        if trust_score.overall_score >= 0.8:
            explanations.append("High trust score indicates very credible report")
        elif trust_score.overall_score >= 0.6:
            explanations.append("Moderate trust score indicates reasonably credible report")
        elif trust_score.overall_score >= 0.4:
            explanations.append("Low trust score indicates potential credibility issues")
        else:
            explanations.append("Very low trust score indicates significant credibility concerns")
        
        # Component explanations
        if trust_score.content_credibility < 0.5:
            explanations.append("Content analysis shows potential inconsistencies")
        
        if trust_score.source_reliability < 0.5:
            explanations.append("Source reliability is below average")
        
        # Processing insights
        text_features = processing_results.get('text_features', {})
        if text_features.get('language_confidence', 1.0) < 0.8:
            explanations.append("Language detection confidence is low")
        
        image_features = processing_results.get('image_features', {})
        if image_features.get('count', 0) == 0:
            explanations.append("No visual evidence provided")
        
        duplicate_result = processing_results.get('duplicate_result')
        if duplicate_result and duplicate_result.is_duplicate:
            explanations.append("Report appears to be similar to existing reports")
        
        return {
            "summary": explanations[0] if explanations else "Standard trust assessment completed",
            "details": explanations,
            "recommendations": generate_recommendations(trust_score),
            "confidence_level": "high" if trust_score.confidence > 0.8 else "medium" if trust_score.confidence > 0.6 else "low"
        }
    
    except Exception as e:
        logger.error(f"Error generating trust explanation: {e}")
        return {
            "summary": "Trust score calculated",
            "details": [],
            "recommendations": [],
            "confidence_level": "unknown"
        }


def generate_recommendations(trust_score: TrustScore) -> List[str]:
    """Generate actionable recommendations based on trust score."""
    recommendations = []
    
    if trust_score.overall_score < 0.4:
        recommendations.append("Manual verification strongly recommended")
        recommendations.append("Request additional evidence from reporter")
    
    if trust_score.cross_verification < 0.5:
        recommendations.append("Seek additional confirmation from other sources")
    
    if trust_score.content_credibility < 0.6:
        recommendations.append("Review content for inconsistencies")
    
    if len(trust_score.warnings) > 0:
        recommendations.append("Address identified warnings before acting on report")
    
    if not recommendations:
        recommendations.append("Report appears credible - proceed with standard verification")
    
    return recommendations
