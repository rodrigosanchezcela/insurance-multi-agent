"""Pipeline state model for LangGraph workflow."""

from typing import Optional, TypedDict
from insurance_multi_agent.models.document import Document
from insurance_multi_agent.models.entities import InsuranceEntities
from insurance_multi_agent.models.risks import Risks


class AgentState(TypedDict, total=False):
    """State that flows through the insurance processing pipeline."""

    document: Document          # required — always set before pipeline starts
    entities: InsuranceEntities # optional — set after entity extraction
    risks: Risks                # optional — set after risk analysis
    summary: str                # optional — set after summarization