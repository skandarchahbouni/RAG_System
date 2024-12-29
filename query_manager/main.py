from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

# Configuration
INFORMATION_RETRIEVAL_API_HOST = os.getenv("INFORMATION_RETRIEVAL_API_HOST")
RESPONSE_GENERATOR_API_HOST = os.getenv("RESPONSE_GENERATOR_API_HOST")

# FastAPI app
app = FastAPI()


# Pydantic model for the new endpoint's request body
class CombinedRequest(BaseModel):
    query: str


@app.post("/rag_response")
async def combined_query(request: CombinedRequest):
    query = request.query
    try:
        # Step 1: Request relevant documents
        releavant_docs_response = requests.get(
            f"{INFORMATION_RETRIEVAL_API_HOST}/releavant_docs", params={"query": query}
        )
        releavant_docs_response.raise_for_status()  # Ensure the request was successful
        documents = releavant_docs_response.text  # Get documents as text

        # Step 2: Use relevant documents to generate a response
        generate_payload = {"query": query, "docs": documents}
        generate_response = requests.post(
            f"{RESPONSE_GENERATOR_API_HOST}/generate_response", json=generate_payload
        )
        generate_response.raise_for_status()  # Ensure the request was successful
        generated_text = generate_response.json()["response"]

        # Return the final response
        return {"response": generated_text}

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with the API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5002)
