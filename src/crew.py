from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task
from langchain_openai import ChatOpenAI

from src.tools.music_analysis_tools import (
    AudioQualityTool,
    BPMDetectionTool,
    GenreConfidenceTool,
)
from src.tools.parameter_tools import (
    GenreExpansionTool,
    PreferenceParserTool,
    SearchWeightsTool,
)
from src.tools.playlist_tools import (
    PlaylistSummaryTool,
    RegionalAvailabilityTool,
)
from src.tools.youtube_tools import (
    PlaylistAddTool,
    PlaylistCreateTool,
    VideoMetadataTool,
    VideoSearchTool,
)


@CrewBase
class PlaiCrew:
    """Plai crew"""

    # LLM ------------------------------------------------------------------------
    @llm
    def llm(self) -> ChatOpenAI:
        return ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0.7)

    # Agents -----------------------------------------------------------------------
    @agent
    def parameter_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["parameter_analysis_agent"],
            llm=self.llm(),
            tools=[
                PreferenceParserTool(),
                SearchWeightsTool(),
                GenreExpansionTool(),
            ],
            max_iter=3,
            verbose=True,
        )

    @agent
    def music_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["music_search_agent"],
            llm=self.llm(),
            tools=[
                VideoSearchTool(),
                VideoMetadataTool(),
            ],
            max_iter=3,
            verbose=True,
        )

    @agent
    def curation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["curation_agent"],
            llm=self.llm(),
            tools=[
                AudioQualityTool(),
                BPMDetectionTool(),
                GenreConfidenceTool(),
            ],
            max_iter=3,
            verbose=True,
        )

    @agent
    def playlist_creation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["playlist_creation_agent"],
            llm=self.llm(),
            tools=[
                VideoSearchTool(),
                PlaylistCreateTool(),
                PlaylistAddTool(),
            ],
            max_iter=3,
            verbose=True,
        )

    @agent
    def delivery_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["delivery_agent"],
            llm=self.llm(),
            tools=[
                PlaylistSummaryTool(),
                RegionalAvailabilityTool(),
            ],
            max_iter=3,
            verbose=True,
        )

    # Tasks ------------------------------------------------------------------------
    @task
    def analyze_user_input_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_user_input_task"],
        )

    @task
    def search_music_task(self) -> Task:
        return Task(
            config=self.tasks_config["search_music_task"],
        )

    @task
    def curate_music_task(self) -> Task:
        return Task(
            config=self.tasks_config["curate_music_task"],
        )

    @task
    def create_playlist_task(self) -> Task:
        return Task(
            config=self.tasks_config["create_playlist_task"],
        )

    @task
    def deliver_playlist_task(self) -> Task:
        return Task(
            config=self.tasks_config["deliver_playlist_task"],
        )

    @task
    def add_videos_task(self) -> Task:
        return Task(
            config=self.tasks_config["add_videos_task"],
        )

    # Crew ------------------------------------------------------------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm=self.llm(),
            verbose=True,
        )
