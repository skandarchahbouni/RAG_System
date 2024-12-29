FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m nltk.downloader punkt_tab
ENV QUERY_MANAGER_API="http://query_manager:5002" \
    DATA_PATH="data" \
    OLLAMA_API_HOST="http://ollama:11434" \
    EMBED_MODEL="nomic-embed-text" \
    COLLECTION_NAME="stories_collection"
EXPOSE 3000
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=3000"]