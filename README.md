# Insurance Multi-Agent System

An intelligent multi-agent system for automated insurance document processing using LangGraph and LangChain. The system extracts structured data from insurance PDFs, identifies potential risks, and generates comprehensive summaries.

## 🎯 Features

- **OCR-based Text Extraction**: Extracts text from scanned insurance documents using PyMuPDF and Tesseract
- **Entity Extraction**: Automatically identifies key insurance information (policy numbers, coverage amounts, dates, etc.)
- **Risk Analysis**: Detects missing information, inconsistencies, unusual clauses, and fraud indicators
- **Summary Generation**: Creates human-readable summaries combining extracted entities and identified risks
- **LangGraph Pipeline**: Parallel processing pipeline for efficient document analysis
- **Structured Output**: Type-safe data models using Pydantic

## 🏗️ Project Structure

```
Insurance-multi-agent/
├── src/insurance_multi_agent/
│   ├── agents/                    # Agent implementations
│   │   ├── entity_extractor_agent.py    # Extracts structured insurance data
│   │   ├── risk_analyzer_agent.py       # Identifies risks and issues
│   │   ├── summary_agent.py             # Generates summaries
│   │   └── prompts.py                   # System prompts for agents
│   ├── models/                    # Pydantic data models
│   │   ├── document.py           # Document representation
│   │   ├── entities.py           # InsuranceEntities model
│   │   ├── risks.py              # Risks model
│   │   └── state.py              # LangGraph state definition
│   ├── text_extractor/           # OCR and text processing
│   │   ├── text_extractor.py    # PDF extraction logic
│   │   └── utils/
│   │       └── helper_tools.py  # Text cleaning utilities
│   ├── pipeline.py               # LangGraph orchestration
│   ├── config.py                 # Configuration management
│   └── constants.py              # Application constants
├── notebooks/
│   └── development.ipynb         # Development and testing notebook
├── tests/                        # Test files
│   ├── test_agents.py
│   └── test_orchestrator.py
├── data/
│   ├── raw/                      # Input PDF files
│   └── processed/                # Processed outputs
├── main.py                       # Application entry point
├── pyproject.toml                # Project dependencies (uv)
├── .env.example                  # Example environment variables
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Tesseract OCR installed on your system
- OpenRouter API key (or compatible LLM provider)
- uv package manager (recommended) or pip

### System Dependencies

Install Tesseract OCR:

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rodrigosanchezcela/insurance-multi-agent.git
cd insurance-multi-agent
```

2. Install dependencies with uv:
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
```

Edit `.env` and add your API key:
```env
OPENROUTER_API_KEY=your_api_key_here
```

### Running the Application

```bash
uv run python main.py
```

Or activate the virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows
python main.py
```

## 📖 Usage

### Processing a Document

```python
from insurance_multi_agent.text_extractor.text_extractor import TextExtractor
from insurance_multi_agent.pipeline import InsurancePipeline

# Extract text from PDF
extractor = TextExtractor()
document = extractor.extract_text_from_pdf("path/to/insurance.pdf")

# Run the pipeline
pipeline = InsurancePipeline()
initial_state = {
    "document": document,
    "entities": None,
    "risks": None,
    "summary": None
}

result = pipeline.graph.compile().invoke(initial_state)

# Access results
print("Entities:", result['entities'])
print("Risks:", result['risks'])
print("Summary:", result['summary'])
```

### Individual Agent Usage

```python
from insurance_multi_agent.agents.entity_extractor_agent import EntityExtractorAgent
from insurance_multi_agent.agents.risk_analyzer_agent import RiskAnalyzerAgent
from insurance_multi_agent.agents.summary_agent import SummaryAgent

# Extract entities
entity_agent = EntityExtractorAgent()
entities = entity_agent.extract_entities(document)

# Analyze risks
risk_agent = RiskAnalyzerAgent()
risks = risk_agent.analyze_risk(document)

# Generate summary
summary_agent = SummaryAgent()
summary = summary_agent.summarize(risks=risks, entities=entities)
```

## 🔧 Configuration

### LLM Provider

The system uses OpenRouter by default. Configure in `config.py`:

```python
class Config:
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    BASE_URL: str = "https://openrouter.ai/api/v1"
    MODEL: str = "openai/gpt-4o-mini"  # Change model as needed
```

### Pipeline Architecture

The LangGraph pipeline processes documents with parallel entity extraction and risk analysis:

```
START → [extract_entities] ↘
                            → [summarize] → END
START → [analyze_risk]     ↗
```

Both agents read the document independently and run in parallel, then their outputs are combined in the summary node.

## 🧪 Testing

Interactive testing is available in the Jupyter notebook:

```bash
jupyter notebook notebooks/development.ipynb
```

Run unit tests:
```bash
pytest
```

## 📊 Data Models

### InsuranceEntities
- `policy_number`: str
- `policy_type`: str
- `insured_name`: str
- `insurer`: str
- `coverage_amount`: float
- `premium`: float
- `start_date`: str
- `end_date`: str

### Risks
- `risks`: List[str] - List of identified risk findings

### Document
- `source`: str - File path
- `content`: str - Raw extracted text
- `clean_content`: str - Cleaned and processed text
- `pages`: int
- `characters`: int
- `language`: str

## 🛠️ Development

### Adding a New Agent

1. Create agent file in `src/insurance_multi_agent/agents/`:
```python
from langchain_openai import ChatOpenAI
from insurance_multi_agent.config import Config

class MyCustomAgent:
    def __init__(self):
        config = Config()
        self.llm = ChatOpenAI(
            model=config.MODEL,
            base_url=config.BASE_URL,
            api_key=config.OPENROUTER_API_KEY
        )
    
    def process(self, document):
        # Your agent logic
        pass
```

2. Add system prompt to `prompts.py`
3. Create Pydantic model in `models/` if needed
4. Add node to pipeline in `pipeline.py`

### Adding Dependencies

```bash
uv add package-name
```

## 🔍 Troubleshooting

**OCR Quality Issues:**
- Ensure Tesseract is properly installed
- Check document quality and resolution
- Adjust preprocessing in `text_extractor.py`

**API Rate Limits:**
- Use a paid tier API key
- Implement retry logic with exponential backoff
- Consider switching to a different model

**Memory Issues with Large PDFs:**
- Process documents page by page
- Reduce image resolution in OCR preprocessing
- Use streaming for large documents

## 📚 Next Steps

- [ ] Implement batch processing for multiple documents
- [ ] Add caching for LLM responses
- [ ] Create REST API endpoint
- [ ] Add support for more document formats
- [ ] Improve OCR text cleaning
- [ ] Add validation and confidence scores
- [ ] Implement error handling and retry logic
- [ ] Add logging and monitoring

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

MIT License