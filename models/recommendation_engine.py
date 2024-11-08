# recommendation_engine.py

import logging
from typing import List, Dict, Optional
from anthropic import Anthropic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MovieRecommendationEngine:
    """Movie recommendation engine using Anthropic's Claude API"""

    def __init__(self, anthropic_api_key: str):
        self.anthropic = Anthropic(api_key=anthropic_api_key)

    def generate_group_recommendations(self, preferences_data: List[Dict]) -> Dict:
        """Generate movie recommendations based on group preferences"""

        # Analyze group preferences
        group_analysis = self._analyze_group_preferences(preferences_data)

        prompt = self._create_group_prompt(group_analysis)

        try:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,  # Increased token limit to accommodate detailed Markdown
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = response.content[0].text.strip()

            # Extract Markdown content from the response
            markdown_content = self._extract_markdown(response_text)

            if markdown_content:
                return {
                    "markdown": markdown_content
                }
            else:
                return {
                    "error": "Failed to extract Markdown recommendations",
                    "raw_response": response_text
                }

        except Exception as e:
            logger.exception("Exception occurred while generating group recommendations.")
            return {
                "error": f"Error generating recommendations: {str(e)}",
                "raw_response": ""
            }

    def generate_personal_recommendations(self, user_preferences: Dict) -> Dict:
        """Generate personalized movie recommendations"""

        prompt = self._create_personal_prompt(user_preferences)

        try:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,  # Increased token limit
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = response.content[0].text.strip()

            # Extract Markdown content from the response
            markdown_content = self._extract_markdown(response_text)

            if markdown_content:
                return {
                    "markdown": markdown_content
                }
            else:
                return {
                    "error": "Failed to extract Markdown personal recommendations",
                    "raw_response": response_text
                }

        except Exception as e:
            logger.exception("Exception occurred while generating personal recommendations.")
            return {
                "error": f"Error generating personal recommendations: {str(e)}",
                "raw_response": ""
            }

    def _analyze_group_preferences(self, preferences_data: List[Dict]) -> Dict:
        """Analyze and summarize group preferences"""

        genres = {}
        moods = {}
        time_periods = {}
        quality_markers = {}
        languages = {}

        for pref in preferences_data:
            # Count genres
            for genre in pref.get('genres', []):
                genres[genre] = genres.get(genre, 0) + 1

            # Count moods
            for mood in pref.get('moods', []):
                moods[mood] = moods.get(mood, 0) + 1

            # Count time periods
            for period in pref.get('time_periods', []):
                time_periods[period] = time_periods.get(period, 0) + 1

            # Count quality markers
            for marker in pref.get('quality_markers', []):
                quality_markers[marker] = quality_markers.get(marker, 0) + 1

            # Count languages
            for lang in pref.get('languages', []):
                languages[lang] = languages.get(lang, 0) + 1

        total_users = len(preferences_data)

        # Convert to percentages and sort by popularity
        analysis = {
            "genres": dict(sorted(
                {k: (v / total_users) * 100 for k, v in genres.items()}.items(),
                key=lambda x: x[1], reverse=True
            )),
            "moods": dict(sorted(
                {k: (v / total_users) * 100 for k, v in moods.items()}.items(),
                key=lambda x: x[1], reverse=True
            )),
            "time_periods": dict(sorted(
                {k: (v / total_users) * 100 for k, v in time_periods.items()}.items(),
                key=lambda x: x[1], reverse=True
            )),
            "quality_markers": dict(sorted(
                {k: (v / total_users) * 100 for k, v in quality_markers.items()}.items(),
                key=lambda x: x[1], reverse=True
            )),
            "languages": dict(sorted(
                {k: (v / total_users) * 100 for k, v in languages.items()}.items(),
                key=lambda x: x[1], reverse=True
            )),
            "total_users": total_users
        }

        return analysis

    def _create_group_prompt(self, analysis: Dict) -> str:
        """Create prompt for group recommendations"""

        # Get top preferences
        top_genres = list(analysis['genres'].keys())[:5]
        top_moods = list(analysis['moods'].keys())[:5]
        top_periods = list(analysis['time_periods'].keys())[:3]
        top_markers = list(analysis['quality_markers'].keys())[:3]

        prompt = f"""You are a friendly and knowledgeable film expert. Based on these group preferences:

Top Genres: {', '.join(top_genres)}
Top Moods: {', '.join(top_moods)}
Preferred Time Periods: {', '.join(top_periods)}
Quality Markers: {', '.join(top_markers)}

Please recommend movies in these categories:

1. Five "Must-Watch" films that would appeal to the whole group
2. Three mood-based recommendations for each of the top 3 moods
3. Three "Discovery" picks that could expand the group's horizons while still being enjoyable

For each movie, include:
- **Title and Year**
- **Genres**
- **Brief Description**
- **Match Score (0-100)**
- **Selling Points** (bullet list of 3 items)
- **Explanation** of why it's recommended

Provide the recommendations formatted in Markdown with clear headings, subheadings, and bullet points. Do not include any additional text or explanations outside the Markdown content.
"""

        return prompt

    def _create_personal_prompt(self, preferences: Dict) -> str:
        """Create prompt for personal recommendations"""

        prompt = f"""You are a friendly and knowledgeable film expert. Based on these user preferences:

Favorite Genres: {', '.join(preferences.get('genres', []))}
Preferred Moods: {', '.join(preferences.get('moods', []))}
Time Periods: {', '.join(preferences.get('time_periods', []))}
Quality Markers: {', '.join(preferences.get('quality_markers', []))}
Languages: {', '.join(preferences.get('languages', []))}

Please recommend movies in these categories:

1. Three perfect matches based on these preferences
2. Three personal picks you think this person would especially enjoy
3. Three "bridge" picks that could help them explore new genres/styles while still being enjoyable

For each movie, include:
- **Title and Year**
- **Genres**
- **Brief Description**
- **Match Score (0-100)**
- **Selling Points** (bullet list of 3 items)
- **Explanation** of why it's recommended

Provide the recommendations formatted in Markdown with clear headings, subheadings, and bullet points. Do not include any additional text or explanations outside the Markdown content.
"""

        return prompt

    def _extract_markdown(self, text: str) -> Optional[str]:
        """Extract Markdown content from text."""
        try:
            # Assuming the AI returns pure Markdown as instructed
            return text
        except Exception as e:
            logger.error(f"Error extracting Markdown: {e}")
            return None
