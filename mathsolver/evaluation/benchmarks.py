import pandas as pd
import json
import os
import numpy as np
from tqdm import tqdm
from ..core.direct_solver import DirectSolver
from ..core.divide_conquer_solver import DivideConquerSolver
from .metrics import calculate_metrics

# Custom JSON encoder to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def run_benchmark(benchmark_file, provider, output_file, max_iterations=5):
    """
    Run benchmark tests using both direct and divide-and-conquer methods.
    
    Args:
        benchmark_file: Path to the benchmark JSON or CSV file
        provider: The provider instance to use
        output_file: Path to save the results
        max_iterations: Maximum iterations for divide and conquer
    
    Returns:
        Dictionary with metrics for both methods
    """
    # Load benchmark data
    if benchmark_file.endswith('.json'):
        df = pd.read_json(benchmark_file, lines=True)
    elif benchmark_file.endswith('.csv'):
        df = pd.read_csv(benchmark_file)
    else:
        raise ValueError("Benchmark file must be JSON or CSV")
    
    # Initialize solvers
    direct_solver = DirectSolver(provider)
    dc_solver = DivideConquerSolver(provider, max_iterations)
    
    direct_results = []
    dc_results = []
    
    # Load existing results if present
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing_results = json.load(f)
            direct_results = existing_results.get("direct_results", [])
            dc_results = existing_results.get("dc_results", [])
    
    start_index = len(direct_results)  # Assuming both have same length
    
    try:
        for i in tqdm(range(start_index, len(df)), desc="Processing problems"):
            problem = df['problem'].iloc[i]
            ground_truth = df['answer'].iloc[i]
            
            # Run direct solver
            direct_solution = direct_solver.solve(problem)
            
            direct_entry = {
                'problem_index': int(i) if isinstance(i, np.integer) else i,
                'problem': problem,
                'ground_truth': ground_truth,
                'solution': direct_solution['final_answer'],
                'iterations_needed': direct_solution['iterations'],
                'solution_attempts': direct_solution['solution_attempts'],
                'subquestions': direct_solution['subquestions']
            }
            
            direct_results.append(direct_entry)
            
            # Run divide and conquer solver
            dc_solution = dc_solver.solve(problem)
            
            dc_entry = {
                'problem_index': int(i) if isinstance(i, np.integer) else i,
                'problem': problem,
                'ground_truth': ground_truth,
                'solution': dc_solution['final_answer'],
                'iterations_needed': dc_solution['iterations'],
                'solution_attempts': dc_solution['solution_attempts'],
                'subquestions': dc_solution['subquestions']
            }
            
            dc_results.append(dc_entry)
            
            # Save after each problem to avoid data loss
            all_results = {
                "direct_results": direct_results,
                "dc_results": dc_results
            }
            
            with open(output_file, 'w') as f:
                json.dump(all_results, f, indent=2, cls=NumpyEncoder)
            
            print(f"Completed problem {i+1}/{len(df)}")
            print(f"Direct method took 1 iteration")
            print(f"Divide & Conquer method took {dc_solution['iterations']} iterations")
            print(f"Generated {len(dc_solution['subquestions'])} subquestions")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error occurred at index {i}: {str(e)}")
        # Save what we have so far
        all_results = {
            "direct_results": direct_results,
            "dc_results": dc_results
        }
        
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2, cls=NumpyEncoder)
    
    # Calculate and return metrics
    direct_metrics = calculate_metrics(direct_results)
    dc_metrics = calculate_metrics(dc_results)
    
    metrics = {
        "direct_method": direct_metrics,
        "divide_conquer_method": dc_metrics
    }
    
    # Save metrics to a separate file
    metrics_file = output_file.replace('.json', '_metrics.json')
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2, cls=NumpyEncoder)
    
    # Also save as CSV for easier analysis
    direct_df = pd.DataFrame(direct_results)
    dc_df = pd.DataFrame(dc_results)
    
    direct_csv = output_file.replace('.json', '_direct.csv')
    dc_csv = output_file.replace('.json', '_dc.csv')
    
    direct_df.to_csv(direct_csv, index=False)
    dc_df.to_csv(dc_csv, index=False)
    
    return metrics