import requests

def pull_required_models(ollama_api_host: str, model_id: str):
    response = requests.get(f"{ollama_api_host}/v1/models")
    if response.status_code == 200:
        try:
            models = response.json().get("data", [])
            if models is None:
                raise ValueError("No data found in response.")
        except ValueError:
            raise ValueError("Invalid response format, 'data' key is missing or empty.")
    else:
        raise Exception(f"Failed to fetch models from {ollama_api_host}. Status code: {response.status_code}")
    
    already_pulled = False
    for model in models:
        if model["id"] == model_id:
            already_pulled = True
    if not already_pulled:
        payload = {"model": model_id}
        res = requests.post(f"{ollama_api_host}/api/pull", json=payload)
        res.raise_for_status()
