import requests
import chromadb
import time
from mattsollamatools import chunk_text_by_sentences
import os
import logging

# Configuration
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
OLLAMA_API_HOST = os.getenv("OLLAMA_API_HOST")
EMBED_MODEL = os.getenv("EMBED_MODEL")


# Chroma setup
def chroma_setup():
    chroma = chromadb.HttpClient(host="vectordb", port=8000)
    # Delete collection if exists
    if any(
        collection.name == COLLECTION_NAME for collection in chroma.list_collections()
    ):
        print("deleting collection")
        chroma.delete_collection(COLLECTION_NAME)
    # Create collection
    collection = chroma.get_or_create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )
    return collection


# Pull the required models if they aren't already pulled
def pull_required_models():
    already_pulled = False
    response = requests.get(f"{OLLAMA_API_HOST}/v1/models")
    for model in response.json()["data"]:
        if model["id"] == EMBED_MODEL:
            already_pulled = True
            break
    if not already_pulled:
        logging.info("Pulling required model .... This may take up to some minutes ...")
        payload = {"model": EMBED_MODEL}
        response = requests.post(f"{OLLAMA_API_HOST}/api/pull", json=payload)
        response.raise_for_status()


def calculate_embeddings(uploaded_files):
    pull_required_models()
    collection = chroma_setup()
    starttime = time.time()
    print("Calculate embeddings ..")
    # Loop through all text files in the data path
    for uploaded_file in uploaded_files:
        filename = uploaded_file.name
        # Check if it's a file
        text = uploaded_file.read().decode("utf-8")
        chunks = chunk_text_by_sentences(
            source_text=text, sentences_per_chunk=7, overlap=0
        )
        print(f"with {len(chunks)} chunks from {filename}")
        # Embed each chunk and add it to the Chroma collection
        for index, chunk in enumerate(chunks):
            # Step 1: Get embeddings via Ollama API
            embedding_payload = {"model": EMBED_MODEL, "prompt": chunk}
            response = requests.post(
                f"{OLLAMA_API_HOST}/api/embeddings", json=embedding_payload
            )
            response.raise_for_status()  # Ensure the request was successful
            embed = response.json()["embedding"]
            # Step 2: Add the embedding to the Chroma collection
            print(".", end="", flush=True)
            collection.add(
                [filename + str(index)],
                [embed],
                documents=[chunk],
                metadatas={"source": filename},
            )
    logging.info("--- %s seconds ---" % (time.time() - starttime))
