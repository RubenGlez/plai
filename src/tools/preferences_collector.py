from typing import Dict

import streamlit as st
from langchain.tools import tool


@tool(
    """Tool for collecting and validating user input for playlist creation.
    Collects genre, subgenre, target audience, mood, and duration preferences.""",
)
def collect_playlist_preferences() -> Dict:
    """Collects and validates user preferences for playlist creation using Streamlit."""

    # Set page configuration
    st.set_page_config(page_title="Playlist Creator", page_icon="🎵", layout="wide")

    # Main title and description
    st.title("🎵 Custom Playlist Creator")
    st.write("Please fill in your preferences to create your personalized playlist.")

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        # Genre selection
        genre = st.selectbox(
            "Select Main Genre",
            options=[
                "Pop",
                "Rock",
                "Hip Hop",
                "Electronic",
                "Jazz",
                "Classical",
                "R&B",
                "Latin",
                "Metal",
                "Folk",
                "Country",
                "Indie",
            ],
            help="Choose the primary genre for your playlist",
        )

        # Subgenre input
        subgenre = st.text_input(
            "Subgenre (Optional)",
            help="Specify a subgenre if you have a preference",
        )

        # Duration selection
        duration = st.slider(
            "Playlist Duration (minutes)",
            min_value=10,
            max_value=180,
            value=60,
            step=10,
            help="Select the desired length of your playlist",
        )

    with col2:
        # Target audience/environment
        target_audience = st.selectbox(
            "Target Audience/Environment",
            options=[
                "Party",
                "Workout",
                "Study",
                "Relaxation",
                "Work",
                "Commute",
                "Dinner",
                "Background",
                "Focus",
                "Sleep",
            ],
            help="Choose the primary use case for your playlist",
        )

        # Mood selection
        mood = st.select_slider(
            "Mood/Energy Level",
            options=[
                "Very Calm",
                "Calm",
                "Moderate",
                "Energetic",
                "Very Energetic",
            ],
            value="Moderate",
            help="Select the desired mood or energy level",
        )

        # Additional preferences
        preferences = st.text_area(
            "Additional Preferences (Optional)",
            help="Add any specific preferences or requirements",
        )

    # Advanced options in an expander
    with st.expander("Advanced Options"):
        tempo_range = st.slider(
            "Tempo Range (BPM)",
            min_value=60,
            max_value=200,
            value=(80, 160),
            help="Select the range of beats per minute",
        )

        explicit_content = st.radio(
            "Explicit Content", options=["Allow", "Exclude"], horizontal=True
        )

        language = st.multiselect(
            "Preferred Languages",
            options=[
                "English",
                "Spanish",
                "French",
                "German",
                "Japanese",
                "Korean",
                "Any",
            ],
            default=["English"],
        )

    # Submit button
    if st.button("Create Playlist", type="primary"):
        playlist_params = {
            "genre": genre,
            "subgenre": subgenre if subgenre else None,
            "duration_minutes": duration,
            "target_audience": target_audience,
            "mood": mood,
            "additional_preferences": preferences if preferences else None,
            "advanced_options": {
                "tempo_range": {"min": tempo_range[0], "max": tempo_range[1]},
                "explicit_content": explicit_content,
                "languages": language,
            },
        }

        # Display the collected parameters
        st.success("Playlist parameters collected successfully!")
        st.json(playlist_params)

        return playlist_params

    return None
