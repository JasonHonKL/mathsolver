from . import Provider
import replicate

class ReplicateProvider(Provider):
    def __init__(self, api_token, model_path):
        self.api_token = api_token
        self.model_path = model_path
        
    def get_completion(self, messages, temperature=0.7, max_tokens=1000):
        # Convert messages to Replicate format
        prompt = ""
        for message in messages:
            if message["role"] == "system":
                prompt += f"System: {message['content']}\n"
            elif message["role"] == "user":
                prompt += f"User: {message['content']}\n"
            elif message["role"] == "assistant":
                prompt += f"Assistant: {message['content']}\n"
        
        output = replicate.run(
            self.model_path,
            input={
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        
        # Replicate typically returns a generator
        return "".join(output)