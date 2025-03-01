from abc import ABC, abstractmethod

class Provider(ABC):
    @abstractmethod
    def get_completion(self, messages, temperature=0.7, max_tokens=1000):
        pass