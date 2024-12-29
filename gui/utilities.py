import requests
import chromadb
import time
from mattsollamatools import chunk_text_by_sentences
import os, magic
import logging

# Configuration
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
DATA_PATH = os.getenv("DATA_PATH")
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


def readtext(path):
    path = path.rstrip()
    path = path.replace(" \n", "")
    path = path.replace("%0A", "")
    relative_path = path
    filename = os.path.abspath(relative_path)
    filetype = magic.from_file(filename, mime=True)
    print(f"\nEmbedding {filename} as {filetype}")
    text = ""
    if filetype == "application/pdf":
        print("PDF not supported yet")
    if filetype == "text/plain":
        with open(filename, "rb") as f:
            text = f.read().decode("utf-8")
    if os.path.exists(filename) and filename.find("content/") > -1:
        os.remove(filename)
    return text


def calculate_embeddings():
    pull_required_models()
    collection = chroma_setup()
    starttime = time.time()
    print("Calculate embeddings ..")
    # Loop through all text files in the data path
    for filename in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, filename)
        # Check if it's a file
        if os.path.isfile(file_path):
            # Read the file content
            text = readtext(file_path)
            # Chunk the text by sentences
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
