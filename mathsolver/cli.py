import argparse
import json
import os
from .config import Config
from .providers.openai_provider import OpenAIProvider
from .providers.replicate_provider import ReplicateProvider
from .providers.ollama_provider import OllamaProvider
from .evaluation.benchmarks import run_benchmark

def main():
    parser = argparse.ArgumentParser(description='MathSolver: Solving math problems with LLMs')
    
    # Main commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configure the system')
    config_parser.add_argument('--provider', choices=['openai', 'replicate', 'ollama'], 
                              help='Provider to use')
    config_parser.add_argument('--api-key', help='API key for the provider')
    config_parser.add_argument('--base-url', help='Base URL for the provider')
    config_parser.add_argument('--model', help='Model to use')
    config_parser.add_argument('--config-file', default='mathsolver_config.json', 
                              help='Path to config file')
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Run benchmarks')
    benchmark_parser.add_argument('--benchmark-file', required=True, 
                                help='Path to benchmark file')
    benchmark_parser.add_argument('--output-file', default='results.json',
                                help='Path to output file')
    benchmark_parser.add_argument('--max-iterations', type=int, default=5,
                                help='Maximum iterations for divide and conquer')
    benchmark_parser.add_argument('--config-file', default='mathsolver_config.json', 
                                help='Path to config file')
    
    # Solve command
    solve_parser = subparsers.add_parser('solve', help='Solve a single problem')
    solve_parser.add_argument('--problem', required=True, help='Math problem to solve')
    solve_parser.add_argument('--method', choices=['direct', 'divide-conquer', 'graph'], 
                            default='divide-conquer', help='Method to use')
    solve_parser.add_argument('--config-file', default='mathsolver_config.json', 
                            help='Path to config file')
    
    args = parser.parse_args()
    
    if args.command == 'config':
        configure(args)
    elif args.command == 'benchmark':
        run_benchmarks(args)
    elif args.command == 'solve':
        solve_problem(args)
    else:
        parser.print_help()

def configure(args):
    config = Config(args.config_file)
    
    if args.provider:
        config.set('provider_type', args.provider)
        
        provider_config = config.get('provider_config', {})
        if args.api_key:
            provider_config['api_key'] = args.api_key
        if args.base_url:
            provider_config['base_url'] = args.base_url
        if args.model:
            provider_config['model'] = args.model
            
        config.set('provider_config', provider_config)
    
    config.save(args.config_file)
    print(f"Configuration saved to {args.config_file}")

def get_provider(config):
    provider_type = config.provider_type
    provider_config = config.provider_config
    
    if provider_type == 'openai':
        return OpenAIProvider(
            api_key=provider_config.get('api_key'),
            base_url=provider_config.get('base_url'),
            model=provider_config.get('model', 'gpt-4')
        )
    elif provider_type == 'replicate':
        return ReplicateProvider(
            api_token=provider_config.get('api_key'),
            model_path=provider_config.get('model')
        )
    elif provider_type == 'ollama':
        return OllamaProvider(
            base_url=provider_config.get('base_url', 'http://localhost:11434'),
            model=provider_config.get('model', 'llama2')
        )
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")

def run_benchmarks(args):
    config = Config(args.config_file)
    
    # Override config with command-line args if provided
    if args.benchmark_file:
        config.set('benchmark_file', args.benchmark_file)
    if args.output_file:
        config.set('output_file', args.output_file)
    if args.max_iterations:
        config.set('max_iterations', args.max_iterations)
    
    provider = get_provider(config)
    
    print(f"Running benchmarks from {config.benchmark_file}")
    print(f"Results will be saved to {config.output_file}")
    print(f"Using provider: {config.provider_type}")
    
    metrics = run_benchmark(
        config.benchmark_file,
        provider,
        config.output_file,
        config.max_iterations
    )
    
    print("\nBenchmark Complete!")
    print("\nDirect Method Metrics:")
    for key, value in metrics['direct_method'].items():
        print(f"  {key}: {value}")
    
    print("\nDivide & Conquer Method Metrics:")
    for key, value in metrics['divide_conquer_method'].items():
        print(f"  {key}: {value}")

def solve_problem(args):
    from .core.direct_solver import DirectSolver
    from .core.divide_conquer_solver import DivideConquerSolver
    from .core.graph_search_solver import GraphSearchSolver
    
    config = Config(args.config_file)
    provider = get_provider(config)
    
    if args.method == 'direct':
        solver = DirectSolver(provider)
    elif args.method == 'graph':
        solver = GraphSearchSolver(provider, 10)  # Max 10 nodes
    else:  # divide-conquer
        solver = DivideConquerSolver(provider, config.max_iterations)
    
    print(f"Solving problem using {args.method} method...")
    solution = solver.solve(args.problem)
    
    print("\nProblem:")
    print(args.problem)
    print("\nSolution:")
    print(solution['final_answer'])
    
    if args.method != 'direct':
        print(f"\nTook {solution['iterations']} iterations")
        if solution['subquestions']:
            print("\nSubquestions generated:")
            for i, sq in enumerate(solution['subquestions'], 1):
                print(f"{i}. {sq}")

if __name__ == "__main__":
    main()