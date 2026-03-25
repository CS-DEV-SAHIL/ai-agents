from blogdon.crew import Blogdon
from datetime import datetime

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'keywords': ['AI', 'LLMs', 'AI LLMs'],
        'current_year': str(datetime.now().year)
    }

    try:
        Blogdon().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
