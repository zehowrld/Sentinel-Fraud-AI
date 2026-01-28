# This uses LangGraph to build an AI that thinks like a forensic analyst.
from langraph.graph import StateGraph, END 
from src.utils import logger 

def investigator_node(state):
    """AI Agent checks if the transaction matches known fraud patterns."""
    logger.info("🔍 Agent: Investigating transaction history...")
    # Simulation: In a real app, you'd call a Vector DB here
    state['investigation_done'] = True
    return state

def reporter_node(state):
    """AI Agent writes the final report."""
    logger.info("📝 Agent: Generating SAR (Suspicious Activity Report)...")
    state['report'] = "High risk detected: Wallet associated with known mixer"
    return state

# Define the workflow
builder = StateGraph(dict)
builder.add_node("investigator", investigator_node)
builder.add_node("reporter", reporter_node)
builder.set_entry_point("investigator")
builder.add_edge("investigator", "reporter")
builder.add_edge("reporter", End)

fraud_agent = builder.compile()