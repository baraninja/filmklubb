# analysis.py

import pandas as pd
from typing import List, Dict
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def analyze_preferences(preferences: List[Dict]) -> Dict:
    """Analyze preferences data and return structured insights"""

    df = pd.DataFrame(preferences)

    # Basic statistics
    stats = {
        "total_users": len(df),
        "total_preferences": sum(df['genres'].apply(len)) + sum(df['moods'].apply(len)),
        "avg_genres_per_user": df['genres'].apply(len).mean(),
        "avg_moods_per_user": df['moods'].apply(len).mean()
    }

    # Genre analysis
    genre_counts = df['genres'].explode().value_counts()
    genre_data = pd.DataFrame({
        'Genre': genre_counts.index,
        'Count': genre_counts.values,
        'Percentage': (genre_counts.values / len(df) * 100).round(1)
    })

    # Mood analysis
    mood_counts = df['moods'].explode().value_counts()
    mood_data = pd.DataFrame({
        'Mood': mood_counts.index,
        'Count': mood_counts.values,
        'Percentage': (mood_counts.values / len(df) * 100).round(1)
    })

    # Time period analysis
    time_counts = df['time_periods'].explode().value_counts()
    time_data = pd.DataFrame({
        'Period': time_counts.index,
        'Count': time_counts.values,
        'Percentage': (time_counts.values / len(df) * 100).round(1)
    })

    # Language analysis
    lang_counts = df['languages'].explode().value_counts()
    lang_data = pd.DataFrame({
        'Language': lang_counts.index,
        'Count': lang_counts.values,
        'Percentage': (lang_counts.values / len(df) * 100).round(1)
    })

    # Trend analysis
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_counts = df.groupby('date').size().reset_index(name='submissions')

    return {
        "stats": stats,
        "genre_data": genre_data,
        "mood_data": mood_data,
        "time_data": time_data,
        "language_data": lang_data,
        "trends": daily_counts
    }

def create_genre_chart(genre_data: pd.DataFrame) -> go.Figure:
    """Create genre distribution chart"""

    fig = go.Figure(data=[
        go.Bar(
            x=genre_data['Count'],
            y=genre_data['Genre'],
            orientation='h',
            marker_color='#3b82f6',
            text=genre_data['Percentage'].apply(lambda x: f'{x}%'),
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Genre Distribution",
        xaxis_title="Number of Users",
        yaxis_title=None,
        showlegend=False,
        height=400,
        margin=dict(l=100, r=50, t=50, b=50)
    )

    return fig

def create_mood_chart(mood_data: pd.DataFrame) -> go.Figure:
    """Create mood distribution chart"""

    fig = go.Figure(data=[
        go.Bar(
            x=mood_data['Count'],
            y=mood_data['Mood'],
            orientation='h',
            marker_color='#8b5cf6',
            text=mood_data['Percentage'].apply(lambda x: f'{x}%'),
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Mood Distribution",
        xaxis_title="Number of Users",
        yaxis_title=None,
        showlegend=False,
        height=400,
        margin=dict(l=100, r=50, t=50, b=50)
    )

    return fig

def create_time_chart(time_data: pd.DataFrame) -> go.Figure:
    """Create time period distribution chart"""

    fig = px.pie(
        time_data,
        values='Count',
        names='Period',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(
        title="Time Period Distribution",
        showlegend=True,
        height=300,
        margin=dict(l=0, r=0, t=50, b=50)
    )

    return fig

def create_language_chart(lang_data: pd.DataFrame) -> go.Figure:
    """Create language distribution chart"""

    fig = px.pie(
        lang_data,
        values='Count',
        names='Language',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(
        title="Language Distribution",
        showlegend=True,
        height=300,
        margin=dict(l=0, r=0, t=50, b=50)
    )

    return fig

def create_trend_chart(trends: pd.DataFrame) -> go.Figure:
    """Create submission trends chart"""

    fig = go.Figure(data=go.Scatter(
        x=trends['date'],
        y=trends['submissions'],
        mode='lines+markers',
        line=dict(color='#3b82f6', width=2),
        marker=dict(color='#3b82f6', size=8)
    ))

    fig.update_layout(
        title="Submissions Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Submissions",
        showlegend=False,
        height=300,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig

def analyze_correlations(preferences: List[Dict]) -> pd.DataFrame:
    """Analyze correlations between genres and moods"""

    df = pd.DataFrame(preferences)

    # Create correlation matrix
    genre_mood_corr = pd.DataFrame()
    for _, row in df.iterrows():
        for genre in row['genres']:
            for mood in row['moods']:
                genre_mood_corr = pd.concat([
                    genre_mood_corr,
                    pd.DataFrame({'Genre': [genre], 'Mood': [mood]})
                ])

    corr_matrix = pd.crosstab(
        genre_mood_corr['Genre'],
        genre_mood_corr['Mood']
    )

    return corr_matrix

def create_correlation_chart(corr_matrix: pd.DataFrame) -> go.Figure:
    """Create correlation heatmap"""

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='Viridis'
    ))

    fig.update_layout(
        title="Genre-Mood Correlations",
        xaxis_title="Moods",
        yaxis_title="Genres",
        height=500,
        margin=dict(l=100, r=100, t=50, b=50)
    )

    return fig
