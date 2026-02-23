# Insurance Multi-Agent System

A modular and extensible multi-agent system built with Python and LangChain.

## 🏗️ Project Structure

```
Insurance-multi-agent/
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # Abstract base class for all agents
│   └── example_agent.py   # Example agent implementation
├── tools/                  # Tools that agents can use
│   ├── __init__.py
│   └── example_tool.py    # Example tools
├── workflows/              # Agent orchestration
│   ├── __init__.py
│   └── orchestrator.py    # Multi-agent workflow orchestrator
├── config/                 # Configuration
│   ├── __init__.py
│   └── settings.py        # Application settings
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── logger.py          # Logging utilities
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_orchestrator.py
├── main.py                 # Application entry point
├── pyproject.toml          # Project dependencies
├── .env.example            # Example environment variables
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or uv package manager

### Installation

1. Clone the repository (if not already done)

2. Install dependencies:
```bash
uv sync
```

Or with pip:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

```bash
python main.py
```

Or with uv:
```bash
uv run python main.py
```

## 📖 Usage

### Creating a New Agent

1. Create a new file in the `agents/` directory
2. Inherit from `BaseAgent`
3. Implement the `execute()` method

```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="My Custom Agent",
            description="Does something specific"
        )
    
    async def execute(self, task: str, context=None):
        # Your agent logic here
        return {"status": "success", "result": "..."}
```

### Creating Tools

Add tools in the `tools/` directory that agents can use:

```python
def my_custom_tool(input_data):
    # Tool logic here
    return {"result": "..."}
```

### Orchestrating Agents

Use the `AgentOrchestrator` to coordinate multiple agents:

```python
from workflows.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()
orchestrator.register_agent(agent1)
orchestrator.register_agent(agent2)

workflow = [
    {"agent_name": "Agent 1", "task": "First task"},
    {"agent_name": "Agent 2", "task": "Second task"}
]

result = await orchestrator.execute_workflow(workflow)
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

Or with uv:
```bash
uv run pytest
```

## 📝 Configuration

Edit `config/settings.py` to customize:
- Default LLM model
- Temperature and token limits
- Timeout settings
- Logging configuration

Use environment variables in `.env` for sensitive data like API keys.

## 🛠️ Development

### Adding Dependencies

With uv:
```bash
uv add package-name
```

With pip:
```bash
pip install package-name
# Then update pyproject.toml
```

### Code Structure Best Practices

- Keep agents focused on single responsibilities
- Use the orchestrator for complex multi-step workflows
- Add tools to extend agent capabilities
- Write tests for new agents and workflows
- Use type hints for better code clarity

## 📚 Next Steps

1. Customize the example agents for your insurance use case
2. Add domain-specific tools (claim processing, risk assessment, etc.)
3. Implement error handling and retry logic
4. Add more sophisticated orchestration patterns
5. Integrate with your data sources and APIs

## 🤝 Contributing

Feel free to extend and customize this structure for your specific needs.

## 📄 License

[Add your license here]