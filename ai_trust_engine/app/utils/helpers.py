"""
Utility functions for SeaSense AI Trust Engine
"""

import hashlib
import re
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from geopy.distance import geodesic
import base64
import io
from PIL import Image


def calculate_location_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two GPS coordinates in kilometers."""
    try:
        return geodesic((lat1, lon1), (lat2, lon2)).kilometers
    except Exception:
        return float('inf')


def normalize_coordinates(latitude: float, longitude: float) -> Tuple[float, float]:
    """Normalize GPS coordinates to standard format."""
    # Ensure latitude is between -90 and 90
    lat = max(-90.0, min(90.0, latitude))
    
    # Ensure longitude is between -180 and 180
    lon = longitude
    while lon > 180:
        lon -= 360
    while lon < -180:
        lon += 360
    
    return lat, lon


def is_ocean_location(latitude: float, longitude: float) -> bool:
    """
    Simple check if coordinates are likely in ocean.
    In a real implementation, this would use a proper coastline database.
    """
    # For now, simple heuristic - assume locations far from major landmasses are ocean
    # This is a simplified implementation
    
    # Indian Ocean region (simplified)
    if 20 >= latitude >= -50 and 50 <= longitude <= 120:
        return True
    
    # Arabian Sea
    if 5 <= latitude <= 25 and 50 <= longitude <= 80:
        return True
    
    # Bay of Bengal
    if 5 <= latitude <= 25 and 80 <= longitude <= 100:
        return True
    
    return False


def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text."""
    hashtag_pattern = r'#\w+'
    hashtags = re.findall(hashtag_pattern, text, re.IGNORECASE)
    return [tag.lower() for tag in hashtags]


def extract_mentions(text: str) -> List[str]:
    """Extract mentions from text."""
    mention_pattern = r'@\w+'
    mentions = re.findall(mention_pattern, text, re.IGNORECASE)
    return [mention.lower() for mention in mentions]


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text."""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls


def clean_text(text: str) -> str:
    """Clean and normalize text for processing."""
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Remove mentions and hashtags for cleaner text
    text = re.sub(r'[@#]\w+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters (keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text


def generate_report_hash(content: str, location: Tuple[float, float], timestamp: datetime) -> str:
    """Generate a unique hash for a report to help with deduplication."""
    # Combine content, location (rounded), and timestamp (rounded to hour)
    location_rounded = (round(location[0], 4), round(location[1], 4))
    timestamp_rounded = timestamp.replace(minute=0, second=0, microsecond=0)
    
    hash_input = f"{content.lower().strip()}{location_rounded}{timestamp_rounded}"
    return hashlib.md5(hash_input.encode()).hexdigest()


def validate_image_data(base64_data: str) -> Dict[str, Any]:
    """Validate and analyze image data."""
    try:
        # Decode base64
        image_bytes = base64.b64decode(base64_data)
        
        # Check size
        size_mb = len(image_bytes) / (1024 * 1024)
        
        # Open image to get properties
        image = Image.open(io.BytesIO(image_bytes))
        
        return {
            'valid': True,
            'size_mb': size_mb,
            'width': image.width,
            'height': image.height,
            'format': image.format,
            'mode': image.mode,
            'total_pixels': image.width * image.height
        }
    
    except Exception as e:
        return {
            'valid': False,
            'error': str(e),
            'size_mb': 0,
            'width': 0,
            'height': 0
        }


def calculate_text_quality_score(text: str) -> float:
    """Calculate a quality score for text content."""
    if not text or not text.strip():
        return 0.0
    
    score = 0.0
    
    # Length score (optimal range: 50-500 characters)
    length = len(text.strip())
    if 50 <= length <= 500:
        length_score = 1.0
    elif length < 50:
        length_score = length / 50.0
    else:
        length_score = max(0.3, 1.0 - (length - 500) / 1000.0)
    
    score += 0.4 * length_score
    
    # Sentence structure (count of sentences)
    sentences = text.count('.') + text.count('!') + text.count('?')
    sentence_score = min(1.0, sentences / 5.0)
    score += 0.2 * sentence_score
    
    # Word diversity (unique words / total words)
    words = text.lower().split()
    if words:
        unique_words = len(set(words))
        word_diversity = unique_words / len(words)
        score += 0.2 * word_diversity
    
    # Has proper capitalization
    if text[0].isupper() if text else False:
        score += 0.1
    
    # Contains numbers (often indicates specific details)
    if re.search(r'\d', text):
        score += 0.1
    
    return min(1.0, score)


def time_window_filter(timestamp: datetime, window_hours: int = 24) -> bool:
    """Check if timestamp is within the specified time window."""
    now = datetime.utcnow()
    time_diff = now - timestamp
    return time_diff.total_seconds() <= window_hours * 3600


def spatial_cluster_check(location1: Tuple[float, float], 
                         location2: Tuple[float, float], 
                         threshold_km: float = 10.0) -> bool:
    """Check if two locations are within spatial clustering threshold."""
    distance = calculate_location_distance(location1[0], location1[1], location2[0], location2[1])
    return distance <= threshold_km


def calculate_engagement_rate(likes: int, shares: int, comments: int, followers: int) -> float:
    """Calculate social media engagement rate."""
    if followers <= 0:
        return 0.0
    
    total_engagement = likes + shares + comments
    engagement_rate = total_engagement / followers
    
    # Cap at 100% and return as percentage
    return min(1.0, engagement_rate) * 100


def format_trust_score_summary(trust_score: float) -> str:
    """Format trust score into human-readable summary."""
    if trust_score >= 0.9:
        return "Excellent"
    elif trust_score >= 0.8:
        return "Very High"
    elif trust_score >= 0.7:
        return "High"
    elif trust_score >= 0.6:
        return "Good"
    elif trust_score >= 0.5:
        return "Moderate"
    elif trust_score >= 0.4:
        return "Low"
    elif trust_score >= 0.3:
        return "Poor"
    else:
        return "Very Poor"


def get_priority_color(priority: str) -> str:
    """Get color code for priority level."""
    color_map = {
        'critical': '#FF0000',  # Red
        'high': '#FF8C00',      # Orange
        'medium': '#FFD700',    # Gold
        'low': '#32CD32'        # Green
    }
    return color_map.get(priority.lower(), '#808080')  # Gray for unknown


def batch_process_generator(items: List[Any], batch_size: int = 10):
    """Generator for batch processing of items."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def retry_with_exponential_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)
            
        def sync_wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
        
        import asyncio
        import inspect
        
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def generate_api_response(success: bool, message: str, data: Any = None, 
                         errors: List[str] = None, processing_time: float = None) -> Dict[str, Any]:
    """Generate standardized API response."""
    response = {
        'success': success,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    if errors:
        response['errors'] = errors
    
    if processing_time is not None:
        response['processing_time'] = processing_time
    
    return response


def mask_sensitive_data(text: str) -> str:
    """Mask sensitive information in text for logging."""
    # Mask email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', text)
    
    # Mask phone numbers (simple pattern)
    text = re.sub(r'\b\d{10,}\b', '***********', text)
    
    # Mask credit card-like numbers
    text = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '****-****-****-****', text)
    
    return text
