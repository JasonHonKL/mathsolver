from . import Provider
from openai import OpenAI

class OpenAIProvider(Provider):
    def __init__(self, api_key, base_url=None, model="gpt-4"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        
    def get_completion(self, messages, temperature=0.7, max_tokens=1000):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content