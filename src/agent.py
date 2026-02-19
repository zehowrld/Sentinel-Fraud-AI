# This uses LangGraph to build an AI that thinks like a forensic analyst.
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END 
from src.utils import logger 
from openai import OpenAI

# Automatically find and load the .env file
load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
else:
    print(f"✅ SUCCESS: API Key loaded (starts with: {api_key[:8]}...)")

client = OpenAI(api_key=api_key)

def investigator_node(state):
    """AI Agent checks if the transaction matches known fraud patterns."""
    logger.info(f"🔍 Agent: Investigating {state.get('symbol', 'Token')}...")
    # Simulation: In a real app, you'd call a Vector DB here
    state['investigation_done'] = True
    return state

def reporter_node(state):
    """AI Agent uses OpenAI to write a UNIQUE forensic report."""
    logger.info("📝 Agent: Generating Unique Forensic Report via OpenAI...")
    
    symbol = state.get('symbol', 'Token').upper()
    ratio = state.get('ratio', 0)
    is_gnn_flagged = state.get('is_gnn_flagged', False)

    status_text = "🚩 GNN NETWORK ALERT: COORDINATED ACTIVITY DETECTED" if is_gnn_flagged else "Node analyzed via local features."
    
    # The Prompt: instructing the AI to write a unique analysis
    prompt = f"""
    You are a Senior Crypto Forensic Analyst. 
    Analyze the token {symbol} which has a Volume/Market Cap ratio of {ratio:.4f}.
    
    Task: Write a professional forensic report. 
    - Do NOT use a fixed template.
    - If the ratio is very high (>0.5), explain why this suggests wash trading or a potential rug pull.
    - If the ratio is moderate, suggest liquidity anomalies.
    - Use specific financial terminology.
    
    Format the output in Markdown with these sections:
    ### 🛡️ Sentinel Forensic Report: {symbol}
    **Risk Assessment:** [Risk Level]
    ---
    #### 🔍 Key Findings
    #### 🤖 Agent Reasoning
    #### ⚖️ Recommendation
    """

    try:
        # GPT-4o will now 'write' the text instead of using a hardcoded string
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional financial forensic assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7 # Higher temperature means more unique/creative writing
        )
        report = response.choices[0].message.content
    except Exception as e:
        print(f"🔴 OPENAI ERROR: {e}")
        logger.error(f"Error calling OpenAI: {e}")
        report = f"⚠️ Analysis failed for {symbol}. Error: {str(e)[:50]}..."
    
    state['report'] = report
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
def run_agent_analysis(symbol, ratio, is_gnn_flagged=False):
    """Runs the LangGraph workflow for a specific coin."""
    initial_state = {"symbol": symbol, "ratio": ratio, "investigation_done": False, "is_gnn_flagged": is_gnn_flagged}
    result = fraud_agent.invoke(initial_state)
    return result.get('report', "No report generated.")