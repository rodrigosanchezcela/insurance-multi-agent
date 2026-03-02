from langchain.tools import tool
from insurance_multi_agent.models.document import Document
from insurance_multi_agent.models.entities import InsuranceEntities
from insurance_multi_agent.models.risks import Risks
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from insurance_multi_agent.config import Config
from insurance_multi_agent.agents import ENTITY_EXTRACTION_PROMPT, RISK_ANALYSIS_PROMPT, CLAUSE_SUMMARIZATION_PROMPT

cfg = Config()

entity_llm = ChatOpenAI(api_key=cfg.openrouter_api_key, 
                                base_url="https://openrouter.ai/api/v1",
                                model=cfg.entity_extraction_model,
                    )

risks_llm = ChatOpenAI(api_key=cfg.openrouter_api_key, 
                                base_url="https://openrouter.ai/api/v1",
                                model=cfg.risk_analysis_model,
                    )

summarization_llm = ChatOpenAI(api_key=cfg.openrouter_api_key,
                                base_url="https://openrouter.ai/api/v1",
                                model=cfg.clause_summarization_model,
                    )

@tool
def extract_entities(clean_text : str) -> InsuranceEntities:
    """
    This tool analyzes the clean text and extracts important insurance entities 
    such as policyholder name, policy number, coverage details, dates, and other relevant entities.
    The extracted entities are returned in a structured format using the InsuranceEntities Pydantic model.

    Args:
        clean_text (str): The cleaned text from which to extract insurance entities.
    Returns:
        InsuranceEntities: A structured representation of the extracted insurance entities.
    """

    messages = [SystemMessage(content=ENTITY_EXTRACTION_PROMPT),
                HumanMessage(content=clean_text)]
    
    response = entity_llm.with_structured_output(InsuranceEntities).invoke(messages)
    return response.model_dump()


@tool
def analyze_risks(clean_text: str) -> Risks:
    """
    Tool to analyze risks in the insurance document. It takes the cleaned text as input and identifies potential risks
    mentioned in the document. The identified risks are returned in a structured format using the Risks Pydantic model.
    Args:
        clean_text (str): The cleaned text from the insurance document.
    Returns:
        Risks: A structured representation of the identified risks in the document.
    """
    messages = [SystemMessage(content=RISK_ANALYSIS_PROMPT),
                HumanMessage(content=clean_text)]
    
    response = risks_llm.with_structured_output(Risks).invoke(messages)
    return response.model_dump()



@tool
def validate_entities(entities: InsuranceEntities) -> dict:
    """
    Validates extracted insurance entities for completeness.
    Call this AFTER extract_entities, passing the result directly.
    Returns a validation report the supervisor can reason over.

    Args:
        entities (InsuranceEntities): The extracted insurance entities.
    Returns:
        dict: A report with 'is_valid' (bool) and 'issues' (list of strings).
    """
    issues = []
    if not entities.insured_name or entities.insured_name == "Not found":
        issues.append("Insured Person is missing.")
    if not entities.policy_number or entities.policy_number == "Not found":
        issues.append("Policy Number is missing.")
    if not entities.coverage_amount:
        issues.append("Coverage Amount is missing.")
    if not entities.start_date or entities.start_date == "Not found":
        issues.append("Start Date is missing.")
    if not entities.end_date or entities.end_date == "Not found":
        issues.append("End Date is missing.")

    is_valid = len(issues) == 0
    return {"is_valid": is_valid, "issues": issues}

@tool
def summarize_clauses(clean_text: str) -> str:
    """
    Summarizes the key clauses in the insurance document. It takes the cleaned text as input and produces a concise summary of the main clauses and conditions outlined in the document.

    Args:
        clean_text (str): The cleaned text from the insurance document.
    Returns:
        str: A summary of the key clauses in the document.
    """
    messages = [SystemMessage(content=CLAUSE_SUMMARIZATION_PROMPT),
                HumanMessage(content=clean_text)]
    
    response = summarization_llm.invoke(messages)
    return response.content
