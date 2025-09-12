from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SearchType(str, Enum):
    TOPIC = "topic"
    CHANNEL = "channel"

class VideoMetadata(BaseModel):
    video_id: str
    title: str
    description: str
    channel_id: str
    channel_name: str
    duration: Optional[int] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    upload_date: Optional[datetime] = None
    tags: List[str] = []
    thumbnail_url: Optional[str] = None
    url: str

class ChannelMetadata(BaseModel):
    channel_id: str
    channel_name: str
    channel_url: str
    subscriber_count: Optional[int] = None
    video_count: Optional[int] = None
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    country: Optional[str] = None
    custom_url: Optional[str] = None

class ContentAnalysis(BaseModel):
    video_id: str
    title_analysis: Dict[str, Any]
    description_analysis: Dict[str, Any]
    semantic_score: float
    engagement_score: float
    predicted_performance: str
    key_patterns: List[str]
    emotional_tone: Dict[str, float]
    readability_score: float
    optimal_length_score: float

class SearchRequest(BaseModel):
    query: str
    search_type: SearchType = SearchType.TOPIC
    max_results: int = Field(default=20, le=50)
    analyze_content: bool = True

class ChannelAnalysisRequest(BaseModel):
    channel_url: str
    max_videos: int = Field(default=50, le=100)
    include_comments: bool = False
    deep_analysis: bool = True

class VideoAnalysisRequest(BaseModel):
    video_url: str
    include_comments: bool = True
    max_comments: int = Field(default=100, le=500)

class AnalysisResponse(BaseModel):
    status: str
    data: Optional[Any] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None

class PatternDetectionResult(BaseModel):
    pattern_type: str
    pattern_value: str
    frequency: int
    performance_impact: float
    examples: List[str]

class EngagementMetrics(BaseModel):
    views_to_likes_ratio: float
    views_to_comments_ratio: float
    engagement_rate: float
    virality_score: float
    sentiment_score: float

class ComparisonResult(BaseModel):
    channel_1: ChannelMetadata
    channel_2: ChannelMetadata
    metrics_comparison: Dict[str, Any]
    content_similarity: float
    audience_overlap_estimate: float
    competitive_advantages: Dict[str, List[str]]