# app.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from models.recommendation_engine import MovieRecommendationEngine
from utils.analysis import (
    analyze_preferences,
    create_genre_chart,
    create_mood_chart,
    create_time_chart,
    create_language_chart,
    create_trend_chart,
    analyze_correlations,
    create_correlation_chart
)
import time  # Import time for simulating progress
import hashlib
import json
from bson import ObjectId  # Import ObjectId for type checking

# Function to hash preferences data
def hash_preferences(preferences_data):
    # Serialize the preferences data to a JSON string with sorted keys for consistency
    preferences_str = json.dumps(preferences_data, sort_keys=True)
    # Create a SHA256 hash of the string
    return hashlib.sha256(preferences_str.encode()).hexdigest()

# Function to convert ObjectId and datetime to string
def convert_objectid_and_datetime(preferences):
    """Converts ObjectId and datetime objects to strings in each document."""
    for pref in preferences:
        if '_id' in pref and isinstance(pref['_id'], ObjectId):
            pref['_id'] = str(pref['_id'])
        if 'timestamp' in pref and isinstance(pref['timestamp'], datetime):
            pref['timestamp'] = pref['timestamp'].isoformat()
    return preferences

# Page configuration
st.set_page_config(
    page_title="Film Preferences & Recommendations",
    page_icon="🎬",
    layout="wide"
)

# Load environment variables
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize MongoDB connection
@st.cache_resource
def init_mongodb():
    try:
        client = MongoClient(MONGODB_URI)
        return client.movie_preferences
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return None

db = init_mongodb()

# Initialize recommendation engine
@st.cache_resource
def init_engine():
    return MovieRecommendationEngine(anthropic_api_key=ANTHROPIC_API_KEY)

engine = init_engine()

# Constants
GENRES = [
    "Science Fiction", "Crime Drama", "New York Stories", 
    "Psychological Thriller", "Action Adventure", "Mystery", 
    "Romantic Comedy", "Musical", "Documentary", "War Film", 
    "Fantasy", "Historical Drama", "Animated"
]

TIME_PERIODS = [
    "Present Day", "Mid-20th Century", "Future", 
    "19th Century", "Medieval"
]

QUALITY_MARKERS = [
    "Cult Classic", "Hidden Gem", "Critically Acclaimed", 
    "Oscar Nominated", "Crowd Favorite"
]

LANGUAGES = ["Swedish", "English", "Other Languages"]

MOODS = [
    "Thrilling", "Feel-good", "Philosophical", "Dark and Dystopian",
    "Action-packed", "Inspiring", "Mysterious", "Playful", 
    "Mind-bending", "Humorous", "Melancholic", "Cozy", 
    "Romantic", "Nostalgic"
]

