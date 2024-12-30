from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utilities import pull_required_models
import requests
import chromadb
import os

# Configuration
MAIN_MODEL = os.getenv("MAIN_MODEL")
OLLAMA_API_HOST = os.getenv("OLLAMA_API_HOST")
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")

# Chroma client setup
chroma = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

# FastAPI app
app = FastAPI()


# Ensure required models are pulled
pull_required_models(ollama_api_host=OLLAMA_API_HOST, model_id=MAIN_MODEL)


# Pydantic model for request body
class GenerateRequest(BaseModel):
    query: str
    docs: str


@app.post("/generate_response")
async def generate_response(request: GenerateRequest):
    query = request.query
    docs = request.docs
    try:
        # Construct the model query
        modelquery = f"{query} - Answer that question using the following text as a resource: {docs}"
        # Send the query to Ollama API
        generate_payload = {"model": MAIN_MODEL, "prompt": modelquery, "stream": False}
        response = requests.post(
            f"{OLLAMA_API_HOST}/api/generate", json=generate_payload
        )
        response.raise_for_status()  # Ensure the request was successful
        output = response.json()
        # Return the response
        return {"response": output["response"]}
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with Ollama API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)
