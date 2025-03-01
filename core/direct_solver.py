from .solver import Solver

class DirectSolver(Solver):
    def __init__(self, provider):
        super().__init__(provider)
        
    def solve(self, problem):
        system_prompt = """You are an expert mathematical problem solver. Provide a direct solution to the problem.
1. Analyze the problem carefully.
2. If needed, provide Python code with necessary imports.
3. For your answer, provide:
   - Both symbolic expression AND numerical value when possible
   - Use LaTeX for mathematical expressions (e.g., $\\frac{3}{4}$)
4. Verify your solution when possible."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Problem: {problem}\nSolve this problem step by step."}
        ]
        
        response = self.provider.get_completion(messages)
        
        return {
            "final_answer": response,
            "iterations": 1,
            "solution_attempts": [response],
            "subquestions": []
        }