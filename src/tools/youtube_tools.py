import os
import pickle
from typing import List, Type

from crewai_tools import BaseTool
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
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


class YouTubeBaseTool(BaseTool):
    """Base class for YouTube tools with authentication handling"""

    def _get_youtube_service(self):
        """Gets authenticated YouTube service."""
        creds = None
        # Token file stores the user's access and refresh tokens
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        # If there are no valid credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secrets.json",
                    ["https://www.googleapis.com/auth/youtube.force-ssl"],
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        # Build and return the YouTube service
        return build("youtube", "v3", credentials=creds)


class VideoSearchTool(YouTubeBaseTool):
    name: str = "Search YouTube Videos"
    description: str = "Search for videos on YouTube based on query and filters"
    args_schema: Type[BaseModel] = VideoSearchInput

    def _run(self, query: str, filters: dict) -> dict:
        try:
            youtube = self._get_youtube_service()

            # Construir los parámetros de búsqueda
            search_params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": 10,  # Ajusta según necesites
                "videoCategoryId": "10",  # ID para música
            }

            # Aplicar filtros adicionales si existen
            if "language" in filters:
                search_params["relevanceLanguage"] = filters["language"]

            # Realizar la búsqueda
            search_response = youtube.search().list(**search_params).execute()

            # Procesar resultados
            videos = []
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                videos.append(
                    {
                        "video_id": video_id,
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                    }
                )

            return {
                "status": "success",
                "video_ids": [v["video_id"] for v in videos],
                "videos": videos,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}


class PlaylistCreateTool(YouTubeBaseTool):
    name: str = "Create YouTube Playlist"
    description: str = (
        "Creates a new YouTube playlist with the specified title and description"
    )
    args_schema: Type[BaseModel] = PlaylistCreateInput

    def _run(
        self,
        title: str,
        description: str,
        privacy_status: str = "private",
        channel_id: str = None,
    ) -> dict:
        try:
            youtube = self._get_youtube_service()

            # Si no se proporciona channel_id, obtener lista de canales
            if not channel_id:
                channels = youtube.channels().list(part="snippet", mine=True).execute()

                if not channels["items"]:
                    return {"status": "error", "message": "No channels found"}

                # Usar el primer canal por defecto
                channel_id = channels["items"][0]["id"]

            playlist_insert_response = (
                youtube.playlists()
                .insert(
                    part="snippet,status",
                    body={
                        "snippet": {
                            "title": title,
                            "description": description,
                            "channelId": channel_id,
                        },
                        "status": {"privacyStatus": privacy_status},
                    },
                )
                .execute()
            )

            return {
                "playlist_id": playlist_insert_response["id"],
                "channel_id": channel_id,
                "url": f"https://www.youtube.com/playlist?list={playlist_insert_response['id']}",
                "status": "success",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


class PlaylistAddTool(YouTubeBaseTool):
    name: str = "Add Videos to Playlist"
    description: str = "Add videos to an existing YouTube playlist"
    args_schema: Type[BaseModel] = PlaylistAddInput

    def _run(self, playlist_id: str, video_ids: List[str]) -> dict:
        try:
            youtube = self._get_youtube_service()
            results = []

            # Añadir logging para debug
            print(f"Adding videos to playlist {playlist_id}")
            print(f"Video IDs to add: {video_ids}")

            for video_id in video_ids:
                try:
                    response = (
                        youtube.playlistItems()
                        .insert(
                            part="snippet",
                            body={
                                "snippet": {
                                    "playlistId": playlist_id,
                                    "resourceId": {
                                        "kind": "youtube#video",
                                        "videoId": video_id,
                                    },
                                }
                            },
                        )
                        .execute()
                    )
                    results.append(response)
                    print(f"Successfully added video {video_id}")
                except Exception as e:
                    print(f"Error adding video {video_id}: {str(e)}")

            return {
                "status": "success",
                "added_videos": len(results),
                "playlist_id": playlist_id,
                "failed_videos": len(video_ids) - len(results),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


class VideoMetadataTool(YouTubeBaseTool):
    name: str = "Video Metadata Fetcher"
    description: str = (
        "Fetches detailed video metadata including duration, view count, "
        "like ratio, comments sentiment, language, and content rating."
    )
    args_schema: Type[BaseModel] = VideoMetadataInput

    def _run(self, video_id: str) -> dict:
        youtube = self._get_youtube_service()

        try:
            video_response = (
                youtube.videos()
                .list(part="snippet,contentDetails,statistics", id=video_id)
                .execute()
            )

            if not video_response["items"]:
                raise Exception(f"Video {video_id} not found")

            video = video_response["items"][0]
            return {
                "title": video["snippet"]["title"],
                "description": video["snippet"]["description"],
                "duration": video["contentDetails"]["duration"],
                "viewCount": video["statistics"].get("viewCount", 0),
                "likeCount": video["statistics"].get("likeCount", 0),
                "commentCount": video["statistics"].get("commentCount", 0),
                "language": video["snippet"].get("defaultLanguage", "unknown"),
                "tags": video["snippet"].get("tags", []),
                "publishedAt": video["snippet"]["publishedAt"],
            }
        except HttpError as e:
            raise Exception(f"Failed to fetch video metadata: {str(e)}")
