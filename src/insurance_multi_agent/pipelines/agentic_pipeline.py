"""Agentic pipeline following the ReAct framework using the ReActSupervisor."""

from insurance_multi_agent.agents.react_supervisor import ReActSupervisor
from insurance_multi_agent.tools.agent_tools import (
    extract_entities,
    analyze_risks,
    validate_entities,
    summarize_clauses,
)
from insurance_multi_agent.models.document import Document
from insurance_multi_agent.config import Config

cfg = Config()


class AgenticPipeline:
    """Agentic pipeline: the ReActSupervisor decides which tools to call and in what order."""

    def __init__(self):
        self.supervisor = ReActSupervisor(tools=cfg.agent_tools, model=cfg.orchestrator_model)

    def run(self, document: Document) -> str:
        """
        Run the agentic pipeline on an insurance document.

        Args:
            document (Document): The insurance document to process.
        Returns:
            str: The final analysis produced by the supervisor.
        """
        return self.supervisor.run(text=document.clean_content)