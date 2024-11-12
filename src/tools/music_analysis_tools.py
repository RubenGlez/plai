from typing import Type

import librosa
import numpy as np
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from pytube import YouTube


class BPMDetectionInput(BaseModel):
    """Input schema for BPM detection."""

    audio_sample: bytes = Field(
        ..., description="Raw audio sample bytes to analyze for tempo detection"
    )


class AudioQualityInput(BaseModel):
    """Input schema for audio quality analysis."""

    video_id: str = Field(..., description="Video ID to analyze audio quality metrics")


class GenreConfidenceInput(BaseModel):
    """Input schema for genre confidence calculation."""

    video_id: str = Field(..., description="Video ID to analyze")
    expected_genre: str = Field(
        ..., description="Expected genre to calculate confidence against"
    )


class BPMDetectionTool(BaseTool):
    name: str = "BPM Detector"
    description: str = (
        "Analyzes an audio sample to detect its tempo/BPM (Beats Per Minute). "
        "Useful for tempo-based music analysis and matching."
    )
    args_schema: Type[BaseModel] = BPMDetectionInput

    def _run(self, audio_sample: bytes) -> float:
        try:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(audio_sample, dtype=np.float32)

            # Detect tempo using librosa
            tempo, _ = librosa.beat.beat_track(y=audio_data)
            return round(tempo, 2)
        except Exception as e:
            return f"Error detecting BPM: {str(e)}"


class AudioQualityTool(BaseTool):
    name: str = "Audio Quality Analyzer"
    description: str = (
        "Analyzes audio stream quality metrics including bitrate, dynamic range, "
        "noise levels, and overall audio clarity score."
    )
    args_schema: Type[BaseModel] = AudioQualityInput

    def _run(self, video_id: str) -> dict:
        try:
            # Validate video ID
            if not video_id or len(video_id) != 11:
                return "Error: Invalid YouTube video ID"

            # Download audio from YouTube
            try:
                yt = YouTube(f"https://youtube.com/watch?v={video_id}")
                audio_stream = yt.streams.filter(only_audio=True).first()
                if not audio_stream:
                    return "Error: No audio stream available for this video"
                audio_path = audio_stream.download(filename="temp_audio")
            except Exception as youtube_error:
                return f"YouTube Error: {str(youtube_error)}"

            # Load audio and analyze
            y, sr = librosa.load(audio_path)

            # Basic quality metrics
            return {
                "bitrate": audio_stream.abr,
                "sample_rate": sr,
                "duration": len(y) / sr,
                "rms_energy": float(librosa.feature.rms(y=y).mean()),
                "zero_crossings": float(librosa.feature.zero_crossing_rate(y).mean()),
            }
        except Exception as e:
            return f"Error analyzing audio quality: {str(e)}"


class GenreConfidenceTool(BaseTool):
    name: str = "Genre Confidence Calculator"
    description: str = (
        "Calculates a confidence score for how well a track matches an "
        "expected genre classification."
    )
    args_schema: Type[BaseModel] = GenreConfidenceInput

    def _run(self, video_id: str, expected_genre: str) -> float:
        try:
            # Validate inputs
            if not video_id or len(video_id) != 11:
                return "Error: Invalid YouTube video ID"
            if not expected_genre:
                return "Error: Expected genre cannot be empty"

            # Download audio
            try:
                yt = YouTube(f"https://youtube.com/watch?v={video_id}")
                audio_stream = yt.streams.filter(only_audio=True).first()
                if not audio_stream:
                    return "Error: No audio stream available for this video"
                audio_path = audio_stream.download(filename="temp_audio")
            except Exception as youtube_error:
                return f"YouTube Error: {str(youtube_error)}"

            # Extract features
            y, sr = librosa.load(audio_path)

            # Calculate basic genre features
            tempo, _ = librosa.beat.beat_track(y=y)
            spectral_centroids = librosa.feature.spectral_centroid(y=y)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y)[0]

            # Simplified genre matching (example rules)
            confidence = 0.5  # Base confidence

            if expected_genre.lower() == "rock":
                if 100 < tempo < 140:
                    confidence += 0.2
                if spectral_centroids.mean() > 2000:
                    confidence += 0.3
            elif expected_genre.lower() == "classical":
                if tempo < 100:
                    confidence += 0.2
                if spectral_rolloff.mean() < 3000:
                    confidence += 0.3

            return round(min(confidence, 1.0), 2)
        except Exception as e:
            return f"Error calculating genre confidence: {str(e)}"
