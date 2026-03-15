#!/bin/bash

# 1. Generate Forensic Results
RUN python -m main

# 3. Start the Streamlit dashboard
streamlit run app/dashboard.py --server.port=7860 --server.address=0.0.0.0 --server.enableXsrfProtection=false