# Load custom CSS
def load_css():
    try:
        with open('.streamlit/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Continuing without custom styles.")

load_css()

# App header
st.markdown("""
    <div class="app-header">
        <div class="header-content">
            <h1>🎬 Film Preferences Analysis (Beta)</h1>
            <p>Discover group dynamics and get personalized recommendations</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    # Display logo if available
    if os.path.exists("static/logo.png"):
        st.image("static/logo.png", width=300)
    else:
        st.write("<h3>🎬 Film Club</h3>", unsafe_allow_html=True)
    
    selected = st.radio(
        "Navigation",
        ["Submit Preferences", "View Analysis", "Get Recommendations"]
    )
    
    st.markdown("---")
    
    if db is not None:
        # Quick stats
        total_entries = db.preferences.count_documents({})
        recent_entries = db.preferences.count_documents({
            "timestamp": {"$gte": datetime.now() - timedelta(days=7)}
        })

        st.metric("Total Entries", total_entries)
        st.metric("New This Week", recent_entries)

# Caching function for group recommendations based on the hash
@st.cache_data(show_spinner=False)
def get_group_recommendations(preferences_hash, _preferences_data):
    return engine.generate_group_recommendations(_preferences_data)

# Main content
if selected == "Submit Preferences":
    st.title("Share Your Film Preferences")
    
    with st.form("preferences_form", clear_on_submit=True):
        st.markdown("""
            <div class="form-intro">
                <p>Help us understand your film preferences. Your input will improve our group recommendations.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name")
            genres = st.multiselect("Favorite Genres", GENRES)
            time_periods = st.multiselect("Preferred Time Periods", TIME_PERIODS)
            languages = st.multiselect("Language Preferences", LANGUAGES)
        
        with col2:
            quality_markers = st.multiselect("Quality Markers", QUALITY_MARKERS)
            moods = st.multiselect("Preferred Moods", MOODS)
        
        submit = st.form_submit_button("Submit Preferences")
        
        if submit:
            if not name or not genres or not time_periods or not languages or not quality_markers or not moods:
                st.error("Please fill in all fields")
            else:
                with st.spinner("Saving your preferences..."):
                    try:
                        # Create preference document
                        preference = {
                            "name": name,
                            "genres": genres,
                            "time_periods": time_periods,
                            "languages": languages,
                            "quality_markers": quality_markers,
                            "moods": moods,
                            "timestamp": datetime.now()
                        }
                        
                        # Save to MongoDB
                        db.preferences.insert_one(preference)
                        st.success("Thank you! Your preferences have been saved.")
                        st.balloons()
                        
                        # Clear form
                        st.experimental_rerun()
                        
                    except Exception as e:
                        st.error(f"Error saving preferences: {str(e)}")

elif selected == "View Analysis":
    st.title("Group Preferences Analysis")
    
    # Retrieve preferences and convert ObjectId and datetime to string
    preferences = list(db.preferences.find())
    preferences = convert_objectid_and_datetime(preferences)
    
    if not preferences:
        st.info("No preferences have been submitted yet.")
    else:
        df = pd.DataFrame(preferences)
        
        # **Convert 'timestamp' column from string back to datetime**
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Perform analysis
        analysis_results = analyze_preferences(preferences)
        
        stats = analysis_results["stats"]
        genre_data = analysis_results["genre_data"]
        mood_data = analysis_results["mood_data"]
        time_data = analysis_results["time_data"]
        lang_data = analysis_results["language_data"]
        trends = analysis_results["trends"]
        corr_matrix = analyze_correlations(preferences)
        
        # Overview Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Active Users",
                stats["total_users"],
                delta=f"+{len(df[df['timestamp'] >= datetime.now() - timedelta(days=7)])} this week"
            )
        with col2:
            st.metric("Avg. Genres/User", f"{stats['avg_genres_per_user']:.1f}")
        with col3:
            st.metric("Avg. Moods/User", f"{stats['avg_moods_per_user']:.1f}")
        with col4:
            st.metric("Total Preferences", stats["total_preferences"])
        
        st.markdown("---")
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["Distributions", "Trends", "Correlations", "Language Preferences"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Genre Distribution
                st.markdown("### Genre Preferences")
                fig_genres = create_genre_chart(genre_data)
                st.plotly_chart(fig_genres, use_container_width=True)
            
            with col2:
                # Mood Distribution
                st.markdown("### Mood Preferences")
                fig_moods = create_mood_chart(mood_data)
                st.plotly_chart(fig_moods, use_container_width=True)
        
        with tab2:
            # Trend Analysis
            st.markdown("### Submissions Over Time")
            fig_trends = create_trend_chart(trends)
            st.plotly_chart(fig_trends, use_container_width=True)
        
        with tab3:
            # Correlation Heatmap
            st.markdown("### Genre-Mood Correlations")
            fig_corr = create_correlation_chart(corr_matrix)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with tab4:
            # Language Preferences
            st.markdown("### Language Preferences")
            fig_lang = create_language_chart(lang_data)
            st.plotly_chart(fig_lang, use_container_width=True)

elif selected == "Get Recommendations":
    st.title("Movie Recommendations")
    
    # Get all preferences from database and convert ObjectId and datetime to string
    preferences_data = list(db.preferences.find())
    preferences_data = convert_objectid_and_datetime(preferences_data)
    
    if not preferences_data:
        st.warning("No preferences found. Please submit preferences first.")
    else:
        with st.container():
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            progress_bar = progress_placeholder.progress(0)
            status_messages = ["Analyzing preferences...", "Generating recommendations...", "Finalizing..."]
            for i, message in enumerate(status_messages):
                status_placeholder.text(message)
                progress_bar.progress((i + 1) / len(status_messages))
                time.sleep(1)  # Simulate processing time
        
            try:
                st.write("🎬 Finding the perfect movies for your group...")
                
                # Compute the hash of preferences_data
                preferences_hash = hash_preferences(preferences_data)
                
                # Generate group recommendations (cached)
                recommendations = get_group_recommendations(preferences_hash, preferences_data)
                
                if "error" in recommendations:
                    st.error(recommendations["error"])
                    st.text_area("Raw Response", recommendations["raw_response"], height=200)
                else:
                    # Display recommendations in Markdown
                    st.markdown(recommendations["markdown"], unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
col1, col2 = st.columns([4,1])
with col2:
    st.markdown(
        '<p class="footer-text">Developed by Anders Barane</p>',
        unsafe_allow_html=True
    )
