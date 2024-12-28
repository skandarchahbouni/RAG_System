import requests
import sys
import chromadb

# Configuration
EMBED_MODEL = "nomic-embed-text"
MAIN_MODEL = "gemma:2b"
OLLAMA_API_HOST = "http://ollama:11434"
CHROMA_HOST = "vectordb"
CHROMA_PORT = 8000

# Chroma client setup
chroma = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
collection = chroma.get_or_create_collection("buildragwithpython")

# Parse the query from command-line arguments
query = " ".join(sys.argv[1:])

# Step 0: Pull required models if they aren't already pulled
response = requests.get(f"{OLLAMA_API_HOST}/v1/models")
models = response.json()["data"]
for m in [EMBED_MODEL, MAIN_MODEL]:
    for model in models:
        if model["id"] == m:
            continue
    payload = {"model": m}
    res = requests.post(f"{OLLAMA_API_HOST}/api/pull", json=payload)
    res.raise_for_status()


# Step 1: Get embeddings via Ollama API
embedding_payload = {"model": EMBED_MODEL, "prompt": query}
response = requests.post(f"{OLLAMA_API_HOST}/api/embeddings", json=embedding_payload)
response.raise_for_status()  # Ensure the request was successful
queryembed = response.json()["embedding"]

# Step 2: Query the Chroma database for relevant documents
relevantdocs = collection.query(query_embeddings=[queryembed], n_results=5)[
    "documents"
][0]
docs = "\n\n".join(relevantdocs)

# Step 3: Generate a response using the main model via Ollama API
modelquery = (
    f"{query} - Answer that question using the following text as a resource: {docs}"
)

generate_payload = {"model": MAIN_MODEL, "prompt": modelquery, "stream": False}
response = requests.post(f"{OLLAMA_API_HOST}/api/generate", json=generate_payload)
response.raise_for_status()
output = response.json()

# Print the response
print(output["response"])
