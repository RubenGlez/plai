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
        # Implementation goes here
        pass


class SearchWeightsTool(BaseTool):
    name: str = "Search Weights Generator"
    description: str = (
        "Calculates relative importance weights for different search criteria "
        "based on parsed user preferences."
    )
    args_schema: Type[BaseModel] = SearchWeightsInput

    def _run(self, parameters: dict) -> dict:
        # Implementation goes here
        pass


class GenreExpansionTool(BaseTool):
    name: str = "Genre Expander"
    description: str = (
        "Generates a list of related subgenres and alternative names "
        "for a given music genre."
    )
    args_schema: Type[BaseModel] = GenreExpansionInput

    def _run(self, genre: str) -> List[str]:
        # Implementation goes here
        pass
