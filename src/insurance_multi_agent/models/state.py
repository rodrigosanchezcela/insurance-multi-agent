"""Pipeline state model for LangGraph workflow."""

from pydantic import BaseModel
from typing import Optional, TypedDict
from insurance_multi_agent.models.document import Document
from insurance_multi_agent.models.entities import InsuranceEntities
from insurance_multi_agent.models.risks import Risks


class AgentState(TypedDict):
    """State that flows through the insurance processing pipeline."""
    
    document: Document
    entities: Optional[InsuranceEntities] = None
    risks: Optional[Risks] = None
    summary: Optional[str] = None