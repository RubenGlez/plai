from typing import List, Type

from crewai_tools import BaseTool
from pydantic import BaseModel, Field


class TransitionAnalysisInput(BaseModel):
    """Input schema for transition analysis."""

    track_list: List[dict] = Field(
        ..., description="List of tracks to analyze for transitions compatibility"
    )


class RegionalAvailabilityInput(BaseModel):
    """Input schema for regional availability check."""

    video_ids: List[str] = Field(
        ..., description="List of video IDs to check for regional availability"
    )
    region_code: str = Field(
        ..., description="Region code to check availability against"
    )


class PlaylistSummaryInput(BaseModel):
    """Input schema for playlist summary generation."""

    playlist_data: dict = Field(
        ..., description="Complete playlist data including track metadata"
    )


class TransitionAnalysisTool(BaseTool):
    name: str = "Transition Analyzer"
    description: str = (
        "Analyzes adjacent tracks in a playlist for compatibility based on "
        "key compatibility, BPM matching, and energy level transitions."
    )
    args_schema: Type[BaseModel] = TransitionAnalysisInput

    def _run(self, track_list: List[dict]) -> List[dict]:
        """
        Analyze adjacent tracks for:
        - Key compatibility
        - BPM matching
        - Energy level transitions
        """
        # Implementation goes here
        pass


class RegionalAvailabilityTool(BaseTool):
    name: str = "Regional Availability Checker"
    description: str = (
        "Verifies if videos in a playlist are available in the user's region "
        "to prevent regional licensing issues."
    )
    args_schema: Type[BaseModel] = RegionalAvailabilityInput

    def _run(self, video_ids: List[str], region_code: str) -> dict:
        """Verify if videos are available in user's region"""
        # Implementation goes here
        pass


class PlaylistSummaryTool(BaseTool):
    name: str = "Playlist Summarizer"
    description: str = (
        "Generates a comprehensive summary of a playlist including genre distribution, "
        "tempo range, era spread, language breakdown, and total duration."
    )
    args_schema: Type[BaseModel] = PlaylistSummaryInput

    def _run(self, playlist_data: dict) -> dict:
        """
        Create a summary including:
        - Genre distribution
        - Tempo range
        - Era spread
        - Language breakdown
        - Total duration
        """
        # Implementation goes here
        pass
