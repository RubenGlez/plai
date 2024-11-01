from typing import List, Optional, TypedDict


class TempoRange(TypedDict):
    min: int
    max: int


class AdvancedOptions(TypedDict, total=False):
    tempo_range: TempoRange
    explicit_content: str
    languages: List[str]


class AdditionalRequirements(TypedDict, total=False):
    preferences: Optional[str]
    tempo_range: TempoRange
    explicit_content: str
    languages: List[str]


class PlaylistParams(TypedDict, total=False):
    genre: str
    subgenre: Optional[str]
    duration: int
    target_audience: str
    mood: str
    additional_requirements: AdditionalRequirements
