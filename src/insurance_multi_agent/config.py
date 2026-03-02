"""file for project configuration"""
import os
from dotenv import load_dotenv
from insurance_multi_agent.tools.agent_tools import (analyze_risks, 
                                                     extract_entities, 
                                                     summarize_clauses, 
                                                     validate_entities)

load_dotenv()  # loads .env before any class attributes read os.getenv()

class Config:
    
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY")

    #models for agents
    entity_extraction_model: str = "openai/gpt-4o-mini"
    risk_analysis_model: str = "openai/gpt-4o-mini"
    clause_summarization_model: str = "openai/gpt-4o-mini"
    orchestrator_model: str = "openai/gpt-4o-mini"
    max_retries: int = 3
    agent_tools = [extract_entities, analyze_risks, summarize_clauses, validate_entities]


