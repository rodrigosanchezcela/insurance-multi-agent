import logging
from insurance_multi_agent.models.document import Document
from insurance_multi_agent.agents.react_supervisor import ReActSupervisor
from insurance_multi_agent.tools.agent_tools import (
    extract_entities,
    analyze_risks,
    validate_entities,
    summarize_clauses,
)
from insurance_multi_agent.config import Config

# Show INFO logs from the supervisor so you can watch the ReAct loop
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)


def main():
    # Minimal sample document — replace clean_content with real extracted text
    sample_text = """INSURANCE POLICY DOCUMENT
    Policy Number: POL-2024-78432
    Policy Type: Comprehensive Health Insurance
    Insured Name: Jane Doe
    Insurer: SecureLife Insurance Co.
    Coverage Amount: $500,000
    Premium: $1,200 per year
    Start Date: 2024-01-01
    End Date: 2024-12-31

    Key Clauses:
    - Pre-existing conditions are excluded for the first 12 months.
    - Claims must be filed within 30 days of the incident.
    - Coverage does not apply outside the country of residence.
    - In case of fraud, the policy will be immediately voided.
    """

    document = Document(
        source="test_document",
        content=sample_text,
        clean_content=sample_text.strip(),
        pages=1,
        characters=len(sample_text),
    )

    tools = [extract_entities, analyze_risks, validate_entities, summarize_clauses]
    supervisor = ReActSupervisor(tools=tools, model=Config.orchestrator_model)
    result = supervisor.run(text=document.clean_content)

    print("\n=== FINAL RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
