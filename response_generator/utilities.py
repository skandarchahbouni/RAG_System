import requests


def pull_required_models(ollama_api_host: str, model_id: str):
    response = requests.get(f"{ollama_api_host}/v1/models")
    models = response.json()["data"]
    already_pulled = False
    for model in models:
        if model["id"] == model_id:
            already_pulled = True
    if not already_pulled:
        payload = {"model": model_id}
        res = requests.post(f"{ollama_api_host}/api/pull", json=payload)
        res.raise_for_status()
