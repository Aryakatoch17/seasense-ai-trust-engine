"""
Citizen Reports API Endpoints
Handles submission and processing of citizen-generated hazard reports
"""

import logging
import time
from typing import List
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.models.schemas import (
    CitizenReport, ProcessedReport, APIResponse, 
    BatchProcessRequest, TrustScore, Priority
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


@router.post("/submit", response_model=APIResponse)
@router.post("/citizen", response_model=APIResponse)  # Add alias for Postman
async def submit_citizen_report(
    report: CitizenReport,
    background_tasks: BackgroundTasks,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Submit a new citizen report for processing.
    
    This endpoint accepts a citizen report and processes it through the AI pipeline
    to generate a trust score and detect potential duplicates.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Received citizen report: {report.id}")
        
        # Validate report data
        if not report.description.strip():
            raise HTTPException(status_code=400, detail="Report description cannot be empty")
        
        if not (-90 <= report.location.latitude <= 90):
            raise HTTPException(status_code=400, detail="Invalid latitude")
        
        if not (-180 <= report.location.longitude <= 180):
            raise HTTPException(status_code=400, detail="Invalid longitude")
        
        # Process in background for large reports, immediate for small ones
        if len(report.images or []) > 3 or len(report.description) > 1000:
            background_tasks.add_task(process_report_background, report, ai_pipeline)
            
            return APIResponse(
                success=True,
                message="Report submitted successfully. Processing in background.",
                data={"report_id": report.id, "status": "processing"},
                processing_time=time.time() - start_time
            )
        else:
            # Process immediately for small reports
            processed_report = await process_citizen_report(report, ai_pipeline)
            
            return APIResponse(
                success=True,
                message="Report processed successfully",
                data=processed_report.dict(),
                processing_time=time.time() - start_time
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing citizen report {report.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/status/{report_id}")
async def get_report_status(report_id: str):
    """
    Get the processing status of a submitted report.
    
    This endpoint allows checking the status of reports that are being
    processed in the background.
    """
    try:
        # In a real implementation, this would check a database or cache
        # For now, return a mock response
        return APIResponse(
            success=True,
            message="Report status retrieved",
            data={
                "report_id": report_id,
                "status": "completed",  # completed, processing, failed
                "progress": 100
            }
        )
    
    except Exception as e:
        logger.error(f"Error getting report status for {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/batch", response_model=APIResponse)
async def submit_batch_reports(
    batch_request: BatchProcessRequest,
    background_tasks: BackgroundTasks,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Submit multiple citizen reports for batch processing.
    
    This endpoint accepts multiple reports and processes them efficiently
    in batch mode with optional priority processing.
    """
    start_time = time.time()
    
    try:
        if len(batch_request.reports) > 100:
            raise HTTPException(status_code=400, detail="Batch size cannot exceed 100 reports")
        
        logger.info(f"Received batch of {len(batch_request.reports)} reports")
        
        # Add to background processing
        background_tasks.add_task(
            process_batch_background, 
            batch_request.reports, 
            ai_pipeline,
            batch_request.priority_processing
        )
        
        batch_id = f"batch_{int(time.time())}"
        
        return APIResponse(
            success=True,
            message=f"Batch of {len(batch_request.reports)} reports submitted for processing",
            data={
                "batch_id": batch_id,
                "report_count": len(batch_request.reports),
                "status": "processing"
            },
            processing_time=time.time() - start_time
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing batch reports: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/duplicates/{report_id}")
async def get_duplicate_reports(
    report_id: str,
    ai_pipeline: AIPipeline = Depends(get_ai_pipeline)
):
    """
    Get duplicate reports for a given report ID.
    
    This endpoint returns reports that are similar to the specified report,
    useful for deduplication and cross-verification.
    """
    try:
        # In a real implementation, this would query the embeddings database
        similar_reports = []  # Mock empty result
        
        return APIResponse(
            success=True,
            message="Duplicate reports retrieved",
            data={
                "report_id": report_id,
                "similar_reports": similar_reports,
                "count": len(similar_reports)
            }
        )
    
    except Exception as e:
        logger.error(f"Error getting duplicates for {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/nearby")
async def get_nearby_reports(
    latitude: float,
    longitude: float,
    radius_km: float = 10.0,
    max_results: int = 50
):
    """
    Get reports near a specific location.
    
    This endpoint returns reports within a specified radius of given coordinates,
    useful for spatial analysis and clustering.
    """
    try:
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            raise HTTPException(status_code=400, detail="Invalid latitude")
        
        if not (-180 <= longitude <= 180):
            raise HTTPException(status_code=400, detail="Invalid longitude")
        
        if radius_km <= 0 or radius_km > 1000:
            raise HTTPException(status_code=400, detail="Radius must be between 0 and 1000 km")
        
        # In a real implementation, this would query a spatial database
        nearby_reports = []  # Mock empty result
        
        return APIResponse(
            success=True,
            message="Nearby reports retrieved",
            data={
                "location": {"latitude": latitude, "longitude": longitude},
                "radius_km": radius_km,
                "reports": nearby_reports,
                "count": len(nearby_reports)
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting nearby reports: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def process_citizen_report(report: CitizenReport, ai_pipeline: AIPipeline) -> ProcessedReport:
    """Process a single citizen report through the AI pipeline."""
    try:
        # Process through AI pipeline
        processing_results = await ai_pipeline.process_citizen_report(report)
        
        # Calculate trust score
        trust_score = await ai_pipeline.calculate_trust_score(report, processing_results)
        
        # Determine priority based on trust score and hazard type
        priority = determine_priority(trust_score, report.hazard_type)
        
        # Extract AI analysis results
        hazard_classification = processing_results['hazard_classification']
        detected_hazards = [hazard_classification['predicted_hazard']]
        
        # Sentiment analysis
        sentiment_scores = processing_results['text_features']['sentiment_scores']
        sentiment_score = sentiment_scores.get('POSITIVE', 0) - sentiment_scores.get('NEGATIVE', 0)
        
        # Language detection
        lang_confidence = processing_results['text_features']['language_confidence']
        
        # Duplicate detection results
        duplicate_result = processing_results['duplicate_result']
        
        # Create processed report
        processed_report = ProcessedReport(
            original_report=report,
            trust_score=trust_score,
            priority=priority,
            detected_hazards=detected_hazards,
            sentiment_score=sentiment_score,
            language_confidence=lang_confidence,
            similar_reports=duplicate_result.similar_reports,
            is_duplicate=duplicate_result.is_duplicate,
            cluster_id=duplicate_result.cluster_id,
            processing_version="v1.0.0"
        )
        
        logger.info(f"Successfully processed report {report.id} with trust score {trust_score.overall_score:.2f}")
        
        return processed_report
    
    except Exception as e:
        logger.error(f"Error processing report {report.id}: {e}")
        raise


def determine_priority(trust_score: TrustScore, hazard_type) -> Priority:
    """Determine report priority based on trust score and hazard type."""
    # High-risk hazard types
    critical_hazards = ["tsunami", "storm"]
    
    if hazard_type in critical_hazards and trust_score.overall_score > 0.7:
        return Priority.CRITICAL
    elif trust_score.overall_score > 0.8:
        return Priority.HIGH
    elif trust_score.overall_score > 0.5:
        return Priority.MEDIUM
    else:
        return Priority.LOW


async def process_report_background(report: CitizenReport, ai_pipeline: AIPipeline):
    """Background task for processing reports."""
    try:
        processed_report = await process_citizen_report(report, ai_pipeline)
        
        # In a real implementation, save to database
        logger.info(f"Background processing completed for report {report.id}")
        
    except Exception as e:
        logger.error(f"Background processing failed for report {report.id}: {e}")


async def process_batch_background(reports: List[CitizenReport], ai_pipeline: AIPipeline, priority: bool = False):
    """Background task for batch processing reports."""
    try:
        processed_count = 0
        
        for report in reports:
            try:
                await process_citizen_report(report, ai_pipeline)
                processed_count += 1
                
                if processed_count % 10 == 0:
                    logger.info(f"Batch processing: {processed_count}/{len(reports)} completed")
            
            except Exception as e:
                logger.error(f"Failed to process report {report.id} in batch: {e}")
                continue
        
        logger.info(f"Batch processing completed: {processed_count}/{len(reports)} reports processed")
        
    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
