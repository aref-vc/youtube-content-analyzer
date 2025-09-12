import re
import logging
from typing import Dict, Any, List, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Disable sentence transformers temporarily due to PyTorch version issue
# from sentence_transformers import SentenceTransformer
import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
import textstat
from collections import Counter
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class ContentAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        # Disabled temporarily due to PyTorch version issue
        # self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sentence_model = None
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Pattern definitions
        self.title_patterns = {
            'question': r'^\b(how|what|why|when|where|who|which|can|should|will|does|is)\b',
            'number_list': r'\d+\s*(tips|ways|reasons|steps|things|secrets|hacks|tricks)',
            'ultimate_guide': r'(ultimate|complete|definitive|comprehensive)\s+guide',
            'beginner': r'(beginner|newbie|starter|basic|101|intro)',
            'advanced': r'(advanced|expert|pro|master|professional)',
            'tutorial': r'(tutorial|how\s+to|step\s+by\s+step|guide)',
            'review': r'(review|unboxing|first\s+look|hands\s+on|tested)',
            'comparison': r'(vs\.|versus|compared|comparison|better)',
            'emotional': r'(amazing|incredible|shocking|unbelievable|insane|crazy|mind\s+blowing)',
            'urgency': r'(now|today|quick|fast|instant|immediately)',
        }
        
        self.power_words = [
            'free', 'new', 'proven', 'easy', 'guaranteed', 'secret', 'exclusive',
            'limited', 'breakthrough', 'revolutionary', 'transform', 'discover',
            'unlock', 'master', 'essential', 'powerful', 'ultimate', 'best'
        ]
        
    def analyze_title(self, title: str) -> Dict[str, Any]:
        """Analyze video title for patterns and effectiveness"""
        try:
            title_lower = title.lower()
            
            # Detect patterns
            patterns_found = []
            for pattern_name, pattern_regex in self.title_patterns.items():
                if re.search(pattern_regex, title_lower):
                    patterns_found.append(pattern_name)
            
            # Count power words
            power_word_count = sum(1 for word in self.power_words if word in title_lower)
            
            # Calculate metrics
            word_count = len(title.split())
            char_count = len(title)
            has_emoji = bool(re.search(r'[\U0001F300-\U0001F9FF]', title))
            has_caps = any(word.isupper() for word in title.split() if len(word) > 1)
            
            # Readability
            readability = textstat.flesch_reading_ease(title)
            
            # Title effectiveness score (0-100)
            effectiveness_score = self._calculate_title_effectiveness(
                patterns_found, power_word_count, word_count, char_count, has_emoji
            )
            
            return {
                'patterns': patterns_found,
                'power_word_count': power_word_count,
                'word_count': word_count,
                'char_count': char_count,
                'has_emoji': has_emoji,
                'has_caps': has_caps,
                'readability': readability,
                'effectiveness_score': effectiveness_score,
                'suggestions': self._get_title_suggestions(effectiveness_score, patterns_found)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing title: {e}")
            return {}
    
    def analyze_description(self, description: str) -> Dict[str, Any]:
        """Analyze video description for SEO and engagement"""
        try:
            if not description:
                return {'error': 'No description provided'}
            
            desc_lower = description.lower()
            
            # Extract links
            links = re.findall(r'https?://[^\s]+', description)
            
            # Extract hashtags
            hashtags = re.findall(r'#\w+', description)
            
            # Check for timestamps
            has_timestamps = bool(re.search(r'\d{1,2}:\d{2}', description))
            
            # Check for CTAs
            cta_patterns = [
                'subscribe', 'like', 'comment', 'share', 'follow',
                'click', 'download', 'join', 'sign up', 'check out'
            ]
            ctas_found = [cta for cta in cta_patterns if cta in desc_lower]
            
            # Word and line count
            word_count = len(description.split())
            line_count = len(description.split('\n'))
            
            # First 125 chars (shown in search)
            preview_text = description[:125]
            
            # Keyword density
            words = re.findall(r'\w+', desc_lower)
            word_freq = Counter(words)
            top_keywords = word_freq.most_common(10)
            
            # Structure analysis
            has_sections = bool(re.search(r'\n\n|\n-|\n\d+\.', description))
            
            return {
                'word_count': word_count,
                'line_count': line_count,
                'link_count': len(links),
                'hashtag_count': len(hashtags),
                'has_timestamps': has_timestamps,
                'ctas_found': ctas_found,
                'preview_text': preview_text,
                'top_keywords': top_keywords,
                'has_sections': has_sections,
                'seo_score': self._calculate_seo_score(
                    word_count, len(hashtags), has_timestamps, len(ctas_found)
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing description: {e}")
            return {}
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using VADER"""
        try:
            scores = self.sentiment_analyzer.polarity_scores(text)
            return {
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu'],
                'compound': scores['compound']
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {}
    
    def analyze_comments_sentiment(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment across multiple comments"""
        try:
            if not comments:
                return {'error': 'No comments provided'}
            
            sentiments = []
            for comment in comments:
                if comment.get('text'):
                    sentiment = self.analyze_sentiment(comment['text'])
                    sentiments.append(sentiment)
            
            if not sentiments:
                return {'error': 'No valid comments for analysis'}
            
            # Calculate average sentiment
            avg_sentiment = {
                'positive': np.mean([s['positive'] for s in sentiments]),
                'negative': np.mean([s['negative'] for s in sentiments]),
                'neutral': np.mean([s['neutral'] for s in sentiments]),
                'compound': np.mean([s['compound'] for s in sentiments])
            }
            
            # Sentiment distribution
            positive_count = sum(1 for s in sentiments if s['compound'] > 0.05)
            negative_count = sum(1 for s in sentiments if s['compound'] < -0.05)
            neutral_count = len(sentiments) - positive_count - negative_count
            
            return {
                'average_sentiment': avg_sentiment,
                'sentiment_distribution': {
                    'positive': positive_count,
                    'negative': negative_count,
                    'neutral': neutral_count
                },
                'total_comments_analyzed': len(sentiments),
                'overall_tone': self._get_overall_tone(avg_sentiment['compound'])
            }
            
        except Exception as e:
            logger.error(f"Error analyzing comments sentiment: {e}")
            return {}
    
    def create_semantic_embedding(self, text: str) -> np.ndarray:
        """Create semantic embedding for text"""
        try:
            if self.sentence_model:
                return self.sentence_model.encode(text)
            else:
                # Return a simple hash-based embedding as fallback
                return np.array([hash(text) % 1000 / 1000.0])
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            return np.array([])
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            # Simple text similarity based on common words as fallback
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union) if union else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_content_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find patterns across multiple videos"""
        try:
            if not videos:
                return {'error': 'No videos provided'}
            
            # Collect all titles and descriptions
            titles = [v.get('title', '') for v in videos if v.get('title')]
            descriptions = [v.get('description', '') for v in videos if v.get('description')]
            
            # Common title patterns
            all_patterns = []
            for title in titles:
                analysis = self.analyze_title(title)
                all_patterns.extend(analysis.get('patterns', []))
            
            pattern_frequency = Counter(all_patterns)
            
            # Average metrics
            title_lengths = [len(t.split()) for t in titles]
            avg_title_length = np.mean(title_lengths) if title_lengths else 0
            
            # Find best performing patterns
            performance_patterns = self._analyze_performance_patterns(videos)
            
            # Topic clustering
            topics = self._extract_topics(titles + descriptions)
            
            return {
                'common_patterns': dict(pattern_frequency.most_common(5)),
                'average_title_length': avg_title_length,
                'performance_patterns': performance_patterns,
                'main_topics': topics[:10],
                'content_consistency': self._calculate_content_consistency(titles)
            }
            
        except Exception as e:
            logger.error(f"Error finding patterns: {e}")
            return {}
    
    def predict_engagement(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict engagement based on content analysis"""
        try:
            score = 0
            factors = []
            
            # Title analysis contribution
            title_analysis = self.analyze_title(video_data.get('title', ''))
            title_score = title_analysis.get('effectiveness_score', 0)
            score += title_score * 0.3
            if title_score > 70:
                factors.append('Strong title')
            
            # Description analysis contribution
            desc_analysis = self.analyze_description(video_data.get('description', ''))
            seo_score = desc_analysis.get('seo_score', 0)
            score += seo_score * 0.2
            if seo_score > 70:
                factors.append('Good SEO optimization')
            
            # View to like ratio (if available)
            if video_data.get('view_count') and video_data.get('like_count'):
                like_ratio = video_data['like_count'] / video_data['view_count']
                if like_ratio > 0.04:  # 4% is good
                    score += 20
                    factors.append('High like ratio')
            
            # Comment engagement (if available)
            if video_data.get('view_count') and video_data.get('comment_count'):
                comment_ratio = video_data['comment_count'] / video_data['view_count']
                if comment_ratio > 0.005:  # 0.5% is good
                    score += 15
                    factors.append('High comment engagement')
            
            # Tags and hashtags
            if video_data.get('tags'):
                tag_count = len(video_data['tags'])
                if 5 <= tag_count <= 15:
                    score += 10
                    factors.append('Optimal tag usage')
            
            # Normalize score to 0-100
            score = min(100, max(0, score))
            
            # Determine performance tier
            if score >= 80:
                tier = 'Excellent'
            elif score >= 60:
                tier = 'Good'
            elif score >= 40:
                tier = 'Average'
            else:
                tier = 'Needs Improvement'
            
            return {
                'engagement_score': score,
                'performance_tier': tier,
                'positive_factors': factors,
                'recommendations': self._get_engagement_recommendations(score, title_analysis, desc_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error predicting engagement: {e}")
            return {}
    
    def _calculate_title_effectiveness(self, patterns: List[str], power_words: int, 
                                      word_count: int, char_count: int, has_emoji: bool) -> float:
        """Calculate title effectiveness score"""
        score = 50  # Base score
        
        # Pattern bonuses
        if 'question' in patterns:
            score += 10
        if 'number_list' in patterns:
            score += 15
        if 'tutorial' in patterns:
            score += 10
        if 'emotional' in patterns:
            score += 5
        
        # Power word bonus
        score += min(15, power_words * 5)
        
        # Length optimization (8-12 words is optimal)
        if 8 <= word_count <= 12:
            score += 10
        elif word_count < 5 or word_count > 15:
            score -= 10
        
        # Character count (50-60 chars is optimal for search)
        if 50 <= char_count <= 60:
            score += 5
        
        # Emoji bonus (but not too many)
        if has_emoji:
            score += 3
        
        return min(100, max(0, score))
    
    def _calculate_seo_score(self, word_count: int, hashtag_count: int, 
                            has_timestamps: bool, cta_count: int) -> float:
        """Calculate SEO score for description"""
        score = 40  # Base score
        
        # Word count (200-300 is optimal)
        if 200 <= word_count <= 300:
            score += 20
        elif 100 <= word_count < 200:
            score += 10
        elif word_count > 500:
            score -= 5
        
        # Hashtags (3-5 is optimal)
        if 3 <= hashtag_count <= 5:
            score += 15
        elif 1 <= hashtag_count <= 10:
            score += 5
        
        # Timestamps bonus
        if has_timestamps:
            score += 15
        
        # CTA bonus
        if 1 <= cta_count <= 3:
            score += 10
        
        return min(100, max(0, score))
    
    def _get_overall_tone(self, compound_score: float) -> str:
        """Determine overall tone from compound sentiment score"""
        if compound_score >= 0.5:
            return 'Very Positive'
        elif compound_score >= 0.1:
            return 'Positive'
        elif compound_score <= -0.5:
            return 'Very Negative'
        elif compound_score <= -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    
    def _analyze_performance_patterns(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze which patterns correlate with better performance"""
        patterns_performance = {}
        
        for video in videos:
            if video.get('view_count'):
                title_analysis = self.analyze_title(video.get('title', ''))
                for pattern in title_analysis.get('patterns', []):
                    if pattern not in patterns_performance:
                        patterns_performance[pattern] = []
                    patterns_performance[pattern].append(video['view_count'])
        
        # Calculate average performance per pattern
        results = []
        for pattern, views in patterns_performance.items():
            if views:
                results.append({
                    'pattern': pattern,
                    'avg_views': int(np.mean(views)),
                    'video_count': len(views)
                })
        
        # Sort by average views
        results.sort(key=lambda x: x['avg_views'], reverse=True)
        return results[:5]
    
    def _extract_topics(self, texts: List[str]) -> List[Tuple[str, int]]:
        """Extract main topics from texts"""
        all_words = []
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                     'could', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i',
                     'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when',
                     'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
                     'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than',
                     'too', 'very', 'just', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        for text in texts:
            words = re.findall(r'\b[a-z]+\b', text.lower())
            filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
            all_words.extend(filtered_words)
        
        word_freq = Counter(all_words)
        return word_freq.most_common(20)
    
    def _calculate_content_consistency(self, titles: List[str]) -> float:
        """Calculate how consistent the content theme is"""
        if len(titles) < 2:
            return 100.0
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(titles)):
            for j in range(i + 1, len(titles)):
                sim = self.calculate_semantic_similarity(titles[i], titles[j])
                similarities.append(sim)
        
        if similarities:
            return float(np.mean(similarities) * 100)
        return 0.0
    
    def _get_title_suggestions(self, effectiveness_score: float, patterns: List[str]) -> List[str]:
        """Get suggestions for improving title"""
        suggestions = []
        
        if effectiveness_score < 60:
            if 'question' not in patterns:
                suggestions.append("Consider starting with a question to increase engagement")
            if 'number_list' not in patterns:
                suggestions.append("Try using numbered lists (e.g., '5 Tips for...')")
            suggestions.append("Add power words like 'ultimate', 'essential', or 'proven'")
        
        if effectiveness_score < 40:
            suggestions.append("Title may be too short or too long - aim for 8-12 words")
            suggestions.append("Consider adding emotional triggers or urgency")
        
        return suggestions
    
    def _get_engagement_recommendations(self, score: float, title_analysis: Dict, 
                                       desc_analysis: Dict) -> List[str]:
        """Get recommendations for improving engagement"""
        recommendations = []
        
        if score < 70:
            if title_analysis.get('effectiveness_score', 0) < 60:
                recommendations.append("Improve title with questions or numbered lists")
            
            if desc_analysis.get('seo_score', 0) < 60:
                recommendations.append("Optimize description with timestamps and relevant hashtags")
            
            if not desc_analysis.get('has_timestamps'):
                recommendations.append("Add timestamps to improve viewer retention")
            
            if desc_analysis.get('word_count', 0) < 100:
                recommendations.append("Expand description to 200-300 words for better SEO")
        
        return recommendations