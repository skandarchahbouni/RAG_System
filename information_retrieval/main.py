from fastapi import FastAPI, HTTPException, Query
import requests
import chromadb
import os
from utilities import pull_required_models
from pydantic import BaseModel

# Configuration
EMBED_MODEL = os.getenv("EMBED_MODEL")
OLLAMA_API_HOST = os.getenv("OLLAMA_API_HOST")
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


# Initialize FastAPI app
app = FastAPI()

# Ensure required models are pulled
pull_required_models(ollama_api_host=OLLAMA_API_HOST, model_id=EMBED_MODEL)


class QueryRequest(BaseModel):
    query: str


@app.post("/relevant_docs")
async def query_docs(request: QueryRequest) -> str:
    try:
        # Chroma client setup
        chroma = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        collection = chroma.get_or_create_collection(COLLECTION_NAME)
        query = request.query  # Extract the query from the POST request body
        # Step 1: Get embeddings via Ollama API
        embedding_payload = {"model": EMBED_MODEL, "prompt": query}
        response = requests.post(
            f"{OLLAMA_API_HOST}/api/embeddings", json=embedding_payload
        )
        response.raise_for_status()  # Ensure the request was successful
        queryembed = response.json()["embedding"]

        # Step 2: Query the Chroma database for relevant documents
        relevantdocs = collection.query(query_embeddings=[queryembed], n_results=5)[
            "documents"
        ][0]
        docs = "\n\n".join(relevantdocs)
        return docs
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with Ollama API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
