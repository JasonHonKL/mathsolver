# MathSolver

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MathSolver is an advanced problem-solving tool that leverages Large Language Models (LLMs) with multiple strategies to solve mathematical problems. It supports various solving methods and integrates with popular LLM providers.

## Features

- **Multiple Solving Strategies**:
  - Direct solving
  - Divide-and-conquer approach
  - Graph-based problem decomposition
  
- **LLM Provider Support**:
  - OpenAI
  - Replicate
  - Ollama (local models)
  
- **Evaluation Framework**:
  - Benchmarking system
  - Accuracy metrics
  - Solution iteration tracking

- **Flexible Integration**:
  - Command-line interface (CLI)
  - Python API
  - Configurable providers

## Installation

```bash
git clone https://github.com/JasonHonKL/mathsolver
cd mathsolver
pip install -e .
```
Currently it is not availbe in pypi but will be available soon

## Usage

### CLI

#### 1. Configure your LLM provide
```bash
    mathsolver config --provider openai --api-key YOUR_API_KEY --model your-model
```

#### 2. Solve a single problem
```bash
    mathsolver solve --problem "What is the integral of x^2 from 0 to 3?" --method divide-conquer
```

#### Run benchmarks
```bash
    mathsolver benchmark --benchmark-file problems.json --output-file results.json
```

#### Python API
```python
from mathsolver import OpenAIProvider, DivideConquerSolver

# Initialize provider and solver
provider = OpenAIProvider(api_key="your_api_key")
solver = DivideConquerSolver(provider, max_iterations=5)

# Solve a problem
solution = solver.solve("Solve 3x + 2 = 14")
print(f"Answer: {solution['final_answer']}")
print(f"Iterations: {solution['iterations']}")
print(f"Subquestions: {solution['subquestions']}")
```

#### Configuration
```bash
mathsolver config \
  --provider ollama \
  --base-url http://localhost:11434 \
  --model llama2
```

Supported configuration options:
    - Provider type (openai|replicate|ollama)
    - API keys
    - Model selection
    - Base URLs for custom deployments

Run benchamrks with 
```bash
mathsolver benchmark --benchmark-file math_problems.json --output-file results.json
```

#### Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request


#### LICEENSE
This project is licensed under the MIT License - see the LICENSE file for details.