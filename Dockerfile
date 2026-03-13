# 1. Use a specific version for reproducibility
FROM python:3.11-slim

# 2. Set environment variables to optimize Python performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory
WORKDIR /app

# 4. Install system dependencies (only if needed by 'src' logic)
# Note: Adding curl helps with health checks later
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy and install requirements separately for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application
COPY . .

# 7. Expose the default Streamlit port
EXPOSE 8501

# 8. Add a health check (Professional Touch)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 9. Run command with explicit address and port
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]