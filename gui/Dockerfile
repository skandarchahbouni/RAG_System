FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt_tab
COPY . .
ENV QUERY_MANAGER_API="http://query_manager:5002" \
    OLLAMA_API_HOST="http://ollama:11434" \
    EMBED_MODEL="nomic-embed-text" \
    COLLECTION_NAME="rag_collection"
EXPOSE 4000
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=4000"]