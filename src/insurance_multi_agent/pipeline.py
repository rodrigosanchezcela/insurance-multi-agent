"""File orchestrating the agents to create the pipeline for insurance document analysis."""

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from insurance_multi_agent.models.state import AgentState
from insurance_multi_agent.models.document import Document
from insurance_multi_agent.text_extractor.text_extractor import TextExtractor
from insurance_multi_agent.agents.entity_extractor_agent import EntityExtractorAgent, EntityExtractorAgent
from insurance_multi_agent.agents.risk_analyzer_agent import RiskAnalyzerAgent
from insurance_multi_agent.agents.summary_agent import SummaryAgent
from IPython.display import Image, display
    
class InsurancePipeline:

    def __init__(self) -> None:
        self.text_extractor = TextExtractor()
        self.entity_extractor_agent = EntityExtractorAgent()
        self.risk_analyzer_agent = RiskAnalyzerAgent()
        self.summary_agent = SummaryAgent()
        self.document : Document | None = None
        self.graph : StateGraph = self.create_pipeline()
        self.workflow : CompiledStateGraph = None
    
    def extract_entities_node(self, state: AgentState) -> AgentState:
        """Node to extract entities from the document."""
        entities = self.entity_extractor_agent.extract_entities(state['document'])
        #state['entities'] = entities
        return {"entities" : entities}

    def analyze_risk_node(self, state: AgentState) -> AgentState:
        """Node to analyze risks from the document."""
        risks = self.risk_analyzer_agent.analyze_risk(state['document'])
        #state['risks'] = risks
        return {"risks" : risks}
    
    def summarize_node(self, state: AgentState) -> AgentState:
        """Node to summarize the document based on extracted entities and identified risks."""
        summary = self.summary_agent.summarize(risks=state['risks'], entities=state['entities'])
        #state['summary'] = summary
        return {"summary" : summary}
    
    def create_pipeline(self) -> StateGraph:
        """Create graph structure for the insurance document processing pipeline."""
        graph = StateGraph(AgentState)
        graph.add_node("extract_entities", self.extract_entities_node)
        graph.add_node("analyze_risk", self.analyze_risk_node)
        graph.add_node("summarize", self.summarize_node)

        graph.add_edge(START, "extract_entities")
        graph.add_edge(START, "analyze_risk")
        graph.add_edge("extract_entities", "summarize")
        graph.add_edge("analyze_risk", "summarize")
        graph.add_edge("summarize", END)        

        return graph
    
    def display_pipeline(self):
        """Utility function to visualize the pipeline graph."""
        self.workflow = self.graph.compile()
        display(Image(self.workflow.get_graph().draw_mermaid_png()))

    def invoke(self, initial_state: AgentState) -> AgentState:
        """Invoke the pipeline with an initial state."""
        if self.workflow is None:
            self.workflow = self.graph.compile()
        final_state = self.workflow.invoke(initial_state)






    


