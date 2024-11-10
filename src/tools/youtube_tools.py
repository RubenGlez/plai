from typing import List, Type

from crewai_tools import BaseTool
from pydantic import BaseModel, Field


class VideoSearchInput(BaseModel):
    """Input schema for video search."""

    query: str = Field(..., description="Search query string")
    filters: dict = Field(
        ...,
        description="Dictionary of filters including language, content rating, duration, and view count thresholds",
    )


class PlaylistCreateInput(BaseModel):
    """Input schema for playlist creation."""

    title: str = Field(..., description="Title for the new playlist")
    description: str = Field(..., description="Description for the new playlist")
    privacy_status: str = Field(
        ...,
        description="Privacy status for the playlist (public, private, or unlisted)",
    )


class PlaylistAddInput(BaseModel):
    """Input schema for adding videos to playlist."""

    playlist_id: str = Field(..., description="ID of the target playlist")
    video_ids: List[str] = Field(
        ..., description="List of video IDs to add to the playlist"
    )


class VideoMetadataInput(BaseModel):
    """Input schema for video metadata retrieval."""

    video_id: str = Field(..., description="ID of the video to fetch metadata for")


class VideoSearchTool(BaseTool):
    name: str = "YouTube Video Search"
    description: str = (
        "Search YouTube videos with advanced filtering options including language, "
        "content rating, duration, and view count thresholds."
    )
    args_schema: Type[BaseModel] = VideoSearchInput

    def _run(self, query: str, filters: dict) -> List[dict]:
        # Implementation goes here
        pass


class PlaylistCreateTool(BaseTool):
    name: str = "YouTube Playlist Creator"
    description: str = (
        "Creates a new YouTube playlist with specified title, description, "
        "and privacy settings."
    )
    args_schema: Type[BaseModel] = PlaylistCreateInput

    def _run(self, title: str, description: str, privacy_status: str) -> str:
        # Implementation goes here
        pass


class PlaylistAddTool(BaseTool):
    name: str = "Playlist Video Adder"
    description: str = "Adds multiple videos to an existing YouTube playlist."
    args_schema: Type[BaseModel] = PlaylistAddInput

    def _run(self, playlist_id: str, video_ids: List[str]) -> bool:
        # Implementation goes here
        pass


class VideoMetadataTool(BaseTool):
    name: str = "Video Metadata Fetcher"
    description: str = (
        "Fetches detailed video metadata including duration, view count, "
        "like ratio, comments sentiment, language, and content rating."
    )
    args_schema: Type[BaseModel] = VideoMetadataInput

    def _run(self, video_id: str) -> dict:
        # Implementation goes here
        pass
