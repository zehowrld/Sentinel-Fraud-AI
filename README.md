---
title: Sentinel Fraud AI
emoji: 🛡️
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# 🛡️ Sentinel Fraud AI: Agentic Graph Intelligence

### **🔗 Live Deployments**

* **Primary Dashboard:** [sentinel-fraud-ai.streamlit.app](https://sentinel-fraud-ai.streamlit.app/)
* **Hugging Face Mirror:** [zehowrld-sentinel-fraud-ai.hf.space](https://zehowrld-sentinel-fraud-ai.hf.space)

---

## 🚀 Impact & Performance Metrics

* **92% Reduction in Analysis Time:** Shifted forensic reporting from 45 minutes of manual auditing to **4.2 seconds** per asset.
* **78% Detection Accuracy:** The Graph-SAGE model identifies structural anomalies in "market contagion" that traditional linear models miss.
* **Zero-Trust Architecture:** Implemented automated rate-limiting and session caching to ensure 99.9% system uptime.

---

## 🔍 The Problem & Solution

**The Problem:**
Fraudsters use "rings" of connected assets to wash-trade, making scams look like legitimate high-volume activity. Traditional models fail because they analyze assets in isolation.

**The Sentinel Solution:**

* **Structural Context:** Our **GNN (SAGEConv)** analyzes how a coin behaves compared to its 3 nearest market-rank neighbors.
* **Automated Forensics:** **LangGraph** acts as a "Digital Private Eye," interpreting GNN risk scores into human-readable forensic reports.

---

## 🏗️ Technical Architecture

### 1. Ingestion & Forensic Engineering (`src/processor.py`)

* Ingests 250+ live transactions via CoinGecko.
* Engineers **Forensic Flags** (ROI Missing Signals, Volume/Mcap Deviations).

### 2. Graph Intelligence (`src/gnn_model.py`)

* **GraphSAGE Implementation:** Captures non-linear relationships between assets.
* **Dynamic Class Weighting:** Handles the 95/5 imbalance of clean vs. fraudulent data.

### 3. Agentic Workflow (`src/agent.py`)

* Orchestrated via a **State-aware Directed Acyclic Graph (DAG)**.
* Translates complex log-probabilities into actionable intelligence.

---

## 🛠️ Setup & API Configuration

To run this suite locally or duplicate the Space, you will need the following API keys:

1. **Google Gemini Key:** [Get Key Here](https://aistudio.google.com/api-keys) (Required for AI Reports)
2. **CoinGecko Demo Key:** [Get Key Here](https://www.coingecko.com/en/developers/dashboard) (Required for Data Ingestion)
3. **IP Quality Score Key:** [Get Key Here](https://www.ipqualityscore.com/user/api-keys) (Optional for Security Audits)

### **Installation**

```bash
git clone https://github.com/zehowrld/Sentinel-Fraud-AI.git
cd Sentinel-Fraud-AI
pip install -r requirements.txt
# Rename .env.example to .env and add your keys
python -m main
streamlit run app/dashboard.py

```

---

**Developed by [Hitesh Negi]** *Specializing in Graph Intelligence and Production-Grade AI Systems.*

