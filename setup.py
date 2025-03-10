#!/usr/bin/env python
from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="fluxative",
        version="0.1.0",
        description="Generate LLM context files from Git repositories",
        packages=find_packages(),
        py_modules=["src/llmgentool", "src/converter", "src/expander"],
        python_requires=">=3.10",
        install_requires=[
            "gitingest>=0.1.4",
        ],
        extras_require={
            "dev": ["pytest>=7.0.0", "ruff>=0.9.10"],
        },
        entry_points={
            "console_scripts": [
                "fluxative=src.llmgentool:main",
            ],
            "uvx": [
                "fluxative=src.llmgentool:main",
            ],
        },
    )
