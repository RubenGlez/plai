from crewai import Crew

from agents import PlaiAgents
from playlist_params import PlaylistParams
from tasks import PlaiTasks


class PlaiCrew:
    def __init__(self, playlist_params: PlaylistParams):
        self.playlist_params = playlist_params

    def run(self):
        agents = PlaiAgents()
        tasks = PlaiTasks()

        # Agents
        playlist_coordinator = agents.playlist_coordinator()
        parameter_analysis_agent = agents.parameter_analysis_agent()
        music_search_agent = agents.music_search_agent()
        curation_agent = agents.curation_agent()
        download_agent = agents.download_agent()

        # Tasks
        get_user_parameters_task = tasks.get_user_parameters_task(
            playlist_coordinator, self.playlist_params
        )

        analyze_parameters_task = tasks.analyze_parameters_task(
            parameter_analysis_agent,
            {},  # This will be populated with the output from get_user_parameters_task
        )

        search_music_task = tasks.search_music_task(
            music_search_agent,
            {},  # This will be populated with the output from analyze_parameters_task
        )

        curate_playlist_task = tasks.curate_playlist_task(
            curation_agent,
            [],  # This will be populated with the output from search_music_task
        )

        download_songs_task = tasks.download_songs_task(
            download_agent,
            [],  # This will be populated with the output from curate_playlist_task
        )

        assemble_playlist_task = tasks.assemble_playlist_task(
            playlist_coordinator,
            [],  # This will be populated with the output from download_songs_task
        )

        # Define the crew with proper task sequencing
        crew = Crew(
            agents=[
                playlist_coordinator,
                parameter_analysis_agent,
                music_search_agent,
                curation_agent,
                download_agent,
            ],
            tasks=[
                get_user_parameters_task,
                analyze_parameters_task,
                search_music_task,  # Added the missing task
                curate_playlist_task,
                download_songs_task,
                assemble_playlist_task,
            ],
            manager_agent=playlist_coordinator,
        )

        return crew
