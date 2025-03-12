#!/usr/bin/env python
from setuptools import setup
from pathlib import Path

from distutils.util import convert_path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

main_ns = {}
ver_path = convert_path("src/__init__.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

if __name__ == "__main__":
    setup(
        name="fluxative",
        version=main_ns["__version__"],
        description="Generate LLM context files from Git repositories",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=["src"],
        package_dir={"": "."},
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
        },
    )
