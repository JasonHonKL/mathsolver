from setuptools import setup, find_packages

setup(
    name="mathsolver",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "pandas",
        "requests",
        "tqdm",
        "networkx",  # For graph search
        "replicate",  # For Replicate API
    ],
    entry_points={
        "console_scripts": [
            "mathsolver=mathsolver.cli:main",  # Adjusted entry point
        ],
    },
    description="Solve mathematical problems using LLMs with divide and conquer approach",
    author="Jason Hon",
    author_email="j2004nol@gmail.com",
    url="https://github.com/JasonHonKL/mathsolver",
)