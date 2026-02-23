"""File containing implementation for the risk analyzer."""

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import List
from os import getenv
from insurance_multi_agent.config import Config
from langchain_core.messages import HumanMessage, SystemMessage
from insurance_multi_agent.models.entities import InsuranceEntities 
from insurance_multi_agent.models.document import Document
from insurance_multi_agent.models.risks import Risks
from insurance_multi_agent.agents.prompts import CLAUSE_SUMMARIZATION_PROMPT

cfg = Config()

class SummaryAgent:

    def __init__(self):
        self.system_prompt = CLAUSE_SUMMARIZATION_PROMPT
        self.llm = ChatOpenAI(api_key=cfg.openrouter_api_key, 
                                base_url="https://openrouter.ai/api/v1",
                                model="openai/gpt-4o-mini",
                                )
    def summarize(self, risks: Risks, entities: InsuranceEntities) -> str:
        """Summarize the document based on the identified risks and extracted entities."""
        risk_list = "\n".join([f"- {risk}" for risk in risks.risks])
        entity_info = "\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in entities.dict().items()])
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Based on the following identified risks:\n{risk_list}\nand the following extracted entities:\n{entity_info}\nSummarize the insurance document.")
        ]

        summary = self.llm.invoke(messages)
        return summary


