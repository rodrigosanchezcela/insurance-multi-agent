"""Pydantic model for important entities"""

from pydantic import BaseModel
from insurance_multi_agent.models.document import Document 

class InsuranceEntities(BaseModel):
    """Model for representing important insurance entities."""


    policy_number: str
    policy_type: str
    insured_name: str
    insurer: str
    coverage_amount: float
    premium: float
    start_date: str
    end_date: str
