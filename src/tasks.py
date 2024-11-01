from typing import Any, Dict, List

from crewai import Agent, Task

from playlist_params import PlaylistParams


class PlaiTasks:
    def get_user_parameters_task(
        self, agent: Agent, playlist_params: PlaylistParams
    ) -> Task:
        # Extract and validate parameters
        additional_reqs = playlist_params["additional_requirements"]

        params_summary = {
            "genre": playlist_params["genre"],
            "subgenre": playlist_params.get("subgenre", "Not specified"),
            "target_audience": playlist_params["target_audience"],
            "duration": playlist_params["duration"],
            "mood": playlist_params["mood"],
            "preferences": additional_reqs.get("preferences", "None specified"),
            "tempo_range": f"{additional_reqs['tempo_range']['min']}-{additional_reqs['tempo_range']['max']} BPM",
            "explicit_content": additional_reqs["explicit_content"],
            "languages": ", ".join(additional_reqs["languages"]),
        }

        return Task(
            description=f"""Given these playlist parameters, perform a detailed analysis:

            Input Parameters:
            {params_summary}

            Required Analysis Steps:
            1. Genre Analysis:
               - Map {params_summary['genre']} and {params_summary['subgenre']} to specific musical elements
               - Identify key instruments, rhythmic patterns, and harmonic structures
               - List any genre-specific conventions or requirements

            2. Audience & Context Analysis:
               - Define typical listening scenarios for {params_summary['target_audience']}
               - Identify acoustic requirements for the environment
               - Map audience demographics to music preferences

            3. Mood & Energy Mapping:
               - Convert "{params_summary['mood']}" into specific musical parameters
               - Define energy curve expectations
               - Identify key emotional triggers in music

            4. Technical Requirements:
               - Validate tempo range ({params_summary['tempo_range']}) for genre compatibility
               - Define volume normalization requirements
               - Specify transition requirements between songs

            5. Content Guidelines:
               - Create language filtering rules based on: {params_summary['languages']}
               - Define explicit content rules: {params_summary['explicit_content']}
               - Incorporate user preferences: {params_summary['preferences']}""",
            agent=agent,
            expected_output="""Provide a structured analysis of the playlist parameters including:
            1. Validated genre and musical style specifications
            2. Target audience and environment characteristics
            3. Musical features and constraints
            4. Content filtering rules
            5. Any special considerations for playlist creation""",
            context="""This initial task establishes the foundation for the entire playlist creation process.
            The output will guide all subsequent tasks in searching for and selecting appropriate music.
            Focus on creating clear, actionable specifications that will result in a cohesive playlist.""",
        )

    def analyze_parameters_task(self, agent: Agent, user_params: Dict) -> Task:
        return Task(
            description="""Transform the validated parameters into specific search criteria:

            Required Steps:
            1. Musical Feature Extraction:
               - Define acceptable ranges for: tempo, key, mode, danceability, energy, valence
               - Specify required instrumental elements
               - List prohibited musical characteristics

            2. Keyword Generation:
               - Create primary search terms from genre/subgenre
               - Generate mood-based descriptive keywords
               - Include audience-specific terminology
               - Define excluded terms

            3. Audio Profile Creation:
               - Specify target acousticness range
               - Define acceptable instrumentalness levels
               - Set loudness and dynamic range requirements

            4. Metadata Requirements:
               - List required track metadata fields
               - Define release date ranges if applicable
               - Specify artist popularity considerations""",
            agent=agent,
            expected_output="""A comprehensive search profile including:
            1. List of relevant keywords
            2. Specific musical parameters (BPM range, energy level, etc.)
            3. Mood indicators
            4. Target audience characteristics""",
            context=f"""Use these user parameters as input: {user_params}
            The analysis should be detailed enough to guide precise music selection.""",
            dependencies=["get_user_parameters_task"],
        )

    def search_music_task(self, agent: Agent, search_profile: Dict) -> Task:
        return Task(
            description="""Search for songs matching the specified criteria using music APIs.
            Steps:
            1. Query multiple music platforms with the provided keywords
            2. Collect song metadata and audio features
            3. Create an initial pool of potential songs
            4. Validate each song against the basic criteria""",
            agent=agent,
            expected_output="""A list of potential songs including:
            1. Song title and artist
            2. Audio features and characteristics
            3. URLs or identifiers for downloading
            4. Preliminary matching score""",
            context=f"""Use this search profile for finding songs: {search_profile}
            Aim to find at least 2-3 times more songs than needed for the final playlist.""",
            dependencies=["analyze_parameters_task"],
        )

    def curate_playlist_task(self, agent: Agent, song_pool: List[Dict]) -> Task:
        return Task(
            description="""Create an optimized playlist from the song pool using these criteria:

            Curation Steps:
            1. Individual Song Analysis:
               - Score each song against the target parameters
               - Evaluate lyrical content relevance
               - Assess audio quality and production value
               - Calculate energy and mood alignment

            2. Song Flow Optimization:
               - Create energy progression map
               - Ensure key and tempo transitions
               - Balance variety and consistency
               - Identify and resolve jarring transitions

            3. Playlist Structure:
               - Design opening sequence (first 3 songs)
               - Create emotional peak moments
               - Plan energy dips and recoveries
               - Craft satisfying closure sequence

            4. Quality Control:
               - Verify total duration matches requirement
               - Check genre distribution
               - Validate language mix
               - Ensure mood consistency""",
            agent=agent,
            expected_output="""A curated playlist containing:
            1. Final list of selected songs
            2. Order of songs for optimal flow
            3. Justification for each song's inclusion
            4. Expected playlist duration""",
            context=f"""Use this pool of songs for curation: {song_pool}
            Focus on creating a cohesive listening experience.""",
            dependencies=["search_music_task"],
        )

    def download_songs_task(self, agent: Agent, curated_playlist: List[Dict]) -> Task:
        return Task(
            description="""Download the selected songs from appropriate sources.
            Steps:
            1. Locate each song on YouTube or other platforms
            2. Download high-quality audio versions
            3. Verify audio quality and completeness
            4. Handle any failed downloads""",
            agent=agent,
            expected_output="""A collection of downloaded files including:
            1. Audio files for all songs
            2. Download status report
            3. Any quality issues or concerns
            4. Location of downloaded files""",
            context=f"""Process these songs for download: {curated_playlist}
            Ensure all downloads are high-quality and complete.""",
            dependencies=["curate_playlist_task"],
        )

    def assemble_playlist_task(
        self, agent: Agent, downloaded_songs: List[Dict[str, Any]]
    ) -> Task:
        """
        Creates a task for assembling the final playlist package.

        Args:
            agent: The agent responsible for executing the task
            downloaded_songs: List of downloaded song information

        Returns:
            Task object for playlist assembly
        """

        return Task(
            description="""Organize and prepare the final playlist package.
            Steps:
            1. Organize files in a clear structure
            2. Update metadata for all songs
            3. Create playlist files in various formats
            4. Prepare for delivery to user""",
            agent=agent,
            expected_output="""A complete playlist package including:
            1. Organized music files with correct metadata
            2. Playlist files in multiple formats
            3. Documentation of contents
            4. Download/access instructions""",
            context=f"""Process these downloaded songs: {downloaded_songs}
            Create a user-friendly and well-organized final product.""",
            dependencies=["download_songs_task"],
        )
