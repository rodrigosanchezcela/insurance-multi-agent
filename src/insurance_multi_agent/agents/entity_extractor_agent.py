"""class for Agent responsible for extracting entities from the text."""
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from os import getenv
from insurance_multi_agent.config import Config
from langchain_core.messages import HumanMessage, SystemMessage
from insurance_multi_agent.models.entities import InsuranceEntities 
from insurance_multi_agent.models.document import Document
from insurance_multi_agent.agents.prompts import ENTITY_EXTRACTION_PROMPT
cfg = Config()

class EntityExtractorAgent:
    """Agent responsible for extracting important insurance entities from text."""

    def __init__(self):
        self.system_prompt = ENTITY_EXTRACTION_PROMPT

        self.llm = ChatOpenAI(api_key=cfg.openrouter_api_key, 
                                base_url="https://openrouter.ai/api/v1",
                                model="openai/gpt-4o-mini",
                                )
        
    def extract_entities(self, document: Document) -> InsuranceEntities:
        """Function to extract entities from the document."""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=document.clean_content)
        ]

        response = self.llm.with_structured_output(InsuranceEntities).invoke(messages)

        return response

    