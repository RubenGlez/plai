from typing import List, Type

from crewai_tools import BaseTool
from pydantic import BaseModel, Field


class UserPreferencesInput(BaseModel):
    """Input schema for parsing user music preferences."""

    user_input: str = Field(
        ..., description="Natural language input containing user's music preferences"
    )


class SearchWeightsInput(BaseModel):
    """Input schema for generating search weights."""

    parameters: dict = Field(
        ..., description="Dictionary of parsed user preferences to weight"
    )


class GenreExpansionInput(BaseModel):
    """Input schema for genre expansion."""

    genre: str = Field(
        ..., description="Primary genre to expand into related subgenres"
    )


class PreferenceParserTool(BaseTool):
    name: str = "Preference Parser"
    description: str = (
        "Extracts structured parameters from natural language input including "
        "mood keywords, genre/subgenre, temporal preferences, artist preferences, "
        "and explicit content preferences."
    )
    args_schema: Type[BaseModel] = UserPreferencesInput

    def _run(self, user_input: str) -> dict:
        """
        Parse natural language input into structured parameters.
        Returns a dictionary of parsed preferences.
        """
        parsed_params = {
            "genre": [],
            "subgenre": [],
            "mood": [],
            "tempo_range": {"min": None, "max": None},
            "explicit_content": None,
            "languages": [],
            "duration": None,
            "target_audience": None,
        }

        # Convert input to lowercase for easier matching
        input_lower = user_input.lower()

        # Define common keywords for each category
        mood_keywords = {
            "happy": ["happy", "upbeat", "cheerful", "joyful", "energetic"],
            "sad": ["sad", "melancholic", "gloomy", "depressing"],
            "calm": ["calm", "peaceful", "relaxing", "chill", "mellow"],
            "angry": ["angry", "aggressive", "intense", "powerful"],
            "romantic": ["romantic", "love", "passionate", "sensual"],
        }

        # Common genres (using existing mapping from GenreExpansionTool)
        common_genres = [
            "rock",
            "pop",
            "hip hop",
            "electronic",
            "country",
            "latin",
            "jazz",
            "classical",
            "blues",
            "folk",
            "metal",
            "reggae",
            "punk",
            "r&b",
            "k-pop",
            "indie",
        ]

        # Parse genres
        for genre in common_genres:
            if genre in input_lower:
                parsed_params["genre"].append(genre)

        # Parse moods
        for mood, keywords in mood_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                parsed_params["mood"].append(mood)

        # Parse tempo preferences
        tempo_indicators = {
            "fast": {"min": 120, "max": None},
            "slow": {"min": None, "max": 80},
            "moderate": {"min": 80, "max": 120},
        }
        for tempo, range_values in tempo_indicators.items():
            if tempo in input_lower:
                parsed_params["tempo_range"] = range_values

        # Parse explicit content preferences
        if "clean" in input_lower or "family friendly" in input_lower:
            parsed_params["explicit_content"] = False
        elif "explicit" in input_lower:
            parsed_params["explicit_content"] = True

        # Parse languages
        common_languages = {
            "english": ["english", "eng"],
            "spanish": ["spanish", "español", "espanol"],
            "korean": ["korean", "k-pop"],
            "japanese": ["japanese", "j-pop"],
            "french": ["french", "français", "francais"],
        }
        for lang, keywords in common_languages.items():
            if any(keyword in input_lower for keyword in keywords):
                parsed_params["languages"].append(lang)

        # Parse duration preferences
        duration_keywords = {"short": "short", "long": "long", "medium": "medium"}
        for duration in duration_keywords:
            if duration in input_lower:
                parsed_params["duration"] = duration

        # Parse target audience
        audience_keywords = {
            "children": ["kids", "children", "family"],
            "teens": ["teenage", "teens", "adolescent"],
            "adults": ["adult", "mature"],
            "everyone": ["everyone", "all ages"],
        }
        for audience, keywords in audience_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                parsed_params["target_audience"] = audience

        return parsed_params


