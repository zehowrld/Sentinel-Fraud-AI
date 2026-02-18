# This uses LangGraph to build an AI that thinks like a forensic analyst.
from langgraph.graph import StateGraph, END 
from src.utils import logger 

def investigator_node(state):
    """AI Agent checks if the transaction matches known fraud patterns."""
    logger.info(f"🔍 Agent: Investigating {state.get('symbol', 'Token')}...")
    # Simulation: In a real app, you'd call a Vector DB here
    state['investigation_done'] = True
    return state

def reporter_node(state):
    """AI Agent writes the final report based on GNN findings."""
    logger.info("📝 Agent: Generating SAR (Suspicious Activity Report)...")
    state['report'] = f"High risk detected: {state.get('symbol')} volume/mcap ratio is anomalous."
    return state

# Define the workflow
builder = StateGraph(dict)
builder.add_node("investigator", investigator_node)
builder.add_node("reporter", reporter_node)

# Define the path
builder.set_entry_point("investigator")
builder.add_edge("investigator", "reporter")
builder.add_edge("reporter", END)

# Compile the agent
fraud_agent = builder.compile()

# Helper function for your Dashboard/Main to call
def run_agent_analysis(symbol, ratio):
    """Runs the LangGraph workflow for a specific coin."""
    initial_state = {"symbol": symbol, "ratio": ratio, "investigation_done": False}
    result = fraud_agent.invoke(initial_state)
    return result.get('report', "No report generated.")