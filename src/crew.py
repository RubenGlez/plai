from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task
from langchain_openai import ChatOpenAI


@CrewBase
class PlaiCrew:
    """Plai crew"""

    # LLM ------------------------------------------------------------------------
    @llm
    def llm(self) -> ChatOpenAI:
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # Agents -----------------------------------------------------------------------
    @agent
    def parameter_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["parameter_analysis_agent"],
            verbose=True,
            llm=self.llm(),
        )

    @agent
    def music_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["music_search_agent"],
            verbose=True,
            llm=self.llm(),
        )

    @agent
    def curation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["curation_agent"],
            verbose=True,
            llm=self.llm(),
        )

    @agent
    def playlist_creation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["playlist_creation_agent"],
            verbose=True,
            llm=self.llm(),
        )

    @agent
    def delivery_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["delivery_agent"],
            verbose=True,
            llm=self.llm(),
        )

    # Tasks ------------------------------------------------------------------------
    @task
    def analyze_user_input_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_user_input_task"],
        )

    @task
    def search_for_music_task(self) -> Task:
        return Task(
            config=self.tasks_config["search_for_music_task"],
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
