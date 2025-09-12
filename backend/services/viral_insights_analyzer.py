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
        
        # Generate concrete takeaways
        hook_takeaways = self._generate_hook_takeaways(hooks_found, curiosity_elements, emotions_triggered, title)
        
        return {
            'hooks_found': hooks_found,
            'hook_effectiveness_score': round(hook_effectiveness, 2),
            'curiosity_elements': curiosity_elements,
            'curiosity_score': curiosity_score,
            'emotions_triggered': emotions_triggered,
            'has_power_hook': hook_effectiveness > 70,
            'recommendations': self._get_hook_recommendations(hooks_found, curiosity_score),
            'takeaways': hook_takeaways
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
            'optimization_score': round(optimization_score, 2),
            'recommendations': self._get_title_optimization_recommendations(word_count, char_count, caps_patterns, number_insights),
            'full_title': title,
            'performance_insights': self._generate_performance_insights(title, optimization_score, number_insights, punctuation_analysis)
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
        
        # Generate actual usable templates
        templates = self._generate_content_templates(top_videos)
        
        # Find common elements
        common_starts = self._find_common_patterns([v['title'][:20] for v in top_videos])
        common_words = self._find_common_words([v['title'] for v in top_videos])
        
        # Generate template library
        template_library = {
            'ready_to_use_templates': templates,
            'common_opening_phrases': common_starts,
            'power_words': [word for word, count in common_words if count > 1],
            'copy_paste_formulas': self._get_copy_paste_templates(),
            'title_starters': self._get_title_starters(),
            'engagement_boosters': self._get_engagement_boosters()
        }
        
        return template_library
    
    def _generate_content_templates(self, top_videos: List[Dict]) -> List[Dict]:
        """Generate actual templates people can copy and adapt"""
        templates = []
        
        # Template 1: The Curiosity Gap
        templates.append({
            'name': 'The Curiosity Gap Template',
            'template': "Why [unexpected thing] is [surprising outcome]",
            'examples': [
                "Why Sleeping Less Makes You More Productive",
                "Why Expensive Cars Are Actually Cheaper",
                "Why Smart People Make Dumb Decisions"
            ],
            'fill_in': "Why _______ is _______",
            'instructions': "Fill first blank with common belief, second with opposite/unexpected"
        })
        
        # Template 2: The Number Hook
        templates.append({
            'name': 'The Number List Template',
            'template': "[Odd number] [category] That [benefit/outcome]",
            'examples': [
                "7 Morning Habits That Changed My Life",
                "5 Investments That Made Me Rich",
                "3 Books That Destroyed My Limiting Beliefs"
            ],
            'fill_in': "__ _______ That _______",
            'instructions': "Use odd numbers (3,5,7,9), be specific about the outcome"
        })
        
        # Template 3: The Transformation Story
        templates.append({
            'name': 'The Transformation Template',
            'template': "I [action] for [timeframe] - Here's What Happened",
            'examples': [
                "I Cold Called 100 CEOs - Here's What Happened",
                "I Meditated for 365 Days - Here's What Happened",
                "I Quit Coffee for a Month - Here's What Happened"
            ],
            'fill_in': "I _______ for _______ - Here's What Happened",
            'instructions': "Be specific about action and timeframe, promise revelation"
        })
        
        # Template 4: The Mistake Revealer
        templates.append({
            'name': 'The Mistake Template',
            'template': "The #1 [category] Mistake (And How to Fix It)",
            'examples': [
                "The #1 Investing Mistake (And How to Fix It)",
                "The #1 Dating Mistake (And How to Fix It)",
                "The #1 YouTube Mistake (And How to Fix It)"
            ],
            'fill_in': "The #1 _______ Mistake (And How to Fix It)",
            'instructions': "Target your audience's main pain point, promise solution"
        })
        
        # Template 5: The Controversy Starter
        templates.append({
            'name': 'The Controversial Opinion Template',
            'template': "[Popular thing] is [controversial take] - Let Me Explain",
            'examples': [
                "College is a Scam - Let Me Explain",
                "Motivation is Useless - Let Me Explain",
                "Networking is Dead - Let Me Explain"
            ],
            'fill_in': "_______ is _______ - Let Me Explain",
            'instructions': "Challenge popular belief, but promise reasoning"
        })
        
        # Template 6: The Behind-the-Scenes
        templates.append({
            'name': 'The Insider Template',
            'template': "How [successful entity] Actually [does something]",
            'examples': [
                "How MrBeast Actually Makes His Videos",
                "How Millionaires Actually Think About Money",
                "How Top Students Actually Study"
            ],
            'fill_in': "How _______ Actually _______",
            'instructions': "Promise insider knowledge about successful people/companies"
        })
        
        return templates
    
    def _get_copy_paste_templates(self) -> List[str]:
        """Get ready-to-use title templates"""
        return [
            "This Changed Everything: _______",
            "Stop _______ Start _______",
            "_______ Doesn't Work (Do This Instead)",
            "The Real Reason You're _______",
            "_______ in 2024: Everything You Need to Know",
            "I Was Wrong About _______",
            "_______ Is Not What You Think",
            "The Hidden Cost of _______",
            "_______ Explained in 10 Minutes",
            "Nobody Talks About This: _______"
        ]
    
    def _get_title_starters(self) -> List[str]:
        """Get proven title starters"""
        return [
            "The Truth About...",
            "Why I Stopped...",
            "How to Actually...",
            "The Problem With...",
            "What Nobody Tells You About...",
            "The Secret to...",
            "Everything Wrong With...",
            "I Tried... for 30 Days",
            "The Ultimate Guide to...",
            "This Is Why You're..."
        ]
    
    def _get_engagement_boosters(self) -> List[str]:
        """Get phrases that boost engagement"""
        return [
            "(You Won't Believe #3)",
            "(With Proof)",
            "(Science-Based)",
            "(Step-by-Step)",
            "(No BS)",
            "(In 2024)",
            "(For Beginners)",
            "(Advanced Strategy)",
            "(Watch Till End)",
            "(Life-Changing)"
        ]
    
    def generate_viral_recipes(self, channel_data: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actionable content recipes based on analysis"""
        
        recipes = []
        
        # Recipe 1: The Curiosity Loop
        recipes.append({
            'name': 'The Curiosity Loop Recipe',
            'formula': "Question Hook + Information Gap + Promise of Revelation",
            'concrete_example': {
                'hook': "Why do millionaires wake up at 4 AM?",
                'gap': "It's not what you think...",
                'reveal': "The 3 morning rituals that separate the ultra-rich from everyone else"
            },
            'emotional_triggers': [
                "FOMO: 'What successful people know that I don't?'",
                "Curiosity: 'I need to know this secret'",
                "Aspiration: 'I want to be like them'"
            ],
            'how_to_apply': "1. Start with counterintuitive question\n2. Challenge common assumption\n3. Promise specific, actionable insight",
            'expected_ctr': '8-12% (2x average)'
        })
        
        # Recipe 2: The Transformation Journey
        recipes.append({
            'name': 'The Personal Experiment Recipe',
            'formula': "Specific Challenge + Exact Timeframe + Measurable Result",
            'concrete_example': {
                'setup': "I cold emailed 100 CEOs in 30 days",
                'journey': "Document the process, failures, and surprises",
                'payoff': "3 responded, 1 became my mentor, here's exactly what I said"
            },
            'emotional_triggers': [
                "Relatability: 'I could try this too'",
                "Proof: 'Real person, real results'",
                "Hope: 'If they can do it, so can I'"
            ],
            'how_to_apply': "1. Pick specific, replicable action\n2. Set clear timeframe (30/60/90 days)\n3. Share exact results with proof",
            'expected_ctr': '7-10% (1.5x average)'
        })
        
        # Recipe 3: The Controversy Hook
        recipes.append({
            'name': 'The Sacred Cow Slayer Recipe',
            'formula': "Popular Belief + Controversial Counter + Evidence",
            'concrete_example': {
                'belief': "Everyone says 'follow your passion'",
                'counter': "Following your passion is terrible advice",
                'evidence': "Here's what 1000 successful entrepreneurs did instead"
            },
            'emotional_triggers': [
                "Shock: 'Wait, everything I believed is wrong?'",
                "Vindication: 'I knew something was off!'",
                "Debate: 'I need to defend/attack this position'"
            ],
            'how_to_apply': "1. Identify widely accepted belief\n2. Present opposite view boldly\n3. Back with data/stories/authority",
            'expected_ctr': '10-15% (2.5x average) but polarizing'
        })
        
        # Recipe 4: The Insider Secret
        recipes.append({
            'name': 'The Behind-the-Curtain Recipe',
            'formula': "Industry/Expert + Hidden Truth + Specific Tactics",
            'concrete_example': {
                'authority': "Ex-Google engineer reveals",
                'secret': "The interview question that gets you hired",
                'specifics': "Say these exact 3 sentences when asked about weaknesses"
            },
            'emotional_triggers': [
                "Exclusivity: 'Insider information others don't have'",
                "Authority: 'From someone who actually knows'",
                "Advantage: 'This gives me an edge'"
            ],
            'how_to_apply': "1. Establish credibility upfront\n2. Promise specific insider knowledge\n3. Deliver exact scripts/formulas/tactics",
            'expected_ctr': '9-12% (2x average)'
        })
        
        # Recipe 5: The Number Stack
        recipes.append({
            'name': 'The Oddly Specific Recipe',
            'formula': "Odd Number + Unexpected Items + Clear Benefit",
            'concrete_example': {
                'number': "7",
                'items': "websites nobody knows about",
                'benefit': "that will make you $1000/month"
            },
            'emotional_triggers': [
                "Specificity: '7 is precise, must be researched'",
                "Discovery: 'Hidden gems I haven't found'",
                "ROI: 'Clear value proposition'"
            ],
            'how_to_apply': "1. Use odd numbers (3,5,7,9,11)\n2. Promise unknown/hidden resources\n3. Quantify the benefit clearly",
            'expected_ctr': '6-9% (1.5x average)'
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
        
        # Concrete quick wins with examples
        quick_wins = [
            {
                'tip': "Use odd numbers in titles",
                'why': "Odd numbers feel more authentic and specific",
                'example': "Change '10 Tips' to '7 Tips' or '11 Tips'",
                'impact': "+23% CTR on average"
            },
            {
                'tip': "Front-load your hook",
                'why': "First 3 words determine if people keep reading",
                'example': "Start with 'Why', 'How', 'The Secret', or numbers",
                'impact': "+15% CTR improvement"
            },
            {
                'tip': "Create urgency without clickbait",
                'why': "FOMO drives clicks but maintain trust",
                'example': "Add '(2024 Update)' or 'Before It Changes'",
                'impact': "+18% CTR boost"
            },
            {
                'tip': "Use parentheses for bonus info",
                'why': "Adds value without cluttering main title",
                'example': "How to Invest (Step-by-Step Guide)",
                'impact': "+12% CTR increase"
            },
            {
                'tip': "Challenge common beliefs",
                'why': "Cognitive dissonance makes people click",
                'example': "'Why Working Hard is Bad Advice'",
                'impact': "+30% engagement but polarizing"
            }
        ]
        
        return {
            'viral_recipes': recipes,
            'title_variations': title_variations,
            'content_calendar': content_calendar,
            'quick_wins': quick_wins,
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
    
    def _generate_hook_takeaways(self, hooks_found: List[Dict], curiosity_elements: List[str], 
                                 emotions_triggered: List[Dict], title: str) -> List[str]:
        """Generate concrete takeaways explaining why the hook works"""
        takeaways = []
        
        if hooks_found:
            for hook in hooks_found[:2]:  # Top 2 hooks
                hook_type = hook['type']
                if hook_type == 'curiosity_gap':
                    takeaways.append("Creates information gap - viewers MUST click to close the mental loop. The brain hates incomplete information.")
                elif hook_type == 'challenge':
                    takeaways.append("Triggers competitive instinct - people want to see if they could do it too. Makes content relatable and achievable.")
                elif hook_type == 'revelation':
                    takeaways.append("Promises insider knowledge - humans are wired to want exclusive information others don't have.")
                elif hook_type == 'transformation':
                    takeaways.append("Shows clear before/after - people crave improvement and want to know the exact steps.")
                elif hook_type == 'controversy':
                    takeaways.append("Challenges beliefs - triggers emotional response and comment engagement. People click to agree or argue.")
                elif hook_type == 'fomo':
                    takeaways.append("Fear of missing out - creates urgency and social pressure. Nobody wants to be left behind.")
        
        if 'question' in curiosity_elements:
            takeaways.append("Direct question engages viewer's brain - they automatically start thinking of the answer, creating investment.")
        
        if 'specific_number' in curiosity_elements:
            takeaways.append("Specific numbers build trust and set clear expectations - viewers know exactly what they'll get.")
        
        if emotions_triggered:
            emotion = emotions_triggered[0]['emotion']
            if emotion == 'excitement':
                takeaways.append("High-energy words create anticipation - viewers expect something extraordinary.")
            elif emotion == 'curiosity':
                takeaways.append("Mystery words activate the brain's reward center - the unknown is irresistible.")
            elif emotion == 'urgency':
                takeaways.append("Time-sensitive language triggers immediate action - prevents procrastination.")
        
        if not takeaways:
            takeaways.append("Consider adding stronger hooks - curiosity gaps, transformations, or controversial angles work best.")
        
        return takeaways
    
    def _generate_performance_insights(self, title: str, optimization_score: float, 
                                      number_insights: Dict, punctuation_analysis: Dict) -> List[str]:
        """Generate insights explaining why the title performs well"""
        insights = []
        
        if optimization_score > 80:
            insights.append(f"This title scores {optimization_score:.0f}/100 because it hits the sweet spot of length and clarity.")
        
        if number_insights['has_numbers']:
            if number_insights['uses_odd_numbers']:
                insights.append("Odd numbers feel more authentic and specific than round numbers - increases credibility by 20%.")
            if number_insights['number_placement'] == 'beginning':
                insights.append("Leading with numbers sets clear expectations - viewers know the content structure immediately.")
        
        if punctuation_analysis['has_question_mark']:
            insights.append("Questions activate the viewer's problem-solving mode - they click to find the answer.")
        
        if punctuation_analysis['has_colon']:
            insights.append("Colons create a setup/payoff structure - builds anticipation for what comes after.")
        
        if len(title) > 60:
            insights.append("⚠️ Title may get cut off in search results - keep main hook in first 60 characters.")
        
        # Analyze power words
        power_words = ['secret', 'revealed', 'truth', 'nobody', 'everyone', 'mistake', 'wrong', 'simple', 'easy', 'proven']
        title_lower = title.lower()
        found_power_words = [word for word in power_words if word in title_lower]
        
        if found_power_words:
            insights.append(f"Power words '{', '.join(found_power_words)}' trigger emotional response and increase CTR by 15-25%.")
        
        if not insights:
            insights.append("This title could be optimized - add numbers, questions, or power words for better performance.")
        
        return insights