FROM python:3.10-slim
RUN apt-get update && apt-get install -y curl
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["chroma", "run", "--host", "0.0.0.0", "--port", "8000", "--path", "/app/vectordb-stores/chromadb"]