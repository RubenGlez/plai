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
        """Analyze transitions between adjacent tracks."""
        transitions = []

        for i in range(len(track_list) - 1):
            current_track = track_list[i]
            next_track = track_list[i + 1]

            # Calculate compatibility scores
            key_score = self._calculate_key_compatibility(
                current_track.get("key", ""), next_track.get("key", "")
            )

            bpm_score = self._calculate_bpm_compatibility(
                current_track.get("bpm", 0), next_track.get("bpm", 0)
            )

            energy_score = self._calculate_energy_transition(
                current_track.get("energy", 0), next_track.get("energy", 0)
            )

            transitions.append(
                {
                    "track_pair": [current_track["title"], next_track["title"]],
                    "key_compatibility": key_score,
                    "bpm_compatibility": bpm_score,
                    "energy_transition": energy_score,
                    "overall_score": (key_score + bpm_score + energy_score) / 3,
                    "suggestions": self._generate_transition_suggestions(
                        key_score, bpm_score, energy_score
                    ),
                }
            )

        return transitions

    def _calculate_key_compatibility(self, key1: str, key2: str) -> float:
        # Camelot wheel compatibility scoring
        # Simplified version - could be expanded with full Camelot wheel logic
        if not key1 or not key2:
            return 0.5  # Neutral score if keys are unknown

        return 1.0 if key1 == key2 else 0.7  # Perfect match or adjacent keys

    def _calculate_bpm_compatibility(self, bpm1: float, bpm2: float) -> float:
        if not bpm1 or not bpm2:
            return 0.5  # Neutral score if BPM unknown

        bpm_diff = abs(bpm1 - bpm2)
        if bpm_diff <= 5:
            return 1.0
        elif bpm_diff <= 10:
            return 0.8
        elif bpm_diff <= 20:
            return 0.6
        else:
            return 0.4

    def _calculate_energy_transition(self, energy1: float, energy2: float) -> float:
        if not energy1 or not energy2:
            return 0.5  # Neutral score if energy levels unknown

        energy_diff = abs(energy1 - energy2)
        return 1.0 - (energy_diff / 2)  # Smooth transitions preferred

    def _generate_transition_suggestions(
        self, key_score: float, bpm_score: float, energy_score: float
    ) -> List[str]:
        suggestions = []

        if key_score < 0.7:
            suggestions.append("Consider harmonic mixing or key adjustment")
        if bpm_score < 0.6:
            suggestions.append(
                "Large BPM difference - consider tempo transition or alternative track"
            )
        if energy_score < 0.5:
            suggestions.append(
                "Sharp energy level change - consider adding intermediate track"
            )

        return suggestions if suggestions else ["Good transition"]


class RegionalAvailabilityTool(BaseTool):
    name: str = "Regional Availability Checker"
    description: str = (
        "Verifies if videos in a playlist are available in the user's region "
        "to prevent regional licensing issues."
    )
    args_schema: Type[BaseModel] = RegionalAvailabilityInput

    def _run(self, video_ids: List[str], region_code: str) -> dict:
        """Check regional availability of videos."""
        import os

        from googleapiclient.discovery import build

        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        results = {"available": [], "unavailable": [], "restricted": []}

        try:
            # Check videos in batches of 50 (API limit)
            for i in range(0, len(video_ids), 50):
                batch = video_ids[i : i + 50]
                response = (
                    youtube.videos()
                    .list(part="contentDetails,status", id=",".join(batch))
                    .execute()
                )

                for video in response["items"]:
                    video_id = video["id"]

                    # Check if video is blocked in the region
                    region_restriction = video["contentDetails"].get(
                        "regionRestriction", {}
                    )
                    allowed = region_restriction.get("allowed", [])
                    blocked = region_restriction.get("blocked", [])

                    if blocked and region_code in blocked:
                        results["unavailable"].append(video_id)
                    elif allowed and region_code not in allowed:
                        results["restricted"].append(video_id)
                    else:
                        results["available"].append(video_id)

        except Exception as e:
            raise Exception(f"Failed to check regional availability: {str(e)}")

        return results


class PlaylistSummaryTool(BaseTool):
    name: str = "Playlist Summarizer"
    description: str = (
        "Generates a comprehensive summary of a playlist including genre distribution, "
        "tempo range, era spread, language breakdown, and total duration."
    )
    args_schema: Type[BaseModel] = PlaylistSummaryInput

    def _run(self, playlist_data: dict) -> dict:
        """Generate comprehensive playlist summary."""
        tracks = playlist_data.get("tracks", [])

        summary = {
            "total_tracks": len(tracks),
            "total_duration": self._calculate_total_duration(tracks),
            "genre_distribution": self._analyze_genre_distribution(tracks),
            "tempo_analysis": self._analyze_tempo(tracks),
            "era_distribution": self._analyze_eras(tracks),
            "language_breakdown": self._analyze_languages(tracks),
            "mood_analysis": self._analyze_mood(tracks),
        }

        return summary

    def _calculate_total_duration(self, tracks: List[dict]) -> str:
        total_seconds = sum(track.get("duration_seconds", 0) for track in tracks)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    def _analyze_genre_distribution(self, tracks: List[dict]) -> dict:
        genres = {}
        for track in tracks:
            for genre in track.get("genres", ["Unknown"]):
                genres[genre] = genres.get(genre, 0) + 1

        # Convert to percentages
        total = len(tracks)
        return {genre: (count / total) * 100 for genre, count in genres.items()}

    def _analyze_tempo(self, tracks: List[dict]) -> dict:
        bpms = [track.get("bpm", 0) for track in tracks if track.get("bpm", 0) > 0]
        if not bpms:
            return {"min_bpm": 0, "max_bpm": 0, "avg_bpm": 0}

        return {
            "min_bpm": min(bpms),
            "max_bpm": max(bpms),
            "avg_bpm": sum(bpms) / len(bpms),
        }

    def _analyze_eras(self, tracks: List[dict]) -> dict:
        eras = {}
        for track in tracks:
            year = track.get("year", "Unknown")
            decade = f"{str(year)[:3]}0s" if isinstance(year, int) else "Unknown"
            eras[decade] = eras.get(decade, 0) + 1

        return eras

    def _analyze_languages(self, tracks: List[dict]) -> dict:
        languages = {}
        for track in tracks:
            lang = track.get("language", "Unknown")
            languages[lang] = languages.get(lang, 0) + 1

        return languages

    def _analyze_mood(self, tracks: List[dict]) -> dict:
        total_energy = sum(track.get("energy", 0) for track in tracks)
        avg_energy = total_energy / len(tracks) if tracks else 0

        moods = {
            "high_energy": len([t for t in tracks if t.get("energy", 0) > 0.7]),
            "medium_energy": len(
                [t for t in tracks if 0.3 <= t.get("energy", 0) <= 0.7]
            ),
            "low_energy": len([t for t in tracks if t.get("energy", 0) < 0.3]),
            "average_energy": avg_energy,
        }

        return moods
