FROM python:3.13-slim

WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["streamlit", "run", "app.py", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false", \
    "--server.headless=true", \
    "--server.port=8501", \
    "--server.address=0.0.0.0"]
