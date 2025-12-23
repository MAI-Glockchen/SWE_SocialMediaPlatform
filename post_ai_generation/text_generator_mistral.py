import os
import re

import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# -----------------------------
# Personas (prompt templates)
# -----------------------------
PERSONAS = {
    "neutral": "You are a neutral person and write a very short and unique social media post.",
    "positive": "You are a positive person and write a very short and unique social media post.",
    "negative": "You are a negative person and write a very short and unique social media post.",
}


# -----------------------------
# Mistral Text Generator
# -----------------------------
class MistralTextGenerator:
    API_URL = "https://api.mistral.ai/v1/chat/completions"

    def __init__(self, model="mistral-small-latest"):
        self.model = model
        self.api_key = os.getenv("MISTRAL_API_KEY")

        if not self.api_key:
            raise RuntimeError("MISTRAL_API_KEY environment variable not set")

    def generate_text(self, additional_prompt, persona="neutral"):
        persona_instruction = PERSONAS.get(persona, PERSONAS["neutral"])
        prompt = f"{persona_instruction}\n\n{additional_prompt}"

        print(f"[post-generator] Sending request to Mistral API with prompt: {prompt}", flush=True)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 150,
        }

        try:
            resp = requests.post(self.API_URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[post-generator] Error calling Mistral API: {e}", flush=True)
            return f"[Error generating text: {e}]"

        try:
            data = resp.json()
        except ValueError:
            print(f"[post-generator] Invalid JSON from Mistral: {resp.text}", flush=True)
            return "[Error: invalid JSON from Mistral]"

        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            print(f"[post-generator] Unexpected response format: {data}", flush=True)
            return "[Error: unexpected response format from Mistral]"

        # Extract text between ** **
        match = re.search(r"\*\*(.*?)\*\*", text, re.DOTALL)
        if match:
            text = match.group(1).strip()
        else:
            print("[post-generator] No **text** found, returning raw text", flush=True)

        print(f"[post-generator] Received text: {text[:100]}...", flush=True)
        return text
