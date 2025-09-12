from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from typing import List, Dict, Any, Optional
import asyncio
import json

from models.schemas import (
    SearchRequest, ChannelAnalysisRequest, VideoAnalysisRequest,
    AnalysisResponse, VideoMetadata, ChannelMetadata, ContentAnalysis
)
from services.youtube_extractor import YouTubeExtractor
from services.content_analyzer import ContentAnalyzer
from services.viral_insights_analyzer import ViralInsightsAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Content Analyzer API",
    description="Analyze YouTube channels and content patterns",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3025", "http://127.0.0.1:3025", "http://localhost:3026", "http://127.0.0.1:3026"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
youtube_extractor = YouTubeExtractor()
content_analyzer = ContentAnalyzer()
viral_insights = ViralInsightsAnalyzer()

# In-memory cache (replace with Redis in production)
cache = {}
CACHE_TTL = 3600  # 1 hour

@app.get("/")
async def root():
    return {
        "message": "YouTube Content Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search",
            "channel_analysis": "/api/channel/analyze",
            "video_analysis": "/api/video/analyze",
            "patterns": "/api/patterns/detect"
        }
    }

@app.post("/api/search", response_model=AnalysisResponse)
async def search_content(request: SearchRequest):
    """Search for YouTube content by topic or channel"""
    try:
        start_time = time.time()
        
        # Log the search query
        logger.info(f"🔍 Search request - Type: {request.search_type}, Query: '{request.query}', Max results: {request.max_results}")
        
        # Check cache
        cache_key = f"search:{request.query}:{request.search_type}:{request.max_results}"
        if cache_key in cache:
            cached_data = cache[cache_key]
            if time.time() - cached_data['timestamp'] < CACHE_TTL:
                return AnalysisResponse(
                    status="success",
                    data=cached_data['data'],
                    processing_time=0.01
                )
        
        results = []
        
        if request.search_type == "topic":
            # Search for videos on the topic
            videos = youtube_extractor.search_videos(request.query, request.max_results)
            
            # Get top channels for this topic
            channels = youtube_extractor.get_topic_channels(request.query, min(10, request.max_results // 2))
            
            # Analyze content if requested
            if request.analyze_content and videos:
                for video in videos[:10]:  # Analyze top 10
                    if video.get('url'):
                        details = youtube_extractor.get_video_details(video['url'])
                        if details:
                            video['details'] = details
                            video['analysis'] = content_analyzer.analyze_title(details.get('title', ''))
            
            results = {
                'videos': videos,
                'top_channels': channels,
                'query': request.query,
                'total_results': len(videos)
            }
            
        else:  # channel search
            # Search for channels
            channels = youtube_extractor.search_channels(request.query, request.max_results)
            
            # Get sample videos from top channels
            for channel in channels[:3]:  # Get videos from top 3 channels
                if channel.get('channel_url'):
                    videos = youtube_extractor.get_channel_videos(channel['channel_url'], 5)
                    channel['sample_videos'] = videos
            
            results = {
                'channels': channels,
                'query': request.query,
                'total_results': len(channels)
            }
        
        # Cache the results
        cache[cache_key] = {
            'data': results,
            'timestamp': time.time()
        }
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            status="success",
            data=results,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/channel/analyze", response_model=AnalysisResponse)
async def analyze_channel(request: ChannelAnalysisRequest):
    """Analyze a YouTube channel comprehensively"""
    try:
        start_time = time.time()
        
        # Log the channel analysis request
        logger.info(f"📺 Channel analysis request - URL: '{request.channel_url}', Max videos: {request.max_videos}")
        
        # Get channel info
        channel_info = youtube_extractor.get_channel_info(request.channel_url)
        if not channel_info:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        # Get channel videos
        videos = youtube_extractor.get_channel_videos(request.channel_url, request.max_videos)
        
        # Analyze videos
        analyzed_videos = []
        logger.info(f"📊 Starting analysis of {len(videos[:20])} videos...")
        
        for idx, video in enumerate(videos[:20]):  # Analyze top 20 videos in detail
            if video.get('url'):
                logger.info(f"  🎬 [{idx+1}/20] Analyzing video: {video.get('title', 'Unknown')[:50]}...")
                
                try:
                    details = youtube_extractor.get_video_details(video['url'])
                    
                    if details:
                        logger.info(f"    ✅ Video details extracted successfully")
                        
                        # Analyze content
                        title_analysis = content_analyzer.analyze_title(details.get('title', ''))
                        desc_analysis = content_analyzer.analyze_description(details.get('description', ''))
                        engagement_prediction = content_analyzer.predict_engagement(details)
                        
                        # Add viral insights
                        hook_analysis = viral_insights.analyze_hooks(details.get('title', ''))
                        title_performance = viral_insights.analyze_title_performance_factors(
                            details.get('title', ''), 
                            details.get('view_count', 0)
                        )
                        
                        analyzed_videos.append({
                            'video': details,
                            'title_analysis': title_analysis,
                            'description_analysis': desc_analysis,
                            'engagement_prediction': engagement_prediction,
                            'viral_insights': {
                                'hooks': hook_analysis,
                                'title_optimization': title_performance
                            }
                        })
                        logger.info(f"    ✅ Analysis complete for video {idx+1}")
                    else:
                        logger.warning(f"    ⚠️ Failed to get details for: {video['url']}")
                        
                except Exception as e:
                    logger.error(f"    ❌ Error analyzing video {idx+1}: {str(e)}")
                    continue
            else:
                logger.warning(f"  ⚠️ No URL for video: {video.get('title', 'Unknown')}")
        
        # Find patterns across videos
        logger.info(f"🔍 Finding patterns across {len(analyzed_videos)} analyzed videos...")
        patterns = {}
        if analyzed_videos:
            patterns = content_analyzer.find_content_patterns([v['video'] for v in analyzed_videos])
            logger.info(f"  ✅ Patterns extracted successfully")
        else:
            logger.warning(f"  ⚠️ No analyzed videos available for pattern extraction")
            patterns = {
                'error': 'No videos were successfully analyzed',
                'common_patterns': {},
                'average_title_length': 0,
                'performance_patterns': [],
                'main_topics': [],
                'content_consistency': 0
            }
        
        # Calculate channel metrics
        logger.info(f"📈 Calculating channel metrics...")
        channel_metrics = _calculate_channel_metrics(analyzed_videos)
        if not channel_metrics:
            logger.warning(f"  ⚠️ No metrics calculated (no analyzed videos)")
            channel_metrics = {
                'average_engagement_score': 0,
                'average_title_effectiveness': 0,
                'average_seo_score': 0,
                'total_views_analyzed': 0,
                'average_views_per_video': 0,
                'overall_engagement_rate': 0,
                'videos_analyzed': 0
            }
        
        # Generate viral insights
        logger.info(f"🚀 Generating viral insights and content recipes...")
        content_templates = viral_insights.extract_content_templates([v['video'] for v in analyzed_videos])
        viral_recipes = viral_insights.generate_viral_recipes(
            {'top_videos': analyzed_videos[:10]}, 
            patterns
        )
        
        results = {
            'channel': channel_info,
            'total_videos_found': len(videos),
            'videos_analyzed': len(analyzed_videos),
            'top_videos': analyzed_videos[:10],
            'content_patterns': patterns,
            'channel_metrics': channel_metrics,
            'viral_insights': {
                'content_templates': content_templates,
                'viral_recipes': viral_recipes
            }
        }
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            status="success",
            data=results,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Channel analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/video/analyze", response_model=AnalysisResponse)
async def analyze_video(request: VideoAnalysisRequest):
    """Analyze a single YouTube video in detail"""
    try:
        start_time = time.time()
        
        # Get video details
        video_details = youtube_extractor.get_video_details(request.video_url)
        if not video_details:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Analyze title and description
        title_analysis = content_analyzer.analyze_title(video_details.get('title', ''))
        desc_analysis = content_analyzer.analyze_description(video_details.get('description', ''))
        
        # Analyze sentiment
        title_sentiment = content_analyzer.analyze_sentiment(video_details.get('title', ''))
        desc_sentiment = content_analyzer.analyze_sentiment(video_details.get('description', '')[:500])
        
        # Get and analyze comments if requested
        comments_analysis = None
        if request.include_comments:
            comments = youtube_extractor.extract_comments(request.video_url, request.max_comments)
            if comments:
                comments_analysis = content_analyzer.analyze_comments_sentiment(comments)
        
        # Predict engagement
        engagement_prediction = content_analyzer.predict_engagement(video_details)
        
        # Get channel videos for comparison
        channel_url = f"https://youtube.com/channel/{video_details.get('channel_id')}"
        similar_videos = youtube_extractor.get_channel_videos(channel_url, 10)
        
        results = {
            'video': video_details,
            'title_analysis': title_analysis,
            'description_analysis': desc_analysis,
            'sentiment': {
                'title': title_sentiment,
                'description': desc_sentiment
            },
            'comments_analysis': comments_analysis,
            'engagement_prediction': engagement_prediction,
            'channel_context': {
                'other_videos': similar_videos,
                'channel_url': channel_url
            }
        }
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            status="success",
            data=results,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Video analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/patterns/detect", response_model=AnalysisResponse)
async def detect_patterns(video_urls: List[str]):
    """Detect patterns across multiple videos"""
    try:
        start_time = time.time()
        
        # Get details for all videos
        videos = []
        for url in video_urls[:20]:  # Limit to 20 videos
            details = youtube_extractor.get_video_details(url)
            if details:
                videos.append(details)
        
        if not videos:
            raise HTTPException(status_code=404, detail="No valid videos found")
        
        # Find patterns
        patterns = content_analyzer.find_content_patterns(videos)
        
        # Analyze each video
        analyses = []
        for video in videos:
            title_analysis = content_analyzer.analyze_title(video.get('title', ''))
            engagement = content_analyzer.predict_engagement(video)
            analyses.append({
                'title': video.get('title'),
                'views': video.get('view_count'),
                'title_patterns': title_analysis.get('patterns', []),
                'engagement_score': engagement.get('engagement_score', 0)
            })
        
        results = {
            'videos_analyzed': len(videos),
            'patterns': patterns,
            'individual_analyses': analyses
        }
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            status="success",
            data=results,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Pattern detection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channel/{channel_id}/videos")
async def get_channel_videos(channel_id: str, limit: int = 50):
    """Get videos from a specific channel"""
    try:
        channel_url = f"https://youtube.com/channel/{channel_id}"
        videos = youtube_extractor.get_channel_videos(channel_url, limit)
        
        return {
            "status": "success",
            "channel_id": channel_id,
            "video_count": len(videos),
            "videos": videos
        }
        
    except Exception as e:
        logger.error(f"Error getting channel videos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare/channels")
async def compare_channels(channel_urls: List[str]):
    """Compare multiple YouTube channels"""
    try:
        if len(channel_urls) < 2:
            raise HTTPException(status_code=400, detail="Provide at least 2 channel URLs")
        
        start_time = time.time()
        channels_data = []
        
        for url in channel_urls[:5]:  # Limit to 5 channels
            # Get channel info
            channel_info = youtube_extractor.get_channel_info(url)
            if channel_info:
                # Get sample videos
                videos = youtube_extractor.get_channel_videos(url, 20)
                
                # Analyze videos
                patterns = []
                if videos:
                    video_details = []
                    for video in videos[:10]:
                        if video.get('url'):
                            details = youtube_extractor.get_video_details(video['url'])
                            if details:
                                video_details.append(details)
                    
                    if video_details:
                        patterns = content_analyzer.find_content_patterns(video_details)
                
                channels_data.append({
                    'channel': channel_info,
                    'video_count': len(videos),
                    'patterns': patterns
                })
        
        # Compare channels
        comparison = _compare_channel_data(channels_data)
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            status="success",
            data={
                'channels': channels_data,
                'comparison': comparison
            },
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Channel comparison error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _calculate_channel_metrics(analyzed_videos: List[Dict]) -> Dict[str, Any]:
    """Calculate aggregate metrics for a channel"""
    if not analyzed_videos:
        return {}
    
    # Extract metrics
    engagement_scores = [v['engagement_prediction'].get('engagement_score', 0) for v in analyzed_videos]
    title_scores = [v['title_analysis'].get('effectiveness_score', 0) for v in analyzed_videos]
    seo_scores = [v['description_analysis'].get('seo_score', 0) for v in analyzed_videos]
    
    # Views and engagement (handle None values)
    total_views = sum(v['video'].get('view_count') or 0 for v in analyzed_videos)
    total_likes = sum(v['video'].get('like_count') or 0 for v in analyzed_videos)
    total_comments = sum(v['video'].get('comment_count') or 0 for v in analyzed_videos)
    
    # Calculate averages
    import numpy as np
    
    return {
        'average_engagement_score': float(np.mean(engagement_scores)) if engagement_scores else 0,
        'average_title_effectiveness': float(np.mean(title_scores)) if title_scores else 0,
        'average_seo_score': float(np.mean(seo_scores)) if seo_scores else 0,
        'total_views_analyzed': total_views,
        'average_views_per_video': total_views // len(analyzed_videos) if analyzed_videos else 0,
        'overall_engagement_rate': (total_likes + total_comments) / total_views if total_views > 0 else 0,
        'videos_analyzed': len(analyzed_videos)
    }

def _compare_channel_data(channels_data: List[Dict]) -> Dict[str, Any]:
    """Compare metrics across multiple channels"""
    if len(channels_data) < 2:
        return {}
    
    comparison = {
        'subscriber_comparison': {},
        'content_style_comparison': {},
        'pattern_comparison': {}
    }
    
    # Compare subscribers
    for i, channel_data in enumerate(channels_data):
        channel_name = channel_data['channel'].get('channel_name', f'Channel {i+1}')
        comparison['subscriber_comparison'][channel_name] = channel_data['channel'].get('subscriber_count', 0)
    
    # Compare content patterns
    for i, channel_data in enumerate(channels_data):
        channel_name = channel_data['channel'].get('channel_name', f'Channel {i+1}')
        if channel_data.get('patterns'):
            comparison['pattern_comparison'][channel_name] = channel_data['patterns'].get('common_patterns', {})
    
    return comparison

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)