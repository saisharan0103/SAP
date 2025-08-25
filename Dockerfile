# Simple Docker image for SAP application
FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Install dependencies if a requirements file is provided
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

CMD ["python", "main.py"]
