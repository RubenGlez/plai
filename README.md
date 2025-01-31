# Plai

Welcome to Plai Crew, an intelligent YouTube playlist generation system powered by [crewAI](https://crewai.com). This project leverages multiple AI agents working in collaboration to create personalized YouTube playlists based on sophisticated music preferences and criteria.

## Features

- **Multi-Agent System**: Utilizes specialized AI agents for different aspects of playlist creation:
  - Parameter Analysis Agent: Interprets user preferences
  - Music Search Agent: Executes YouTube searches
  - Curation Agent: Evaluates and selects tracks
  - Playlist Creation Agent: Manages playlist organization
  - Delivery Agent: Ensures quality and accessibility

- **Advanced Music Analysis**:
  - BPM (tempo) detection
  - Genre confidence scoring
  - Audio quality analysis
  - Regional availability checking
  - Transition compatibility analysis

- **Smart Parameter Processing**:
  - Natural language preference parsing
  - Genre expansion and subgenre mapping
  - Intelligent search weight generation
  - Multi-language support
  - Content rating management

## Prerequisites

- Python >=3.10 <=3.13
- YouTube API credentials (`client_secrets.json`)
- OpenAI API key
- [UV](https://docs.astral.sh/uv/) package manager

## Installation

1. Install UV if you haven't already:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```


## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the ai-test Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Advanced Usage

- **Training Mode**: Train the AI crew for improved performance

```bash
crewai train <iterations> <filename>
```

- **Replay Mode**: Replay specific task executions
```bash
crewai replay <task_id>
```

- **Test Mode**: Run test iterations with specific models
```bash
crewai test <iterations> <model_name>
```

## Project Structure

- `src/`
  - `config/`: Agent and task configurations
  - `tools/`: Specialized tools for music analysis and playlist management
  - `crew.py`: Core crew implementation and agent definitions
  - `main.py`: Entry points and execution handlers

## Dependencies

- crewAI: Multi-agent system framework
- Google API Client: YouTube integration
- librosa: Audio analysis
- langchain-openai: LLM integration
- Additional utilities for authentication and file handling

## Security Notes

- Sensitive credentials are stored in `.env` and `client_secrets.json`
- OAuth tokens are cached in `token.pickle`
- All sensitive files are excluded from version control

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions to Plai Crew! 

