from . import Provider
import requests
import json

class OllamaProvider(Provider):
    def __init__(self, base_url="http://localhost:11434", model="llama2"):
        self.base_url = base_url
        self.model = model
        
    def get_completion(self, messages, temperature=0.7, max_tokens=1000):
        # Convert messages to Ollama format
        prompt = ""
        for message in messages:
            if message["role"] == "system":
                prompt += f"System: {message['content']}\n"
            elif message["role"] == "user":
                prompt += f"User: {message['content']}\n"
            elif message["role"] == "assistant":
                prompt += f"Assistant: {message['content']}\n"
                
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "max_length": max_tokens
            }
        )
        
        return json.loads(response.text)["response"]