from .solver import Solver
from ..utils.code_execution import execute_python_code

class DivideConquerSolver(Solver):
    def __init__(self, provider, max_iterations=5):
        super().__init__(provider)
        self.max_iterations = max_iterations
        
    def solve(self, problem):
        messages = []
        iteration = 0
        
        system_prompt = """You are an expert mathematical problem solver. Follow these steps:
1. First analyze if the problem can be solved with Python code.
2. If yes, provide clear, executable Python code with necessary imports.
3. If not, break down into smaller sub-problems.
4. For answers, provide:
   - Both symbolic expression AND numerical value when possible
   - Start with 'CONFIDENT:' if you're sure of the answer
   - Use LaTeX for mathematical expressions (e.g., $\\frac{3}{4}$)
5. Keep track of intermediate results and build upon them.
6. Verify your solutions when possible."""

        messages.append({
            "role": "system",
            "content": system_prompt
        })
        messages.append({
            "role": "user",
            "content": f"Problem: {problem}\nAnalyze and solve this problem. If possible, provide Python code. Otherwise, break it down into steps."
        })
        
        solution_attempts = []
        subquestions = []
        
        while iteration < self.max_iterations:
            response = self.provider.get_completion(messages)
            
            solution_attempts.append(response)
            messages.append({"role": "assistant", "content": response})
            
            if response.startswith("CONFIDENT:"):
                return {
                    "final_answer": response.replace("CONFIDENT:", "").strip(),
                    "iterations": iteration + 1,
                    "solution_attempts": solution_attempts,
                    "subquestions": subquestions
                }
            
            if "Step" in response or "Problem" in response:
                for line in response.split('\n'):
                    if (line.startswith(('Step', 'Problem', '•', '-', '*')) or 
                        any(str(i) + '.' in line for i in range(1, 10))):
                        subquestions.append(line.strip())
            
            if "```python" in response:
                code_blocks = response.split("```python")
                for block in code_blocks[1:]:
                    code = block.split("```")[0].strip()
                    execution_result = execute_python_code(code)
                    
                    messages.append({
                        "role": "user",
                        "content": f"The Python code execution resulted in: {execution_result}\n"
                                 "Based on this result, please provide:\n"
                                 "1. The mathematical expression (using LaTeX if needed)\n"
                                 "2. The numerical value\n"
                                 "Start with 'CONFIDENT:' if you're sure of both."
                    })
            else:
                messages.append({
                    "role": "user",
                    "content": "Can any part be solved with Python now? If yes, provide the code. "
                              "If not, continue breaking down the problem. "
                              "Remember to provide both expression and numerical forms when possible."
                })
            
            iteration += 1
            
            if iteration >= self.max_iterations:
                messages.append({
                    "role": "system",
                    "content": "Provide your final answer now, including both expression and numerical value if possible. "
                              "Start with 'CONFIDENT:' if you're sure."
                })
                final_response = self.provider.get_completion(messages)
                return {
                    "final_answer": final_response.replace("CONFIDENT:", "").strip(),
                    "iterations": iteration,
                    "solution_attempts": solution_attempts,
                    "subquestions": subquestions
                }
        
        return None