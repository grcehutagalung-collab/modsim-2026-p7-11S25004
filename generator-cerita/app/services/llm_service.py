import requests
from app.config import Config

def generate_from_llm(prompt: str):
    response = requests.post(
        f"{Config.BASE_URL}/llm/chat",
        json={
            "token": Config.LLM_TOKEN,
            "chat": prompt
        }
    )

    if response.status_code != 200:
        raise Exception(f"LLM request failed with status {response.status_code}")

    return response.json()
