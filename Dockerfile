FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1

PYTHONUNBUFFERED=1

STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends

build-essential

curl

&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY src/ ./src/

EXPOSE 7860

HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health || exit 1

CMD ["streamlit", "run", "app/dashboard.py", "--server.port=7860", "--server.address=0.0.0.0"]