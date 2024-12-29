FROM python:3.10-slim
RUN apt-get update && apt-get install -y curl
WORKDIR /app
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV EMBED_MODEL="nomic-embed-text" \
    OLLAMA_API_HOST="http://ollama:11434" \
    CHROMA_HOST="vectordb" \
    CHROMA_PORT=8000
EXPOSE 5000
CMD ["python", "main.py"]