#!/usr/bin/env python
from setuptools import setup

if __name__ == "__main__":
    setup(
        name="fluxative",
        version="0.1.0",
        description="Generate LLM context files from Git repositories",
        py_modules=["llmgentool", "converter", "expander"],
        python_requires=">=3.10",
        install_requires=[
            "gitingest>=0.1.4",
            "ruff>=0.9.10",
        ],
    extras_require={
        "dev": ["pytest>=7.0.0"],
    },
        entry_points={
            "console_scripts": [
                "fluxative=llmgentool:main",
            ],
            "uvx": [
                "fluxative=llmgentool:main",
            ],
        },
    )