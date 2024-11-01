from typing import Dict

import streamlit as st

from crew import PlaiCrew
from playlist_params import PlaylistParams


class PlaiApp:
    def __init__(self):
        # Initialize session state if not already done
        if "processing" not in st.session_state:
            st.session_state.processing = False
        if "playlist_result" not in st.session_state:
            st.session_state.playlist_result = None

    def process_playlist(self, params: Dict) -> None:
        """Handle the playlist creation process using CrewAI"""
        try:
            # Convert the dictionary to PlaylistParams object
            playlist_params = PlaylistParams(**params)

            # Initialize and run the crew
            crew = PlaiCrew(playlist_params)
            result = crew.run().kickoff()

            # Store the result in session state
            st.session_state.playlist_result = result
            st.session_state.processing = False

        except Exception as e:
            st.error(f"An error occurred while creating the playlist: {str(e)}")
            st.session_state.processing = False

    def run(self):
        # Set page configuration
        st.set_page_config(page_title="Playlist Creator", page_icon="🎵", layout="wide")

        # Main title and description
        st.title("🎵 Custom Playlist Creator")
        st.write(
            "Please fill in your preferences to create your personalized playlist."
        )

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

        # Submit button and processing logic
        if st.button(
            "Create Playlist", type="primary", disabled=st.session_state.processing
        ):
            # Collect parameters
            playlist_params = {
                "genre": genre,
                "subgenre": subgenre if subgenre else None,
                "duration": duration,
                "target_audience": target_audience,
                "mood": mood,
                "additional_requirements": {
                    "preferences": preferences if preferences else None,
                    "tempo_range": {"min": tempo_range[0], "max": tempo_range[1]},
                    "explicit_content": explicit_content,
                    "languages": language,
                },
            }

            # Update processing state
            st.session_state.processing = True

            # Display progress
            with st.spinner("Creating your playlist... This may take a few minutes."):
                self.process_playlist(playlist_params)

        # Display results if available
        if st.session_state.playlist_result:
            st.success("🎉 Playlist created successfully!")

            # Create tabs for different aspects of the result
            tabs = st.tabs(["Playlist", "Details", "Download"])

            with tabs[0]:
                st.write("### Your Playlist")
                st.write(st.session_state.playlist_result.get("playlist", []))

            with tabs[1]:
                st.write("### Playlist Details")
                st.json(st.session_state.playlist_result.get("details", {}))

            with tabs[2]:
                st.write("### Download Options")
                if st.button("Download Playlist"):
                    # Add download functionality here
                    st.download_button(
                        label="Download Playlist Files",
                        data=st.session_state.playlist_result.get("download_data", b""),
                        file_name="playlist.zip",
                        mime="application/zip",
                    )

        return None
