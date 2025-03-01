from .solver import Solver
import networkx as nx

class GraphSearchSolver(Solver):
    def __init__(self, provider, max_nodes=10):
        super().__init__(provider)
        self.max_nodes = max_nodes
        
    def solve(self, problem):
        # Create a graph to represent the problem-solving process
        G = nx.DiGraph()
        G.add_node(0, content=problem, type='problem')
        
        current_node_id = 0
        solution_node_id = None
        node_counter = 1
        
        solution_attempts = []
        subquestions = []
        
        # Start with the initial problem
        frontier = [0]
        
        while frontier and node_counter < self.max_nodes:
            current_node_id = frontier.pop(0)
            node_content = G.nodes[current_node_id]['content']
            
            # If this is a solution node, we're done
            if G.nodes[current_node_id].get('type') == 'solution':
                solution_node_id = current_node_id
                break
            
            # Generate system prompt based on node type
            if G.nodes[current_node_id].get('type') == 'problem':
                system_prompt = """You are an expert mathematical problem solver. Follow these steps:
1. First analyze if the problem can be solved directly.
2. If yes, provide a solution marked with SOLUTION:.
3. If not, break it down into 2-3 smaller sub-problems marked with SUBPROBLEM:.
4. For solutions, provide both symbolic expression AND numerical value when possible."""
            else:  # subproblem
                system_prompt = """You are an expert mathematical problem solver. Follow these steps:
1. Solve the given subproblem.
2. Provide your answer marked with SOLUTION:.
3. If you can't solve it directly, break it further into smaller problems marked with SUBPROBLEM:."""
                
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Problem: {node_content}\nAnalyze and solve this problem."}
            ]
            
            response = self.provider.get_completion(messages)
            solution_attempts.append(response)
            
            # Check if there's a solution in the response
            if "SOLUTION:" in response:
                solution_lines = [line for line in response.split('\n') if "SOLUTION:" in line]
                solution = solution_lines[0].replace("SOLUTION:", "").strip() if solution_lines else ""
                
                solution_node_id = node_counter
                G.add_node(node_counter, content=solution, type='solution')
                G.add_edge(current_node_id, node_counter)
                node_counter += 1
                
                # Add the solution node to the frontier
                frontier.append(solution_node_id)
            
            # Extract subproblems
            subproblem_lines = [line for line in response.split('\n') if "SUBPROBLEM:" in line]
            
            for line in subproblem_lines:
                subproblem = line.replace("SUBPROBLEM:", "").strip()
                subquestions.append(subproblem)
                
                G.add_node(node_counter, content=subproblem, type='subproblem')
                G.add_edge(current_node_id, node_counter)
                frontier.append(node_counter)
                node_counter += 1
        
        # If we didn't find a solution, try to get the best answer from our attempts
        if solution_node_id is None:
            final_prompt = """Based on all our previous work, provide the final answer to the original problem.
Start with FINAL ANSWER: and include both the mathematical expression and numerical value if possible."""
            
            messages = [
                {"role": "system", "content": "You are an expert mathematical problem solver."},
                {"role": "user", "content": f"Original problem: {problem}"},
                {"role": "user", "content": "Our solution attempts so far:\n" + "\n".join(solution_attempts)},
                {"role": "user", "content": final_prompt}
            ]
            
            final_response = self.provider.get_completion(messages)
            solution_attempts.append(final_response)
            
            # Extract the final answer
            if "FINAL ANSWER:" in final_response:
                final_answer = final_response.split("FINAL ANSWER:")[1].strip()
            else:
                final_answer = final_response
                
            return {
                "final_answer": final_answer,
                "iterations": len(solution_attempts),
                "solution_attempts": solution_attempts,
                "subquestions": subquestions,
                "graph": G
            }
        
        # Extract the solution from the solution node
        final_answer = G.nodes[solution_node_id]['content']
        
        return {
            "final_answer": final_answer,
            "iterations": len(solution_attempts),
            "solution_attempts": solution_attempts,
            "subquestions": subquestions,
            "graph": G
        }