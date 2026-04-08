FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (faster caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Then copy code
COPY . .

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]