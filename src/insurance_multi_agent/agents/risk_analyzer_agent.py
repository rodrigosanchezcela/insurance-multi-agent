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
from insurance_multi_agent.agents.prompts import RISK_ANALYSIS_PROMPT

cfg = Config()

class RiskAnalyzerAgent:

    def __init__(self):
        self.system_prompt = RISK_ANALYSIS_PROMPT
        self.llm = ChatOpenAI(api_key=cfg.openrouter_api_key, 
                                base_url="https://openrouter.ai/api/v1",
                                model="openai/gpt-4o-mini",
                                )
    
    def analyze_risk(self, document :  Document) -> List[str]:
        """Analyze the clean text to identify risks"""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=document.clean_content)
        ]

        raw = self.llm.invoke(messages)
        response = self.llm.with_structured_output(Risks).invoke(messages)
        print(raw)
        return response




