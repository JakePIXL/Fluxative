# Fluxative

[<img src="https://img.shields.io/pypi/v/fluxative" alt="PyPI - Version">](https://pypi.org/project/fluxative/)
[<img src="https://img.shields.io/pypi/l/fluxative" alt="PyPI - License">](https://github.com/JakePIXL/fluxative/blob/main/LICENSE)
[<img src="https://img.shields.io/github/issues/JakePIXL/fluxative" alt="GitHub Issues or Pull Requests">](https://github.com/JakePIXL/fluxative/issues)
[<img src="https://img.shields.io/github/actions/workflow/status/JakePIXL/Fluxative/python-publish.yml" alt="GitHub Actions Workflow Status">](https://github.com/JakePIXL/fluxative/actions)
[<img src="https://img.shields.io/pypi/dm/fluxative" alt="PyPI - Downloads">](https://pypi.org/project/fluxative/)
[<img src="https://img.shields.io/github/stars/JakePIXL/fluxative" alt="GitHub Repo stars">](https://github.com/JakePIXL/fluxative/stargazers)


A tool to convert Git repositories into standardized context files for LLM consumption. Consists of three main components:

- `converter.py`: Converts GitIngest output to llms.txt and llms-full.txt formats
- `expander.py`: Expands llms.txt files with actual file content from GitIngest
- `llmgentool.py`: Integrates both modules for an end-to-end solution

## Features

- Generate LLM-friendly context files from Git repositories or GitHub URLs
- Creates five output files:
  - `repo-raw.txt`: Complete original GitIngest output with Summary, Tree, and File Contents
  - `repo-llms.txt`: Basic repository summary with original structure preserved
  - `repo-llms-full.txt`: Comprehensive repository summary with original structure preserved
  - `repo-llms-ctx.txt`: Basic summary with file contents
  - `repo-llms-full-ctx.txt`: Comprehensive summary with file contents
- Preserves the full structure (Summary, Tree, and Content) from GitIngest
- Automatically organizes output files in a directory named after the repository

## Installation

### Using uv

```bash
uv install fluxative
```

### From source

```bash
git clone https://github.com/JakePIXL/Fluxative.git
cd Fluxative
pip install -e .
```

### For development

```bash
git clone https://github.com/JakePIXL/Fluxative.git
cd Fluxative
pip install -e ".[dev]"
```

## Usage

### As a command-line tool

```bash
# Process a local repository
fluxative /path/to/repo

# Process a GitHub URL
fluxative https://github.com/username/repo

# Specify an output directory
fluxative /path/to/repo --output-dir /custom/output/path
```

### With uvx

If you have [uv](https://docs.astral.sh/uv) installed:

```bash
# Process a repository
uvx fluxative /path/to/repo

# With output directory
uvx fluxative /path/to/repo -o /custom/output/path
```

## Output

The tool creates a directory named `<repo-name>-docs` containing:

- `<repo-name>-raw.txt`: Complete original GitIngest output with Summary, Tree structure, and File Contents
- `<repo-name>-llms.txt`: Basic overview of the repository including original structure
- `<repo-name>-llms-full.txt`: Comprehensive overview with all files including original structure
- `<repo-name>-llms-ctx.txt`: Basic overview with embedded file contents
- `<repo-name>-llms-full-ctx.txt`: Comprehensive overview with all embedded file contents

Each file preserves the original structure from GitIngest, ensuring you have access to:
- Repository summary (name, URL, branch, commit)
- Complete directory tree structure
- File contents organized by category

## Requirements

- Python 3.10+
- GitIngest 0.1.4 or higher

## License

MIT License. See [LICENSE](LICENSE) for more information.
