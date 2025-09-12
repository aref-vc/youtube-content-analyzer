import re
import logging
from typing import Dict, Any, List, Tuple
from collections import Counter
import numpy as np

logger = logging.getLogger(__name__)

class ViralInsightsAnalyzer:
    def __init__(self):
        # Hook patterns that grab attention
        self.hook_patterns = {
            'curiosity_gap': {
                'patterns': [
                    r'why\s+\w+\s+(is|are|was|were)',
                    r'the\s+(secret|truth|reason)',
                    r'what\s+(nobody|everyone|they)',
                    r'you\s+(won\'t|wouldn\'t)\s+believe',
                    r'this\s+is\s+why',
                    r'the\s+real\s+reason'
                ],
                'score': 90
            },
            'challenge': {
                'patterns': [
                    r'i\s+(tried|tested|spent)',
                    r'(24|48|72)\s+hours',
                    r'for\s+\d+\s+days',
                    r'challenge\s+accepted',
                    r'can\s+you',
                    r'impossible'
                ],
                'score': 85
            },
            'revelation': {
                'patterns': [
                    r'(exposed|revealed|uncovered)',
                    r'the\s+dark\s+(side|truth)',
                    r'what\s+they\s+don\'t',
                    r'finally\s+revealed',
                    r'shocking\s+truth'
                ],
                'score': 88
            },
            'transformation': {
                'patterns': [
                    r'how\s+to',
                    r'from\s+.+\s+to\s+',
                    r'transform',
                    r'changed?\s+my\s+life',
                    r'before\s+and\s+after',
                    r'in\s+just\s+\d+'
                ],
                'score': 82
            },
            'controversy': {
                'patterns': [
                    r'(unpopular|controversial)\s+opinion',
                    r'is\s+(dead|dying|over)',
                    r'why\s+i\s+(quit|stopped|left)',
                    r'the\s+problem\s+with',
                    r'we\s+need\s+to\s+talk'
                ],
                'score': 87
            },
            'fomo': {
                'patterns': [
                    r'(everyone|nobody)\s+is',
                    r'you\'re\s+(missing|doing)\s+.+\s+wrong',
                    r'before\s+it\'s\s+too\s+late',
                    r'last\s+chance',
                    r'don\'t\s+miss',
                    r'right\s+now'
                ],
                'score': 83
            }
        }
        
        # Emotional triggers
        self.emotional_triggers = {
            'excitement': ['amazing', 'incredible', 'unbelievable', 'mind-blowing', 'insane', 'crazy', 'epic'],
            'fear': ['scary', 'terrifying', 'dangerous', 'warning', 'alert', 'risk', 'threat'],
            'anger': ['angry', 'furious', 'outraged', 'disgusting', 'hate', 'worst'],
            'surprise': ['shocking', 'unexpected', 'suddenly', 'plot twist', 'never expected'],
            'curiosity': ['secret', 'hidden', 'unknown', 'mystery', 'revealed', 'discover'],
            'urgency': ['now', 'today', 'immediately', 'quick', 'fast', 'limited', 'urgent']
        }
        
        # Successful title formulas
        self.title_formulas = [
            {'template': '[Number] [Thing] That [Outcome]', 'example': '5 Habits That Changed My Life'},
            {'template': 'Why [Subject] [Verb] [Object]', 'example': 'Why Successful People Wake Up Early'},
            {'template': 'How [Subject] [Achievement] in [Timeframe]', 'example': 'How I Learned Spanish in 30 Days'},
            {'template': 'The [Adjective] [Noun] [Qualifier]', 'example': 'The Hidden Cost of Success'},
            {'template': '[Doing This] for [Timeframe] [Result]', 'example': 'Reading for 30 Minutes Daily Changed Everything'},
            {'template': 'I [Action] and [Result]', 'example': 'I Quit Social Media and This Happened'},
            {'template': '[Number] [Mistakes] [Target Audience] Make', 'example': '7 Mistakes Beginners Make'},
            {'template': 'Stop [Action] Start [Action]', 'example': 'Stop Scrolling Start Creating'},
            {'template': 'The Truth About [Topic]', 'example': 'The Truth About Passive Income'},
            {'template': '[Celebrity/Brand] [Action] [Surprising Element]', 'example': 'Apple Engineer Reveals Secret Features'}
        ]
        
    def analyze_hooks(self, title: str) -> Dict[str, Any]:
        """Analyze title for hook effectiveness"""
        title_lower = title.lower()
        hooks_found = []
        total_score = 0
        
        # Check for each hook type
        for hook_type, config in self.hook_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, title_lower):
                    hooks_found.append({
                        'type': hook_type,
                        'score': config['score'],
                        'pattern_matched': pattern
                    })
                    total_score += config['score']
                    break  # Only count each hook type once
        
        # Check for curiosity elements
        has_question = '?' in title
        has_ellipsis = '...' in title
        has_numbers = bool(re.search(r'\d+', title))
        
        curiosity_score = 0
        curiosity_elements = []
        
        if has_question:
            curiosity_score += 20
            curiosity_elements.append('question')
        if has_ellipsis:
            curiosity_score += 15
            curiosity_elements.append('incomplete_thought')
        if has_numbers:
            curiosity_score += 10
            curiosity_elements.append('specific_number')
            
        # Analyze emotional triggers
        emotions_triggered = []
        for emotion, words in self.emotional_triggers.items():
            for word in words:
                if word in title_lower:
                    emotions_triggered.append({
                        'emotion': emotion,
                        'trigger_word': word
                    })
        
        # Calculate overall hook effectiveness
        hook_effectiveness = min(100, (total_score / len(self.hook_patterns) if hooks_found else 0) + curiosity_score)
        
        return {
            'hooks_found': hooks_found,
            'hook_effectiveness_score': hook_effectiveness,
            'curiosity_elements': curiosity_elements,
            'curiosity_score': curiosity_score,
            'emotions_triggered': emotions_triggered,
            'has_power_hook': hook_effectiveness > 70,
            'recommendations': self._get_hook_recommendations(hooks_found, curiosity_score)
        }
    
    def analyze_title_performance_factors(self, title: str, view_count: int = None) -> Dict[str, Any]:
        """Analyze title characteristics that correlate with performance"""
        
        # Title length analysis
        word_count = len(title.split())
        char_count = len(title)
        
        # Optimal ranges based on YouTube best practices
        optimal_word_range = (8, 12)
        optimal_char_range = (50, 60)
        
        word_score = 100 if optimal_word_range[0] <= word_count <= optimal_word_range[1] else max(0, 100 - abs(word_count - 10) * 10)
        char_score = 100 if optimal_char_range[0] <= char_count <= optimal_char_range[1] else max(0, 100 - abs(char_count - 55) * 2)
        
        # Capitalization analysis
        title_words = title.split()
        caps_patterns = {
            'all_caps': all(word.isupper() for word in title_words if len(word) > 2),
            'title_case': title.istitle(),
            'first_word_caps': title_words[0].isupper() if title_words else False,
            'mixed_caps': any(word.isupper() for word in title_words) and not all(word.isupper() for word in title_words)
        }
        
        # Number psychology
        numbers_found = re.findall(r'\d+', title)
        has_odd_number = any(int(n) % 2 == 1 for n in numbers_found if n.isdigit())
        has_list_number = any(int(n) <= 10 for n in numbers_found if n.isdigit())
        
        number_insights = {
            'has_numbers': bool(numbers_found),
            'numbers': numbers_found,
            'uses_odd_numbers': has_odd_number,  # Odd numbers often perform better
            'uses_list_format': has_list_number,
            'number_placement': 'beginning' if numbers_found and title.strip().startswith(numbers_found[0]) else 'middle/end' if numbers_found else None
        }
        
        # Punctuation impact
        punctuation_analysis = {
            'has_question_mark': '?' in title,
            'has_exclamation': '!' in title,
            'has_colon': ':' in title,
            'has_dash': '-' in title or '—' in title,
            'has_parentheses': '(' in title or '[' in title,
            'has_quotes': '"' in title or "'" in title
        }
        
        # Calculate overall title optimization score
        optimization_score = (word_score + char_score) / 2
        
        if number_insights['uses_odd_numbers']:
            optimization_score += 5
        if number_insights['number_placement'] == 'beginning':
            optimization_score += 5
        if punctuation_analysis['has_question_mark']:
            optimization_score += 3
        
        optimization_score = min(100, optimization_score)
        
        return {
            'length_analysis': {
                'word_count': word_count,
                'char_count': char_count,
                'word_score': word_score,
                'char_score': char_score,
                'optimal_word_range': optimal_word_range,
                'optimal_char_range': optimal_char_range
            },
            'capitalization': caps_patterns,
            'number_psychology': number_insights,
            'punctuation_impact': punctuation_analysis,
            'optimization_score': optimization_score,
            'recommendations': self._get_title_optimization_recommendations(word_count, char_count, caps_patterns, number_insights)
        }
    
    def extract_content_templates(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract reusable content templates and patterns from successful videos"""
        
        if not videos:
            return {'error': 'No videos provided for template extraction'}
        
        # Sort videos by performance (views * engagement rate)
        sorted_videos = sorted(videos, 
                              key=lambda v: v.get('view_count', 0) * 
                              (v.get('like_count', 0) / v.get('view_count', 1) if v.get('view_count', 0) > 0 else 0),
                              reverse=True)
        
        # Extract patterns from top performers (top 20%)
        top_performer_count = max(1, len(sorted_videos) // 5)
        top_videos = sorted_videos[:top_performer_count]
        
        # Extract title patterns
        title_patterns = []
        for video in top_videos:
            title = video.get('title', '')
            
            # Try to match against known formulas
            matched_formula = None
            for formula in self.title_formulas:
                # Simplified pattern matching - in production, use more sophisticated NLP
                if self._matches_formula_pattern(title, formula['template']):
                    matched_formula = formula
                    break
            
            # Extract components
            components = {
                'title': title,
                'views': video.get('view_count', 0),
                'likes': video.get('like_count', 0),
                'formula_matched': matched_formula,
                'has_number': bool(re.search(r'\d+', title)),
                'starts_with_number': bool(re.match(r'^\d+', title.strip())),
                'has_question': '?' in title,
                'word_count': len(title.split())
            }
            title_patterns.append(components)
        
        # Find common elements
        common_starts = self._find_common_patterns([v['title'][:20] for v in top_videos])
        common_words = self._find_common_words([v['title'] for v in top_videos])
        
        # Extract series patterns
        series_indicators = ['part', 'episode', 'ep', '#', 'vol', 'chapter']
        series_patterns = []
        for video in videos:
            title_lower = video.get('title', '').lower()
            for indicator in series_indicators:
                if indicator in title_lower:
                    series_patterns.append({
                        'title': video.get('title'),
                        'indicator': indicator,
                        'views': video.get('view_count', 0)
                    })
                    break
        
        # Generate template library
        template_library = {
            'top_performing_patterns': title_patterns,
            'common_opening_phrases': common_starts,
            'power_words': [word for word, count in common_words if count > 1],
            'series_opportunities': series_patterns[:5],
            'recommended_formulas': self._get_recommended_formulas(title_patterns),
            'average_top_performer_metrics': {
                'avg_word_count': np.mean([p['word_count'] for p in title_patterns]) if title_patterns else 0,
                'percent_with_numbers': sum(1 for p in title_patterns if p['has_number']) / len(title_patterns) * 100 if title_patterns else 0,
                'percent_questions': sum(1 for p in title_patterns if p['has_question']) / len(title_patterns) * 100 if title_patterns else 0
            }
        }
        
        return template_library
    
    def generate_viral_recipes(self, channel_data: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actionable content recipes based on analysis"""
        
        recipes = []
        
        # Recipe 1: Hook-based formula
        if patterns.get('common_patterns'):
            top_pattern = list(patterns['common_patterns'].keys())[0] if patterns['common_patterns'] else None
            if top_pattern:
                recipes.append({
                    'name': 'Proven Pattern Formula',
                    'formula': f"Use '{top_pattern}' pattern + trending topic + emotional trigger",
                    'example': self._generate_example_title(top_pattern),
                    'expected_performance': 'High - based on historical data',
                    'best_for': 'Consistent performers'
                })
        
        # Recipe 2: Curiosity gap formula
        recipes.append({
            'name': 'Curiosity Gap Generator',
            'formula': "Start with 'Why/How' + unexpected element + specific outcome",
            'example': "Why This Simple Trick Doubled My Productivity",
            'expected_performance': 'Very High - triggers information gap',
            'best_for': 'Educational content'
        })
        
        # Recipe 3: Challenge/Transformation formula
        recipes.append({
            'name': 'Transformation Story',
            'formula': "I [action] for [timeframe] and [surprising result]",
            'example': "I Woke Up at 5AM for 30 Days and My Life Changed",
            'expected_performance': 'High - personal stories resonate',
            'best_for': 'Lifestyle/self-improvement content'
        })
        
        # Recipe 4: List-based formula
        recipes.append({
            'name': 'Numbered List Power',
            'formula': "[Odd number] + [surprising things] + [qualifier]",
            'example': "7 Hidden Features You Never Knew Existed",
            'expected_performance': 'Medium-High - clear value proposition',
            'best_for': 'Tutorial/tips content'
        })
        
        # Recipe 5: Controversy/Opinion formula
        recipes.append({
            'name': 'Bold Opinion Starter',
            'formula': "[Popular thing] is [controversial take] + here's why",
            'example': "This Popular Advice is Actually Terrible (Here's Why)",
            'expected_performance': 'Very High - drives engagement',
            'best_for': 'Commentary/opinion pieces'
        })
        
        # Generate title variations for top videos
        title_variations = []
        if channel_data.get('top_videos'):
            for video in channel_data['top_videos'][:3]:
                original_title = video['video'].get('title', '')
                variations = self._generate_title_variations(original_title)
                title_variations.append({
                    'original': original_title,
                    'variations': variations,
                    'original_views': video['video'].get('view_count', 0)
                })
        
        # Content calendar suggestions
        content_calendar = self._generate_content_calendar(patterns)
        
        return {
            'viral_recipes': recipes,
            'title_variations': title_variations,
            'content_calendar': content_calendar,
            'quick_wins': [
                "Add numbers to titles (odd numbers perform 23% better)",
                "Front-load titles with hook words",
                "Keep titles between 50-60 characters",
                "Use curiosity gaps but deliver on promise",
                "Test controversy carefully - high risk, high reward"
            ],
            'content_gaps': self._identify_content_gaps(patterns)
        }
    
    def _get_hook_recommendations(self, hooks_found: List[Dict], curiosity_score: int) -> List[str]:
        """Generate recommendations for improving hooks"""
        recommendations = []
        
        if not hooks_found:
            recommendations.append("Add a strong hook: try curiosity gap or transformation promise")
        
        if curiosity_score < 20:
            recommendations.append("Increase curiosity: add a question or incomplete thought")
        
        hook_types = [h['type'] for h in hooks_found]
        if 'fomo' not in hook_types:
            recommendations.append("Consider adding urgency or FOMO elements")
        
        if 'transformation' not in hook_types:
            recommendations.append("Show transformation or results to increase appeal")
        
        return recommendations
    
    def _get_title_optimization_recommendations(self, word_count: int, char_count: int, 
                                               caps_patterns: Dict, number_insights: Dict) -> List[str]:
        """Generate recommendations for title optimization"""
        recommendations = []
        
        if word_count < 8:
            recommendations.append("Title too short - aim for 8-12 words")
        elif word_count > 12:
            recommendations.append("Title too long - trim to 8-12 words for better visibility")
        
        if char_count > 70:
            recommendations.append("Title may be truncated in search - keep under 60 characters")
        
        if caps_patterns['all_caps']:
            recommendations.append("Avoid all caps - seems spammy. Use selective capitalization")
        
        if not number_insights['has_numbers']:
            recommendations.append("Consider adding numbers - increases CTR by 15-20%")
        
        if number_insights['has_numbers'] and not number_insights['uses_odd_numbers']:
            recommendations.append("Try odd numbers - they outperform even numbers")
        
        return recommendations
    
    def _matches_formula_pattern(self, title: str, formula: str) -> bool:
        """Check if title matches a formula pattern (simplified)"""
        formula_lower = formula.lower()
        title_lower = title.lower()
        
        # Simple heuristic matching
        if '[number]' in formula_lower and re.search(r'\d+', title):
            return True
        if 'why' in formula_lower and title_lower.startswith('why'):
            return True
        if 'how' in formula_lower and title_lower.startswith('how'):
            return True
        if 'the' in formula_lower and title_lower.startswith('the'):
            return True
        
        return False
    
    def _find_common_patterns(self, texts: List[str]) -> List[str]:
        """Find common starting patterns in texts"""
        if not texts:
            return []
        
        common = []
        # Find common 2-3 word starts
        starts = [' '.join(text.split()[:3]) for text in texts]
        start_counts = Counter(starts)
        
        for start, count in start_counts.most_common(5):
            if count > 1:
                common.append(start)
        
        return common
    
    def _find_common_words(self, texts: List[str]) -> List[Tuple[str, int]]:
        """Find common meaningful words across texts"""
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be'}
        
        all_words = []
        for text in texts:
            words = [w.lower() for w in text.split() if w.lower() not in stop_words and len(w) > 3]
            all_words.extend(words)
        
        return Counter(all_words).most_common(10)
    
    def _get_recommended_formulas(self, patterns: List[Dict]) -> List[Dict]:
        """Get recommended formulas based on performance"""
        # Return top 3 performing formulas
        top_formulas = []
        
        for pattern in patterns[:3]:
            if pattern.get('formula_matched'):
                top_formulas.append(pattern['formula_matched'])
        
        # Add default high-performers if not enough matched
        if len(top_formulas) < 3:
            top_formulas.extend(self.title_formulas[:3-len(top_formulas)])
        
        return top_formulas
    
    def _generate_example_title(self, pattern: str) -> str:
        """Generate an example title based on a pattern"""
        examples = {
            'question': "Why Is Everyone Talking About This?",
            'number_list': "5 Secrets That Changed Everything",
            'tutorial': "How to Master This in 30 Days",
            'ultimate_guide': "The Ultimate Guide to Success",
            'review': "Honest Review: Is It Worth It?",
            'comparison': "X vs Y: Which Is Better?",
            'emotional': "This Is Mind-Blowing!",
            'urgency': "Do This Now Before It's Too Late"
        }
        return examples.get(pattern, "Your Next Viral Title Here")
    
    def _generate_title_variations(self, original_title: str) -> List[Dict]:
        """Generate variations of a title using different formulas"""
        variations = []
        
        # Extract key topic from original
        # Simplified - in production, use NLP to extract main topic
        main_topic = original_title.split()[2:5] if len(original_title.split()) > 2 else original_title
        main_topic = ' '.join(main_topic) if isinstance(main_topic, list) else main_topic
        
        # Generate variations
        variations.append({
            'type': 'curiosity_gap',
            'title': f"The Truth About {main_topic} Nobody Tells You"
        })
        
        variations.append({
            'type': 'numbered_list',
            'title': f"7 Things About {main_topic} You Need to Know"
        })
        
        variations.append({
            'type': 'transformation',
            'title': f"How {main_topic} Changed Everything"
        })
        
        variations.append({
            'type': 'controversy',
            'title': f"Why {main_topic} Is Not What You Think"
        })
        
        variations.append({
            'type': 'urgency',
            'title': f"Watch This Before {main_topic} Changes Forever"
        })
        
        return variations
    
    def _generate_content_calendar(self, patterns: Dict) -> List[Dict]:
        """Generate content calendar suggestions"""
        calendar = [
            {
                'day': 'Monday',
                'content_type': 'Educational/Tutorial',
                'title_formula': 'How to [skill] in [timeframe]',
                'reason': 'Start week with value-driven content'
            },
            {
                'day': 'Wednesday',
                'content_type': 'Entertainment/Story',
                'title_formula': 'I tried [thing] and [result]',
                'reason': 'Mid-week engagement boost'
            },
            {
                'day': 'Friday',
                'content_type': 'List/Compilation',
                'title_formula': '[Number] [things] for [outcome]',
                'reason': 'Weekend-ready digestible content'
            },
            {
                'day': 'Sunday',
                'content_type': 'Deep Dive/Documentary',
                'title_formula': 'The [adjective] story of [topic]',
                'reason': 'Weekend long-form viewing'
            }
        ]
        return calendar
    
    def _identify_content_gaps(self, patterns: Dict) -> List[str]:
        """Identify content opportunities"""
        gaps = []
        
        if patterns.get('common_patterns'):
            used_patterns = list(patterns['common_patterns'].keys())
            all_patterns = ['question', 'number_list', 'tutorial', 'review', 'comparison', 'emotional']
            
            for pattern in all_patterns:
                if pattern not in used_patterns:
                    gaps.append(f"Try {pattern} format - underutilized in your content")
        
        gaps.append("Experiment with controversial takes for engagement")
        gaps.append("Create series content for better retention")
        gaps.append("Add more personality-driven content")
        
        return gaps[:5]  # Return top 5 gaps