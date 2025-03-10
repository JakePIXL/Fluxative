#!/usr/bin/env python
from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

if __name__ == "__main__":
    setup(
        name="fluxative",
        version="0.1.1",
        description="Generate LLM context files from Git repositories",
        long_description=long_description,
        long_description_content_type="text/markdown",
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
