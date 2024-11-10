#!/usr/bin/env python
import sys

from src.crew import PlaiCrew

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew with ChatGPT as the manager.
    """
    inputs = {
        "genre": "Hip-Hop",
        "subgenre": "Trap",
        "duration": 60,
        "target_audience": "Young Adults",
        "mood": "Energetic",
        "additional_requirements": {
            "preferences": "No slow tracks",
            "tempo_range": {"min": 90, "max": 150},
            "explicit_content": "Yes",
            "languages": ["English", "Spanish"],
        },
    }
    PlaiCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "genre": "Hip-Hop",
        "subgenre": "Trap",
        "duration": 60,
        "target_audience": "Young Adults",
        "mood": "Energetic",
        "additional_requirements": {
            "preferences": "No slow tracks",
            "tempo_range": {"min": 90, "max": 150},
            "explicit_content": "Yes",
            "languages": ["English", "Spanish"],
        },
    }
    try:
        PlaiCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        PlaiCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "genre": "Hip-Hop",
        "subgenre": "Trap",
        "duration": 60,
        "target_audience": "Young Adults",
        "mood": "Energetic",
        "additional_requirements": {
            "preferences": "No slow tracks",
            "tempo_range": {"min": 90, "max": 150},
            "explicit_content": "Yes",
            "languages": ["English", "Spanish"],
        },
    }
    try:
        PlaiCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