class SearchWeightsTool(BaseTool):
    name: str = "Search Weights Generator"
    description: str = (
        "Calculates relative importance weights for different search criteria "
        "based on parsed user preferences."
    )
    args_schema: Type[BaseModel] = SearchWeightsInput

    def _run(self, parameters: dict) -> dict:
        """
        Generate weights for search parameters based on their importance.
        Returns a dictionary of parameter weights.
        """
        # Initialize base weights
        weights = {
            "genre_weight": 1.0,
            "mood_weight": 0.8,
            "tempo_weight": 0.6,
            "language_weight": 0.7,
            "popularity_weight": 0.5,
            "explicit_weight": 0.9,
            "duration_weight": 0.4,
            "target_audience_weight": 0.8,
        }

        # Adjust weights based on which parameters are specified
        if parameters.get("genre"):
            weights["genre_weight"] = 1.0 + (0.1 * len(parameters["genre"]))

        if parameters.get("mood"):
            weights["mood_weight"] = 0.9 + (0.1 * len(parameters["mood"]))

        if parameters.get("tempo_range", {}).get("min") or parameters.get(
            "tempo_range", {}
        ).get("max"):
            weights["tempo_weight"] = 0.8

        if parameters.get("languages"):
            weights["language_weight"] = 0.9 + (0.1 * len(parameters["languages"]))

        if parameters.get("explicit_content") is not None:
            weights["explicit_weight"] = 1.0

        if parameters.get("duration"):
            weights["duration_weight"] = 0.6

        if parameters.get("target_audience"):
            weights["target_audience_weight"] = 0.9

        # Normalize weights to sum to 1.0
        total_weight = sum(weights.values())
        normalized_weights = {k: v / total_weight for k, v in weights.items()}

        return normalized_weights


class GenreExpansionTool(BaseTool):
    name: str = "Genre Expander"
    description: str = (
        "Generates a list of related subgenres and alternative names "
        "for a given music genre."
    )
    args_schema: Type[BaseModel] = GenreExpansionInput

    def _run(self, genre: str) -> List[str]:
        """
        Expand a genre into related subgenres and alternative names.
        Returns a list of related genres and subgenres.
        """
        # Enhanced genre mappings with more subgenres and cross-genre fusions
        genre_mappings = {
            "rock": [
                "alternative rock",
                "indie rock",
                "classic rock",
                "hard rock",
                "progressive rock",
                "psychedelic rock",
                "garage rock",
                "blues rock",
                "folk rock",
                "punk rock",
                "metal",
            ],
            "pop": [
                "pop rock",
                "synth pop",
                "indie pop",
                "dance pop",
                "electropop",
                "art pop",
                "chamber pop",
                "baroque pop",
                "dream pop",
                "k-pop",
            ],
            "hip hop": [
                "rap",
                "trap",
                "conscious hip hop",
                "boom bap",
                "southern hip hop",
                "alternative hip hop",
                "experimental hip hop",
                "jazz rap",
                "pop rap",
                "gangsta rap",
            ],
            "electronic": [
                "house",
                "techno",
                "trance",
                "dubstep",
                "drum and bass",
                "ambient",
                "electronica",
                "IDM",
                "synthwave",
                "industrial",
            ],
            "country": [
                "country pop",
                "country rock",
                "country rap",
                "bluegrass",
                "americana",
                "country folk",
                "country blues",
                "nashville sound",
                "outlaw country",
                "contemporary country",
            ],
            "latin": [
                "latin pop",
                "latin rock",
                "latin hip hop",
                "reggaeton",
                "salsa",
                "bachata",
                "merengue",
                "latin jazz",
                "latin trap",
                "cumbia",
            ],
            "jazz": [
                "jazz fusion",
                "smooth jazz",
                "bebop",
                "jazz rap",
                "modal jazz",
                "free jazz",
                "cool jazz",
                "hard bop",
                "swing",
                "contemporary jazz",
            ],
            "classical": [
                "baroque",
                "romantic",
                "modern classical",
                "contemporary classical",
                "minimalist",
                "orchestral",
                "chamber music",
                "opera",
                "neoclassical",
                "avant-garde classical",
            ],
            # ... existing mappings for other genres ...
        }

        # Handle case-insensitive matching
        genre_lower = genre.lower()

        # Direct match
        if genre_lower in genre_mappings:
            return genre_mappings[genre_lower]

        # Partial match (if genre contains spaces or hyphens)
        for main_genre, subgenres in genre_mappings.items():
            if genre_lower in main_genre or main_genre in genre_lower:
                return subgenres
            # Check if it's already a subgenre
            if any(genre_lower in subgenre for subgenre in subgenres):
                return [sg for sg in subgenres if genre_lower in sg]

        # If no match found, return the original genre
        return [genre]
