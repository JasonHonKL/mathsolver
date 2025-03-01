from abc import ABC, abstractmethod

class Solver(ABC):
    def __init__(self, provider):
        self.provider = provider
    
    @abstractmethod
    def solve(self, problem):
        pass