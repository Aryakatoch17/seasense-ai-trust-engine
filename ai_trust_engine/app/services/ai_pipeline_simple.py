"""
Simplified AI Processing Pipeline for SeaSense Trust Engine
Works without heavy ML dependencies for basic demonstration
"""

import asyncio
import logging
import time
import re
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime
import hashlib
import json

from app.models.schemas import (
    CitizenReport, SocialMediaPost, TrustScore, 
    DuplicateDetectionResult, HazardType
)
from config.settings import get_settings

logger = logging.getLogger(__name__)


class SimplifiedAIPipeline:
    """Simplified AI processing pipeline for demonstration purposes."""
    
    def __init__(self):
        self.settings = get_settings()
        self.is_initialized = False
        
        # Cache for duplicate detection
        self.report_embeddings = {}
        self.report_clusters = {}
        
        # Simple keyword-based hazard detection
        self.hazard_keywords = {
            HazardType.TSUNAMI: ['tsunami', 'giant wave', 'wall of water', 'earthquake wave'],
            HazardType.STORM: ['storm', 'cyclone', 'hurricane', 'typhoon', 'wind', 'rain'],
            HazardType.HIGH_WAVES: ['high waves', 'big waves', 'large waves', 'massive waves', 'huge waves'],
            HazardType.POLLUTION: ['pollution', 'oil spill', 'contamination', 'toxic', 'chemicals'],
            HazardType.DEBRIS: ['debris', 'garbage', 'waste', 'floating objects', 'trash'],
            HazardType.UNUSUAL_CURRENT: ['current', 'undertow', 'rip current', 'strange current'],
            HazardType.TEMPERATURE_ANOMALY: ['hot water', 'cold water', 'temperature', 'warm', 'cool'],
            HazardType.OTHER: ['hazard', 'danger', 'emergency', 'alert', 'warning']
        }
        
    async def initialize(self):
        """Initialize the simplified pipeline."""
        try:
            logger.info("Initializing Simplified AI Pipeline...")
            
            # Simple initialization - no heavy models
            self.is_initialized = True
            logger.info("Simplified AI Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Simplified AI Pipeline: {e}")
            raise
    
    async def process_citizen_report(self, report: CitizenReport) -> Dict[str, Any]:
        """Process a citizen report through the simplified pipeline."""
        if not self.is_initialized:
            raise RuntimeError("AI Pipeline not initialized")
        
        start_time = time.time()
        
        try:
            # Extract and process text features
            text_features = await self._process_text_simple(report.description, report.language)
            
            # Process images if available (simplified)
            image_features = await self._process_images_simple(report.images or [])
            
            # Detect duplicates
            duplicate_result = await self._detect_duplicates_simple(report, text_features)
            
            # Perform hazard classification
            hazard_classification = await self._classify_hazards_simple(report.description)
            
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
    
    async def _process_text_simple(self, text: str, language: str = "en") -> Dict[str, Any]:
        """Simple text processing without heavy NLP models."""
        try:
            # Basic text analysis
            words = text.lower().split()
            word_count = len(words)
            char_count = len(text)
            
            # Simple language detection (based on character patterns)
            detected_language = self._detect_language_simple(text)
            lang_confidence = 0.9 if detected_language == language else 0.7
            
            # Simple sentiment analysis (keyword-based)
            sentiment_scores = self._analyze_sentiment_simple(text)
            
            # Create simple text embedding (word frequency based)
            text_embedding = self._create_text_embedding_simple(words)
            
            # Text quality metrics
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
    
    async def _process_images_simple(self, images: List) -> Dict[str, Any]:
        """Simple image processing without heavy CV models."""
        try:
            image_features = {
                'count': len(images),
                'clip_scores': [],
                'detected_objects': [],
                'quality_scores': []
            }
            
            for i, img_data in enumerate(images):
                # Mock image processing
                clip_score = 0.7 + (i * 0.1) % 0.3  # Mock varying scores
                image_features['clip_scores'].append(clip_score)
                
                # Mock object detection
                objects = ['water', 'waves', 'people'] if i == 0 else ['debris', 'coast']
                image_features['detected_objects'].append(objects)
                
                # Mock quality assessment
                quality_score = 0.8 - (i * 0.1) % 0.3  # Mock varying quality
                image_features['quality_scores'].append(quality_score)
            
            # Calculate average scores
            if image_features['clip_scores']:
                image_features['avg_clip_score'] = np.mean(image_features['clip_scores'])
                image_features['avg_quality_score'] = np.mean(image_features['quality_scores'])
            
            return image_features
            
        except Exception as e:
            logger.error(f"Error processing images: {e}")
            return {'count': 0, 'clip_scores': [], 'detected_objects': [], 'quality_scores': []}
    
    def _detect_language_simple(self, text: str) -> str:
        """Simple language detection based on character patterns."""
        # Very basic detection - can be improved
        if any(ord(char) > 127 for char in text):
            # Has non-ASCII characters, likely not English
            return "hi"  # Assume Hindi for simplicity
        return "en"
    
    def _analyze_sentiment_simple(self, text: str) -> Dict[str, float]:
        """Simple sentiment analysis using keyword matching."""
        positive_words = ['good', 'safe', 'calm', 'clear', 'beautiful', 'peaceful']
        negative_words = ['danger', 'emergency', 'massive', 'huge', 'scary', 'terrible', 'bad', 'urgent']
        neutral_words = ['report', 'observe', 'see', 'notice', 'location']
        
        words = text.lower().split()
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        neutral_count = sum(1 for word in words if word in neutral_words)
        
        total = max(1, positive_count + negative_count + neutral_count)
        
        return {
            'POSITIVE': positive_count / total,
            'NEGATIVE': negative_count / total,
            'NEUTRAL': neutral_count / total
        }
    
    def _create_text_embedding_simple(self, words: List[str]) -> np.ndarray:
        """Create a simple text embedding based on word frequency."""
        # Simple bag-of-words approach with common ocean/hazard terms
        common_terms = [
            'wave', 'water', 'sea', 'ocean', 'beach', 'coast', 'shore',
            'storm', 'wind', 'rain', 'debris', 'pollution', 'danger',
            'emergency', 'safety', 'rescue', 'help', 'alert', 'warning'
        ]
        
        embedding = np.zeros(len(common_terms))
        for i, term in enumerate(common_terms):
            embedding[i] = sum(1 for word in words if term in word.lower())
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    async def _detect_duplicates_simple(self, report: CitizenReport, text_features: Dict) -> DuplicateDetectionResult:
        """Simple duplicate detection using text and location similarity."""
        try:
            # Calculate similarity with existing reports
            similarities = []
            similar_report_ids = []
            
            current_embedding = text_features['embedding']
            current_location = (report.location.latitude, report.location.longitude)
            
            for existing_id, existing_data in self.report_embeddings.items():
                existing_embedding = existing_data['embedding']
                existing_location = existing_data['location']
                
                # Text similarity (cosine similarity)
                text_sim = np.dot(current_embedding, existing_embedding)
                
                # Location similarity (inverse distance)
                location_sim = self._calculate_location_similarity(current_location, existing_location)
                
                # Combined similarity
                combined_sim = 0.7 * text_sim + 0.3 * location_sim
                
                if combined_sim > self.settings.SIMILARITY_THRESHOLD:
                    similarities.append(combined_sim)
                    similar_report_ids.append(existing_id)
            
            # Determine if this is a duplicate
            is_duplicate = len(similarities) > 0
            max_similarity = max(similarities) if similarities else 0.0
            
            # Store embedding for future comparisons
            self.report_embeddings[report.id] = {
                'embedding': current_embedding,
                'location': current_location
            }
            
            # Simple cluster assignment
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
    
    def _calculate_location_similarity(self, loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
        """Calculate location similarity based on distance."""
        try:
            # Simple distance calculation (Euclidean distance in degrees)
            lat_diff = abs(loc1[0] - loc2[0])
            lon_diff = abs(loc1[1] - loc2[1])
            distance = (lat_diff**2 + lon_diff**2)**0.5
            
            # Convert to similarity (inverse of distance, normalized)
            max_distance = 1.0  # Approximately 111 km at equator
            similarity = max(0.0, 1.0 - (distance / max_distance))
            
            return similarity
            
        except Exception:
            return 0.0
    
    async def _classify_hazards_simple(self, text: str) -> Dict[str, Any]:
        """Simple hazard classification using keyword matching."""
        try:
            text_lower = text.lower()
            
            # Score each hazard type
            hazard_scores = {}
            for hazard_type, keywords in self.hazard_keywords.items():
                score = 0
                for keyword in keywords:
                    if keyword in text_lower:
                        score += 1
                
                # Normalize by number of keywords
                hazard_scores[hazard_type.value] = score / len(keywords)
            
            # Find the best match
            if hazard_scores:
                best_hazard = max(hazard_scores.keys(), key=lambda k: hazard_scores[k])
                confidence = hazard_scores[best_hazard]
            else:
                best_hazard = HazardType.OTHER.value
                confidence = 0.1
            
            return {
                'predicted_hazard': best_hazard,
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
        """Calculate trust score using simplified algorithms."""
        try:
            start_time = time.time()
            
            # Extract features
            text_features = processing_results['text_features']
            image_features = processing_results['image_features']
            duplicate_result = processing_results['duplicate_result']
            hazard_classification = processing_results['hazard_classification']
            
            # Component scores
            content_credibility = await self._score_content_credibility_simple(
                text_features, image_features, hazard_classification
            )
            
            source_reliability = await self._score_source_reliability_simple(report)
            
            temporal_consistency = 0.75  # Mock score
            
            spatial_consistency = await self._score_spatial_consistency_simple(report)
            
            cross_verification = await self._score_cross_verification_simple(
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
            confidence = 0.8  # Mock confidence
            
            # Identify potential issues
            warnings = []
            if duplicate_result.is_duplicate:
                warnings.append("Report may be duplicate of existing reports")
            if text_features['word_count'] < 20:
                warnings.append("Report description is very short")
            if image_features['count'] == 0:
                warnings.append("No images provided")
            
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
                model_version="simplified-v1.0.0",
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
                model_version="simplified-v1.0.0",
                factors={},
                warnings=["Error in processing"]
            )
    
    async def _score_content_credibility_simple(self, text_features: Dict, image_features: Dict, hazard_classification: Dict) -> float:
        """Simple content credibility scoring."""
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
    
    async def _score_source_reliability_simple(self, report: CitizenReport) -> float:
        """Simple source reliability scoring."""
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
    
    async def _score_spatial_consistency_simple(self, report: CitizenReport) -> float:
        """Simple spatial consistency scoring."""
        # Basic check if coordinates are in ocean/coastal areas
        lat, lon = report.location.latitude, report.location.longitude
        
        # India coastal regions (simplified check)
        coastal_regions = [
            (8, 25, 68, 88),   # Western and Eastern coasts
            (6, 15, 75, 85),   # Southern India
        ]
        
        is_coastal = False
        for min_lat, max_lat, min_lon, max_lon in coastal_regions:
            if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                is_coastal = True
                break
        
        return 0.8 if is_coastal else 0.5
    
    async def _score_cross_verification_simple(self, report: CitizenReport, social_media_posts: List[SocialMediaPost]) -> float:
        """Simple cross-verification scoring."""
        if not social_media_posts:
            return 0.5  # Neutral score when no social media data
        
        # Simple implementation: count of related posts
        verification_score = min(1.0, len(social_media_posts) / 5.0)
        return verification_score
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            # Clear caches
            self.report_embeddings.clear()
            self.report_clusters.clear()
            
            logger.info("Simplified AI Pipeline cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# Alias for backward compatibility
AIPipeline = SimplifiedAIPipeline
