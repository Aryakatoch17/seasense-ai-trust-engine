"""
AI Processing Pipeline for SeaSense Trust Engine
Handles NLP, Computer Vision, and cross-verification
"""

import asyncio
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel, pipeline
import clip
import cv2
from PIL import Image
import io
import base64
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import hashlib

from app.models.schemas import (
    CitizenReport, SocialMediaPost, TrustScore, 
    DuplicateDetectionResult, HazardType
)
from config.settings import get_settings

logger = logging.getLogger(__name__)


class AIPipeline:
    """Main AI processing pipeline for trust scoring."""
    
    def __init__(self):
        self.settings = get_settings()
        self.models = {}
        self.tokenizers = {}
        self.pipelines = {}
        self.is_initialized = False
        
        # Cache for duplicate detection
        self.report_embeddings = {}
        self.report_clusters = {}
        
    async def initialize(self):
        """Initialize all AI models and components."""
        try:
            logger.info("Initializing AI Pipeline...")
            
            # Initialize NLP models
            await self._initialize_nlp_models()
            
            # Initialize Computer Vision models
            await self._initialize_cv_models()
            
            # Initialize clustering for duplicate detection
            await self._initialize_clustering()
            
            self.is_initialized = True
            logger.info("AI Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Pipeline: {e}")
            raise
    
    async def _initialize_nlp_models(self):
        """Initialize NLP models (mBERT, sentiment analysis, etc.)."""
        try:
            # mBERT for multilingual text processing
            logger.info("Loading mBERT model...")
            self.tokenizers['mbert'] = AutoTokenizer.from_pretrained(
                self.settings.MBERT_MODEL
            )
            self.models['mbert'] = AutoModel.from_pretrained(
                self.settings.MBERT_MODEL
            )
            
            # Sentiment analysis pipeline
            logger.info("Loading sentiment analysis pipeline...")
            self.pipelines['sentiment'] = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
            
            # Language detection
            logger.info("Loading language detection pipeline...")
            self.pipelines['language'] = pipeline(
                "text-classification",
                model="papluca/xlm-roberta-base-language-detection"
            )
            
            # Hazard classification
            logger.info("Loading hazard classification pipeline...")
            self.pipelines['hazard'] = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
            
            logger.info("NLP models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize NLP models: {e}")
            raise
    
    async def _initialize_cv_models(self):
        """Initialize Computer Vision models (CLIP, YOLO, etc.)."""
        try:
            # CLIP for image-text alignment
            logger.info("Loading CLIP model...")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.models['clip'], self.models['clip_preprocess'] = clip.load(
                "ViT-B/32", device=device
            )
            
            # Object detection for hazard identification
            logger.info("Loading object detection model...")
            self.pipelines['object_detection'] = pipeline(
                "object-detection",
                model="hustvl/yolos-tiny"
            )
            
            # Image quality assessment
            logger.info("Setting up image quality assessment...")
            # Using simple CV techniques for now
            
            logger.info("Computer Vision models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize CV models: {e}")
            raise
    
    async def _initialize_clustering(self):
        """Initialize clustering algorithms for duplicate detection."""
        try:
            self.clustering_model = DBSCAN(
                eps=self.settings.CLUSTERING_EPS,
                min_samples=self.settings.MIN_SAMPLES,
                metric='cosine'
            )
            logger.info("Clustering initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize clustering: {e}")
            raise
    
    async def process_citizen_report(self, report: CitizenReport) -> Dict[str, Any]:
        """Process a citizen report through the AI pipeline."""
        if not self.is_initialized:
            raise RuntimeError("AI Pipeline not initialized")
        
        start_time = time.time()
        
        try:
            # Extract and process text features
            text_features = await self._process_text(report.description, report.language)
            
            # Process images if available
            image_features = {}
            if report.images:
                image_features = await self._process_images(report.images, report.description)
            
            # Detect duplicates
            duplicate_result = await self._detect_duplicates(report, text_features, image_features)
            
            # Perform hazard classification
            hazard_classification = await self._classify_hazards(report.description)
            
            processing_time = time.time() - start_time
            
            return {
                'text_features': text_features,
                'image_features': image_features,
                'duplicate_result': duplicate_result,
                'hazard_classification': hazard_classification,
                'processing_time': processing_time
            }
            
        except Exception as e:
            logger.error(f"Error processing citizen report: {e}")
            raise
    
    async def _process_text(self, text: str, language: str = "en") -> Dict[str, Any]:
        """Process text content using NLP models."""
        try:
            # Language detection
            lang_result = self.pipelines['language'](text)
            detected_language = lang_result[0]['label']
            lang_confidence = lang_result[0]['score']
            
            # Sentiment analysis
            sentiment_result = self.pipelines['sentiment'](text)
            sentiment_scores = {item['label']: item['score'] for item in sentiment_result[0]}
            
            # Generate text embeddings using mBERT
            inputs = self.tokenizers['mbert'](
                text, 
                return_tensors="pt", 
                truncation=True, 
                padding=True,
                max_length=512
            )
            
            with torch.no_grad():
                outputs = self.models['mbert'](**inputs)
                text_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            
            # Text quality metrics
            word_count = len(text.split())
            char_count = len(text)
            has_urls = 'http' in text.lower()
            has_mentions = '@' in text
            has_hashtags = '#' in text
            
            return {
                'embedding': text_embedding,
                'detected_language': detected_language,
                'language_confidence': lang_confidence,
                'sentiment_scores': sentiment_scores,
                'word_count': word_count,
                'char_count': char_count,
                'has_urls': has_urls,
                'has_mentions': has_mentions,
                'has_hashtags': has_hashtags
            }
            
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            raise
    
    async def _process_images(self, images: List, description: str) -> Dict[str, Any]:
        """Process images using Computer Vision models."""
        try:
            image_features = {
                'count': len(images),
                'clip_scores': [],
                'detected_objects': [],
                'quality_scores': []
            }
            
            for img_data in images:
                # Decode base64 image
                image_bytes = base64.b64decode(img_data.base64_data)
                image = Image.open(io.BytesIO(image_bytes))
                
                # CLIP image-text alignment
                clip_score = await self._calculate_clip_score(image, description)
                image_features['clip_scores'].append(clip_score)
                
                # Object detection
                objects = self.pipelines['object_detection'](image)
                image_features['detected_objects'].append(objects)
                
                # Image quality assessment
                quality_score = await self._assess_image_quality(image)
                image_features['quality_scores'].append(quality_score)
            
            # Calculate average scores
            if image_features['clip_scores']:
                image_features['avg_clip_score'] = np.mean(image_features['clip_scores'])
                image_features['avg_quality_score'] = np.mean(image_features['quality_scores'])
            
            return image_features
            
        except Exception as e:
            logger.error(f"Error processing images: {e}")
            raise
    
    async def _calculate_clip_score(self, image: Image.Image, text: str) -> float:
        """Calculate CLIP similarity between image and text."""
        try:
            device = next(self.models['clip'].parameters()).device
            
            # Preprocess image
            image_input = self.models['clip_preprocess'](image).unsqueeze(0).to(device)
            
            # Tokenize text
            text_input = clip.tokenize([text]).to(device)
            
            with torch.no_grad():
                # Get features
                image_features = self.models['clip'].encode_image(image_input)
                text_features = self.models['clip'].encode_text(text_input)
                
                # Calculate similarity
                similarity = torch.cosine_similarity(image_features, text_features)
                
            return float(similarity.cpu().numpy()[0])
            
        except Exception as e:
            logger.error(f"Error calculating CLIP score: {e}")
            return 0.0
    
    async def _assess_image_quality(self, image: Image.Image) -> float:
        """Assess image quality using computer vision techniques."""
        try:
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Calculate various quality metrics
            
            # 1. Sharpness (Laplacian variance)
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 2. Brightness
            brightness = np.mean(gray)
            
            # 3. Contrast
            contrast = np.std(gray)
            
            # 4. Resolution score
            height, width = gray.shape
            resolution_score = min(1.0, (height * width) / (1920 * 1080))
            
            # Combine metrics into overall quality score
            # Normalize and weight the metrics
            sharpness_norm = min(1.0, sharpness / 1000)  # Normalize sharpness
            brightness_norm = 1.0 - abs(brightness - 128) / 128  # Optimal brightness around 128
            contrast_norm = min(1.0, contrast / 64)  # Normalize contrast
            
            quality_score = (
                0.4 * sharpness_norm + 
                0.2 * brightness_norm + 
                0.2 * contrast_norm + 
                0.2 * resolution_score
            )
            
            return max(0.0, min(1.0, quality_score))
            
        except Exception as e:
            logger.error(f"Error assessing image quality: {e}")
            return 0.5  # Default quality score
    
    async def _detect_duplicates(self, report: CitizenReport, text_features: Dict, image_features: Dict) -> DuplicateDetectionResult:
        """Detect duplicate reports using clustering and similarity."""
        try:
            # Create composite embedding for the report
            report_embedding = await self._create_report_embedding(report, text_features, image_features)
            
            # Calculate similarity with existing reports
            similarities = []
            similar_report_ids = []
            
            for existing_id, existing_embedding in self.report_embeddings.items():
                similarity = cosine_similarity(
                    [report_embedding], [existing_embedding]
                )[0][0]
                
                if similarity > self.settings.SIMILARITY_THRESHOLD:
                    similarities.append(similarity)
                    similar_report_ids.append(existing_id)
            
            # Determine if this is a duplicate
            is_duplicate = len(similarities) > 0
            max_similarity = max(similarities) if similarities else 0.0
            
            # Store embedding for future comparisons
            self.report_embeddings[report.id] = report_embedding
            
            # Cluster assignment (simplified)
            cluster_id = None
            if is_duplicate:
                cluster_id = f"cluster_{hashlib.md5(str(sorted(similar_report_ids)).encode()).hexdigest()[:8]}"
            
            return DuplicateDetectionResult(
                is_duplicate=is_duplicate,
                similarity_score=max_similarity,
                similar_reports=similar_report_ids,
                cluster_id=cluster_id,
                confidence=0.8 if is_duplicate else 0.9
            )
            
        except Exception as e:
            logger.error(f"Error detecting duplicates: {e}")
            return DuplicateDetectionResult(
                is_duplicate=False,
                similarity_score=0.0,
                similar_reports=[],
                cluster_id=None,
                confidence=0.5
            )
    
    async def _create_report_embedding(self, report: CitizenReport, text_features: Dict, image_features: Dict) -> np.ndarray:
        """Create a composite embedding for a report."""
        try:
            # Text embedding
            text_emb = text_features['embedding']
            
            # Location embedding (simple coordinate encoding)
            location_emb = np.array([
                report.location.latitude / 90.0,  # Normalize latitude
                report.location.longitude / 180.0,  # Normalize longitude
            ])
            
            # Hazard type embedding (one-hot encoding)
            hazard_types = list(HazardType)
            hazard_emb = np.zeros(len(hazard_types))
            if report.hazard_type in hazard_types:
                hazard_emb[hazard_types.index(report.hazard_type)] = 1.0
            
            # Image embedding (average CLIP score if available)
            image_emb = np.array([
                image_features.get('avg_clip_score', 0.0),
                image_features.get('count', 0) / 10.0  # Normalize image count
            ])
            
            # Concatenate all embeddings
            composite_embedding = np.concatenate([
                text_emb,
                location_emb,
                hazard_emb,
                image_emb
            ])
            
            return composite_embedding
            
        except Exception as e:
            logger.error(f"Error creating report embedding: {e}")
            # Return a zero embedding as fallback
            return np.zeros(768 + 2 + len(list(HazardType)) + 2)
    
    async def _classify_hazards(self, text: str) -> Dict[str, Any]:
        """Classify hazard types from text description."""
        try:
            # Define candidate hazard labels
            candidate_labels = [hazard.value for hazard in HazardType]
            
            # Perform zero-shot classification
            result = self.pipelines['hazard'](text, candidate_labels)
            
            # Format results
            hazard_scores = {
                label: score for label, score in 
                zip(result['labels'], result['scores'])
            }
            
            # Get top predicted hazard
            top_hazard = result['labels'][0]
            confidence = result['scores'][0]
            
            return {
                'predicted_hazard': top_hazard,
                'confidence': confidence,
                'all_scores': hazard_scores
            }
            
        except Exception as e:
            logger.error(f"Error classifying hazards: {e}")
            return {
                'predicted_hazard': HazardType.OTHER.value,
                'confidence': 0.0,
                'all_scores': {}
            }
    
    async def calculate_trust_score(self, 
                                  report: CitizenReport, 
                                  processing_results: Dict[str, Any],
                                  social_media_posts: List[SocialMediaPost] = None) -> TrustScore:
        """Calculate comprehensive trust score for a report."""
        try:
            start_time = time.time()
            
            # Extract features
            text_features = processing_results['text_features']
            image_features = processing_results['image_features']
            duplicate_result = processing_results['duplicate_result']
            hazard_classification = processing_results['hazard_classification']
            
            # Component scores
            content_credibility = await self._score_content_credibility(
                text_features, image_features, hazard_classification
            )
            
            source_reliability = await self._score_source_reliability(report)
            
            temporal_consistency = await self._score_temporal_consistency(report)
            
            spatial_consistency = await self._score_spatial_consistency(report)
            
            cross_verification = await self._score_cross_verification(
                report, social_media_posts or []
            )
            
            # Calculate overall score (weighted average)
            weights = {
                'content_credibility': 0.3,
                'source_reliability': 0.2,
                'temporal_consistency': 0.15,
                'spatial_consistency': 0.15,
                'cross_verification': 0.2
            }
            
            overall_score = (
                weights['content_credibility'] * content_credibility +
                weights['source_reliability'] * source_reliability +
                weights['temporal_consistency'] * temporal_consistency +
                weights['spatial_consistency'] * spatial_consistency +
                weights['cross_verification'] * cross_verification
            )
            
            # Apply penalties for duplicates
            if duplicate_result.is_duplicate:
                overall_score *= 0.7  # Reduce score for duplicates
            
            # Ensure score is within bounds
            overall_score = max(0.0, min(1.0, overall_score))
            
            # Calculate confidence
            confidence = await self._calculate_confidence(processing_results)
            
            # Identify potential issues
            warnings = await self._identify_warnings(processing_results, overall_score)
            
            processing_time = time.time() - start_time
            
            return TrustScore(
                overall_score=overall_score,
                content_credibility=content_credibility,
                source_reliability=source_reliability,
                temporal_consistency=temporal_consistency,
                spatial_consistency=spatial_consistency,
                cross_verification=cross_verification,
                confidence=confidence,
                processing_time=processing_time,
                model_version="v1.0.0",
                factors={
                    'language_confidence': text_features['language_confidence'],
                    'image_quality': image_features.get('avg_quality_score', 0.0),
                    'clip_alignment': image_features.get('avg_clip_score', 0.0),
                    'hazard_confidence': hazard_classification['confidence']
                },
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Error calculating trust score: {e}")
            # Return default score
            return TrustScore(
                overall_score=self.settings.DEFAULT_TRUST_SCORE,
                content_credibility=0.5,
                source_reliability=0.5,
                temporal_consistency=0.5,
                spatial_consistency=0.5,
                cross_verification=0.5,
                confidence=0.5,
                processing_time=0.0,
                model_version="v1.0.0",
                factors={},
                warnings=["Error in processing"]
            )
    
    async def _score_content_credibility(self, text_features: Dict, image_features: Dict, hazard_classification: Dict) -> float:
        """Score content credibility based on text and image analysis."""
        score = 0.0
        
        # Text quality factors
        lang_confidence = text_features['language_confidence']
        word_count = text_features['word_count']
        
        # Language confidence (higher is better)
        score += 0.3 * lang_confidence
        
        # Text length (optimal range: 50-500 words)
        if 50 <= word_count <= 500:
            length_score = 1.0
        elif word_count < 50:
            length_score = word_count / 50.0
        else:
            length_score = max(0.5, 1.0 - (word_count - 500) / 1000.0)
        score += 0.2 * length_score
        
        # Hazard classification confidence
        score += 0.2 * hazard_classification['confidence']
        
        # Image quality (if available)
        if image_features.get('count', 0) > 0:
            img_quality = image_features.get('avg_quality_score', 0.0)
            clip_score = image_features.get('avg_clip_score', 0.0)
            score += 0.15 * img_quality + 0.15 * clip_score
        else:
            score += 0.3 * 0.7  # Slightly penalize for no images
        
        return max(0.0, min(1.0, score))
    
    async def _score_source_reliability(self, report: CitizenReport) -> float:
        """Score source reliability based on reporter information."""
        score = 0.5  # Base score
        
        # Reporter reputation (if available)
        if report.reporter_reputation is not None:
            score += 0.4 * report.reporter_reputation
        
        # Device information availability
        if report.device_info:
            score += 0.1
        
        # GPS accuracy (if available)
        if report.location.accuracy is not None:
            # Better accuracy = higher score
            accuracy_score = max(0.0, 1.0 - report.location.accuracy / 100.0)
            score += 0.2 * accuracy_score
        
        return max(0.0, min(1.0, score))
    
    async def _score_temporal_consistency(self, report: CitizenReport) -> float:
        """Score temporal consistency."""
        # For now, return a baseline score
        # In a real implementation, this would check:
        # - Report timing vs. historical patterns
        # - Seasonal patterns
        # - Time zone consistency
        return 0.7
    
    async def _score_spatial_consistency(self, report: CitizenReport) -> float:
        """Score spatial consistency."""
        # For now, return a baseline score
        # In a real implementation, this would check:
        # - Geographic plausibility
        # - Proximity to known hazard areas
        # - Ocean vs. land location validation
        return 0.7
    
    async def _score_cross_verification(self, report: CitizenReport, social_media_posts: List[SocialMediaPost]) -> float:
        """Score cross-verification with other sources."""
        if not social_media_posts:
            return 0.5  # Neutral score when no social media data
        
        # Simple implementation: count of related posts
        verification_score = min(1.0, len(social_media_posts) / 5.0)
        return verification_score
    
    async def _calculate_confidence(self, processing_results: Dict) -> float:
        """Calculate confidence in the trust score."""
        confidences = []
        
        # Text processing confidence
        confidences.append(processing_results['text_features']['language_confidence'])
        
        # Hazard classification confidence
        confidences.append(processing_results['hazard_classification']['confidence'])
        
        # Duplicate detection confidence
        confidences.append(processing_results['duplicate_result'].confidence)
        
        # Image processing confidence (if available)
        if processing_results['image_features'].get('count', 0) > 0:
            confidences.append(processing_results['image_features'].get('avg_quality_score', 0.5))
        
        return np.mean(confidences)
    
    async def _identify_warnings(self, processing_results: Dict, overall_score: float) -> List[str]:
        """Identify potential issues and warnings."""
        warnings = []
        
        text_features = processing_results['text_features']
        duplicate_result = processing_results['duplicate_result']
        
        # Language detection issues
        if text_features['language_confidence'] < 0.8:
            warnings.append("Low confidence in language detection")
        
        # Duplicate detection
        if duplicate_result.is_duplicate:
            warnings.append("Report may be duplicate of existing reports")
        
        # Very low trust score
        if overall_score < 0.3:
            warnings.append("Very low trust score - verify manually")
        
        # Short text
        if text_features['word_count'] < 20:
            warnings.append("Report description is very short")
        
        # No images for visual hazards
        image_count = processing_results['image_features'].get('count', 0)
        if image_count == 0:
            warnings.append("No images provided - consider requesting visual evidence")
        
        return warnings
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            # Clear model caches
            self.models.clear()
            self.tokenizers.clear()
            self.pipelines.clear()
            
            # Clear embeddings cache
            self.report_embeddings.clear()
            self.report_clusters.clear()
            
            logger.info("AI Pipeline cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
