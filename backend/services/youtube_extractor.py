import yt_dlp
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class YouTubeExtractor:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'ignoreerrors': True,
            'no_color': True,
            'no_call_home': True,
            'skip_download': True,
        }
        self.executor = ThreadPoolExecutor(max_workers=3)
        
    def search_videos(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Search for videos on YouTube by query"""
        try:
            search_opts = {
                **self.ydl_opts,
                'extract_flat': True,
                'playlistend': max_results,
            }
            
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                search_url = f"ytsearch{max_results}:{query}"
                result = ydl.extract_info(search_url, download=False)
                
                videos = []
                if result and 'entries' in result:
                    for entry in result['entries']:
                        if entry:
                            videos.append({
                                'video_id': entry.get('id'),
                                'title': entry.get('title'),
                                'url': f"https://youtube.com/watch?v={entry.get('id')}",
                                'channel': entry.get('channel'),
                                'channel_id': entry.get('channel_id'),
                                'duration': entry.get('duration'),
                                'view_count': entry.get('view_count'),
                            })
                
                return videos
                
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            return []
    
    def get_channel_info(self, channel_url: str) -> Optional[Dict[str, Any]]:
        """Get detailed channel information - simplified approach"""
        logger.info(f"🔄 Starting channel info extraction for: {channel_url}")
        
        # Extract channel ID from URL
        channel_id = None
        if '/channel/' in channel_url:
            channel_id = channel_url.split('/channel/')[-1].split('/')[0].split('?')[0]
        elif '/@' in channel_url:
            # Handle @ URLs differently
            channel_handle = channel_url.split('/@')[-1].split('/')[0].split('?')[0]
            channel_url = f"https://youtube.com/@{channel_handle}"
        
        logger.info(f"📌 Channel ID/Handle extracted: {channel_id or 'using full URL'}")
        
        # Use simpler extraction for channel info
        try:
            opts = {
                **self.ydl_opts,
                'extract_flat': True,  # Don't extract all videos, just channel info
                'playlistend': 1,  # Only get first video for channel info
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Try to get channel videos page which is faster
                test_url = f"{channel_url}/videos" if '/videos' not in channel_url else channel_url
                logger.info(f"🔄 Attempting fast extraction from: {test_url}")
                
                try:
                    result = ydl.extract_info(test_url, download=False)
                    
                    if result:
                        # Extract channel info from the playlist result
                        channel_data = {
                            'channel_id': channel_id or result.get('channel_id') or result.get('id'),
                            'channel_name': result.get('channel') or result.get('uploader') or result.get('title', 'Unknown Channel'),
                            'channel_url': channel_url,
                            'subscriber_count': self._parse_subscriber_count(result.get('channel_follower_count')),
                            'description': result.get('description', ''),
                            'video_count': result.get('playlist_count') or len(result.get('entries', [])),
                        }
                        logger.info(f"✅ Channel data extracted: {channel_data['channel_name']}")
                        return channel_data
                except Exception as e:
                    logger.warning(f"⚠️ Fast extraction failed: {e}, trying fallback...")
                
                # Fallback: Create basic channel info
                return {
                    'channel_id': channel_id or channel_url.split('/')[-1],
                    'channel_name': 'Channel',
                    'channel_url': channel_url,
                    'subscriber_count': None,
                    'description': '',
                    'video_count': 0,
                }
                    
        except Exception as e:
            logger.error(f"❌ Error getting channel info: {e}")
            # Return basic info even on error
            return {
                'channel_id': channel_id or 'unknown',
                'channel_name': 'Unknown Channel',
                'channel_url': channel_url,
                'subscriber_count': None,
                'description': '',
                'video_count': 0,
            }
    
    def get_channel_videos(self, channel_url: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get videos from a channel"""
        logger.info(f"🔄 Getting videos for channel: {channel_url} (limit: {limit})")
        try:
            opts = {
                **self.ydl_opts,
                'extract_flat': True,
                'playlistend': limit,
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Try the videos tab directly
                urls_to_try = [
                    f"{channel_url}/videos" if '/videos' not in channel_url else channel_url,
                ]
                
                for url in urls_to_try:
                    try:
                        logger.info(f"🔄 Trying URL format: {url}")
                        result = ydl.extract_info(url, download=False)
                        if result and 'entries' in result:
                            videos = []
                            for i, entry in enumerate(result['entries'][:limit]):
                                if entry:
                                    # Debug logging
                                    if i == 0:
                                        logger.info(f"    🔍 First entry keys: {list(entry.keys())[:10]}")
                                        logger.info(f"    🔍 Entry ID: {entry.get('id')}, URL: {entry.get('url')}")
                                    
                                    # Use the correct field from the entry
                                    video_id = entry.get('id')
                                    video_url = entry.get('url')
                                    
                                    # If we have a URL directly, use it; otherwise construct it
                                    if video_url:
                                        final_url = video_url
                                    elif video_id:
                                        final_url = f"https://youtube.com/watch?v={video_id}"
                                    else:
                                        continue
                                    
                                    # Skip if this is not a valid video (e.g., channel tabs)
                                    title = entry.get('title', '')
                                    if title in ['Videos', 'Live', 'Shorts', 'Playlists', 'Community']:
                                        logger.info(f"    ⏭️ Skipping channel tab: {title}")
                                        continue
                                    
                                    videos.append({
                                        'video_id': video_id,
                                        'title': title or 'Unknown',
                                        'url': final_url,
                                        'duration': entry.get('duration'),
                                        'view_count': entry.get('view_count'),
                                    })
                                    logger.info(f"    📹 Added video: {title[:50]}")
                            
                            if videos:
                                logger.info(f"✅ Found {len(videos)} valid videos for channel")
                                return videos
                    except Exception as e:
                        logger.warning(f"⚠️ Failed with URL {url}: {str(e)}")
                        continue
                
                logger.warning(f"⚠️ No videos found for channel {channel_url}")        
                return []
                
        except Exception as e:
            logger.error(f"❌ Error getting channel videos: {e}")
            return []
    
    def get_video_details(self, video_url: str) -> Optional[Dict[str, Any]]:
        """Get detailed video information"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                result = ydl.extract_info(video_url, download=False)
                
                if result:
                    upload_date = None
                    if result.get('upload_date'):
                        try:
                            upload_date = datetime.strptime(result['upload_date'], '%Y%m%d')
                        except:
                            pass
                    
                    return {
                        'video_id': result.get('id'),
                        'title': result.get('title'),
                        'description': result.get('description'),
                        'channel_id': result.get('channel_id'),
                        'channel_name': result.get('channel') or result.get('uploader'),
                        'duration': result.get('duration'),
                        'view_count': result.get('view_count'),
                        'like_count': result.get('like_count'),
                        'comment_count': result.get('comment_count'),
                        'upload_date': upload_date,
                        'tags': result.get('tags', []),
                        'categories': result.get('categories', []),
                        'thumbnail_url': result.get('thumbnail'),
                        'url': video_url,
                        'age_limit': result.get('age_limit'),
                        'live_status': result.get('live_status'),
                        'availability': result.get('availability'),
                    }
                    
        except Exception as e:
            logger.error(f"Error getting video details: {e}")
            return None
    
    def extract_comments(self, video_url: str, max_comments: int = 100) -> List[Dict[str, Any]]:
        """Extract comments from a video"""
        try:
            opts = {
                **self.ydl_opts,
                'getcomments': True,
                'extractor_args': {
                    'youtube': {
                        'max_comments': [str(max_comments)],
                        'comment_sort': ['top'],
                    }
                }
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                result = ydl.extract_info(video_url, download=False)
                
                comments = []
                if result and 'comments' in result:
                    for comment in result['comments'][:max_comments]:
                        comments.append({
                            'text': comment.get('text'),
                            'author': comment.get('author'),
                            'likes': comment.get('like_count', 0),
                            'timestamp': comment.get('timestamp'),
                            'is_favorited': comment.get('is_favorited', False),
                        })
                
                return comments
                
        except Exception as e:
            logger.error(f"Error extracting comments: {e}")
            return []
    
    def search_channels(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for channels by query"""
        try:
            # Search for channels by adding "channel" to query
            channel_search = f"{query} channel"
            videos = self.search_videos(channel_search, max_results * 3)
            
            # Extract unique channels
            channels_dict = {}
            for video in videos:
                if video.get('channel_id') and video['channel_id'] not in channels_dict:
                    channels_dict[video['channel_id']] = {
                        'channel_id': video['channel_id'],
                        'channel_name': video.get('channel'),
                        'channel_url': f"https://youtube.com/channel/{video['channel_id']}",
                    }
                    
                if len(channels_dict) >= max_results:
                    break
            
            return list(channels_dict.values())
            
        except Exception as e:
            logger.error(f"Error searching channels: {e}")
            return []
    
    def get_topic_channels(self, topic: str, max_channels: int = 10) -> List[Dict[str, Any]]:
        """Get top channels for a specific topic"""
        try:
            # Search for videos on the topic
            videos = self.search_videos(topic, max_channels * 5)
            
            # Count videos per channel
            channel_counts = {}
            channel_info = {}
            
            for video in videos:
                channel_id = video.get('channel_id')
                if channel_id:
                    if channel_id not in channel_counts:
                        channel_counts[channel_id] = 0
                        channel_info[channel_id] = {
                            'channel_id': channel_id,
                            'channel_name': video.get('channel'),
                            'channel_url': f"https://youtube.com/channel/{channel_id}",
                        }
                    channel_counts[channel_id] += 1
            
            # Sort channels by video count (popularity indicator)
            sorted_channels = sorted(
                channel_info.items(),
                key=lambda x: channel_counts[x[0]],
                reverse=True
            )
            
            return [channel[1] for channel in sorted_channels[:max_channels]]
            
        except Exception as e:
            logger.error(f"Error getting topic channels: {e}")
            return []
    
    def _parse_subscriber_count(self, count_str: Any) -> Optional[int]:
        """Parse subscriber count from various formats"""
        if isinstance(count_str, int):
            return count_str
        if isinstance(count_str, str):
            # Remove non-numeric characters except for K, M, B
            count_str = count_str.upper().replace(',', '').strip()
            multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
            
            for suffix, multiplier in multipliers.items():
                if suffix in count_str:
                    try:
                        number = float(count_str.replace(suffix, '').strip())
                        return int(number * multiplier)
                    except:
                        pass
            
            # Try to parse as regular number
            try:
                return int(re.sub(r'[^0-9]', '', count_str))
            except:
                pass
        
        return None
    
    async def async_get_multiple_videos(self, video_urls: List[str]) -> List[Dict[str, Any]]:
        """Asynchronously get details for multiple videos"""
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, self.get_video_details, url)
            for url in video_urls
        ]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]