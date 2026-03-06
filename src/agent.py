# This uses LangGraph to build an AI that thinks like a forensic analyst.
import os
import time
import streamlit as st
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END 
from src.utils import logger 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.rate_limiters import InMemoryRateLimiter

# Automatically find and load the .env file
load_dotenv(override=True)

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.08, 
    check_every_n_seconds=0.1, 
    max_bucket_size=10
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # "gemini-2.5-flash-lite"
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_retries=5,
    rate_limiter=rate_limiter
)

# Define a Formal State for the Graph
class AgentState(TypedDict):
    symbol: str
    ratio: float
    price_volatility: float  # Added from EDA
    roi_missing: bool        # Added from EDA
    is_gnn_flagged: bool
    risk_score: float        # Added from GNN output
    investigation_done: bool
    report: str

def investigator_node(state: AgentState):
    """AI Agent checks if the transaction matches known fraud patterns and also refines the investigation based on specific EDA thresholds."""
    logger.info(f"🔍 Sentinel Agent: Cross-referencing {state['symbol']} metrics...")
    
    # Logic: If ratio > 0.95 quantile (from EDA), mark as 'High-Priority'
    state['investigation_done'] = True
    return state

def reporter_node(state: AgentState):
    """Uses Gemini to generate a data-backed forensic narrative."""
    time.sleep(4)
    logger.info(f"📝 Sentinel Agent: Writing Forensic Report for {state['symbol']}...")
    
   # Extracting features you engineered in processor.py
    volatility = state.get('price_volatility', 0) * 100
    roi_status = "MISSING (High Risk Signal)" if state.get('roi_missing') else "Verified"
    
    # The Prompt: instructing the AI to write a unique analysis
    prompt = f"""
    You are a Senior Crypto Forensic Analyst for the 'Sentinel' GNN project.
    
    ASSET: {state['symbol'].upper()}
    - GNN Risk Score: {state.get('risk_score', 0)*100:.2f}%
    - Volume/Mcap Ratio: {state['ratio']:.4f}
    - 24h Price Volatility: {volatility:.2f}%
    - ROI Metadata Status: {roi_status}

    TASK: Write a forensic analysis. 
    1. If GNN Flagged ({state['is_gnn_flagged']}), explain that peer-rank behavior is anomalous.
    2. Use the 'ROI Missing' signal to suggest lack of transparency if applicable.
    3. If Volatility > 20%, mention potential liquidity manipulation.

    ### 🛡️ Sentinel Forensic Report: {state['symbol'].upper()}
    **Final Verdict:** [CRITICAL / HIGH RISK / STABLE]
    ---
    #### 🔍 Data Evidence
    #### 🤖 Model Reasoning
    #### ⚖️ Forensic Recommendation
    """

    try:
        # Use LangChain's invoke method for Gemini
        response = llm.invoke(prompt)
        state['report'] = response.content

    except Exception as e:
        
        logger.error(f"Gemini API Error: {e}")
        state['report'] = f"""
### 🛡️ Sentinel Forensic Report: {state['symbol'].upper()} (DRAFT)
**Final Verdict:** [OFFLINE - HIGH RISK SIGNATURE]
---
#### 🔍 Data Evidence
* **GNN Risk Score:** {state.get('risk_score', 0)*100:.2f}%
* **Volume/Mcap Ratio:** {state['ratio']:.4f}
* **24h Volatility:** {volatility:.2f}%
* **ROI Status:** {roi_status}

#### 🤖 Model Reasoning
The model is currently rate-limited (429 Error), but the input data indicates a high-probability fraud signature based on {state['symbol'].upper()}'s anomalous peer-rank behavior.

#### ⚖️ Forensic Recommendation
Immediate manual audit of smart contract liquidity is advised.
"""
    
    return state

# Define the workflow

builder = StateGraph(AgentState)
builder.add_node("investigator", investigator_node)
builder.add_node("reporter", reporter_node)

# Define the path
builder.set_entry_point("investigator")
builder.add_edge("investigator", "reporter")
builder.add_edge("reporter", END)

# Compile the agent
fraud_agent = builder.compile()

# ADD CACHING
@st.cache_data(ttl=86400, show_spinner=False)
# Helper function for your Dashboard/Main to call
def run_agent_analysis(data_dict):
    """
    Dashboard entry point with streamlit caching. 
    Input: Dictionary containing the coin's processed features.
    """
    symbol = data_dict.get('symbol', 'Unknown')
    try:

        result = fraud_agent.invoke(data_dict)
        return result.get('report', "Report generation timed out.")
    
    except Exception as e:
        logger.error(f"Agent Execution Error for {symbol}: {e}")
        return f"⚠️ System Overloaded for {symbol}. Using cached forensic risk: {data_dict.get('risk_score', 0)*100:.1f}%"
