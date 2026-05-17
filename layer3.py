"""
LAYER 3: ORCHESTRATOR — Routes queries to the right agent
"""

from layer2_agents import (
    SummarizerAgent, RiskAgent, DecisionAgent,
    NegotiationAgent, ComparisonAgent, LawsAgent
)


class OrchestratorAgent:
    def __init__(self):
        self.summarizer = SummarizerAgent()
        self.risk_agent = RiskAgent()
        self.decision_agent = DecisionAgent()
        self.negotiation_agent = NegotiationAgent()
        self.comparison_agent = ComparisonAgent()
        self.laws_agent = LawsAgent()
        self.doc1_text = ""
        self.doc1_name = ""
        self.doc2_text = ""
        self.doc2_name = ""

    def set_document1(self, text: str, name: str):
        self.doc1_text = text
        self.doc1_name = name

    def set_document2(self, text: str, name: str):
        self.doc2_text = text
        self.doc2_name = name

    def has_two_documents(self) -> bool:
        return bool(self.doc1_text and self.doc2_text)

    def route_query(self, user_query: str) -> str:
        if not self.doc1_text:
            return "⚠️ Upload a document first to get an analysis."
        return self.decision_agent.decide(self.doc1_text, user_query)