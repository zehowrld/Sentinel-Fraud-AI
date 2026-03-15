FROM python:3.11-slim

1. Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

2. Working directory
WORKDIR /app

3.System dependencies 
RUN apt-get update && apt-get install -y --no-install-recommends

build-essential

curl

&& rm -rf /var/lib/apt/lists/*

4. Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

5. Application files
COPY app/ ./app/
COPY src/ ./src/

6. Port and Healthcheck for Hugging Face
EXPOSE 7860
HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health || exit 1

7. Start Command
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=7860", "--server.address=0.0.0.0"]