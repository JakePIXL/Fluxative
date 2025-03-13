# Fluxative

[<img src="https://img.shields.io/pypi/v/fluxative" alt="PyPI - Version">](https://pypi.org/project/fluxative/)
[<img src="https://img.shields.io/pypi/l/fluxative" alt="PyPI - License">](https://github.com/JakePIXL/fluxative/blob/main/LICENSE)
[<img src="https://img.shields.io/github/issues/JakePIXL/fluxative" alt="GitHub Issues or Pull Requests">](https://github.com/JakePIXL/fluxative/issues)
[<img src="https://img.shields.io/github/actions/workflow/status/JakePIXL/Fluxative/python-publish.yml" alt="GitHub Actions Workflow Status">](https://github.com/JakePIXL/fluxative/actions)
[<img src="https://img.shields.io/pypi/dm/fluxative" alt="PyPI - Downloads">](https://pypi.org/project/fluxative/)
[<img src="https://img.shields.io/github/stars/JakePIXL/fluxative" alt="GitHub Repo stars">](https://github.com/JakePIXL/fluxative/stargazers)

Fluxative streamlines the conversion of Git repositories into standardized context files optimized for LLM consumption. The project architecture consists of three core components working together:

- `converter.py`: Transforms GitIngest output into structured llms.txt and llms-full.txt formats
- `expander.py`: Enhances llms.txt files by embedding actual file content from GitIngest
- `fluxative.py`: Integrates both modules for a seamless end-to-end solution

## Features

- Generate LLM-friendly context files from Git repositories or GitHub URLs
- Create a comprehensive set of output files:
  - `repo-raw.txt`: Complete original GitIngest output with Summary, Tree, and File Contents
  - `repo-llms.txt`: Basic repository summary with original structure preserved
  - `repo-llms-full.txt`: Comprehensive repository summary with original structure preserved
  - `repo-llms-ctx.txt`: Basic summary with embedded file contents
  - `repo-llms-full-ctx.txt`: Comprehensive summary with embedded file contents
- Preserve the full structure (Summary, Tree, and Content) from GitIngest
- Automatically organize output files in a structured directory named after the repository

## Installation

### Using uv (Recommended)

```bash
uv install fluxative
```

### From source

```bash
git clone https://github.com/JakePIXL/fluxative.git
cd fluxative
pip install -e .
```

### For development

```bash
git clone https://github.com/JakePIXL/fluxative.git
cd fluxative
pip install -e ".[dev]"
```

## Usage

### As a command-line tool

```bash
# Process a local repository
fluxative /path/to/repo

# Process a GitHub URL
fluxative https://github.com/username/repo

# Specify a custom output directory
fluxative /path/to/repo --output-dir /custom/output/path
```

### With uvx

If you have [uv](https://docs.astral.sh/uv) installed, you can run Fluxative directly without installation:

```bash
# Process a repository
uvx fluxative /path/to/repo

# With custom output directory
uvx fluxative /path/to/repo -o /custom/output/path
```

## Output

Fluxative creates a directory named `<repo-name>-docs` containing different files based on the arguments used:

### Default Output (Always Generated)
- `<repo-name>-llms.txt`: Basic overview of the repository preserving original structure
- `<repo-name>-llms-ctx.txt`: Basic overview with embedded file contents for quick reference

### With `--full-context` Flag
- `<repo-name>-llms-full.txt`: Comprehensive overview including all files with original structure
- `<repo-name>-llms-full-ctx.txt`: Comprehensive overview with all embedded file contents

### With `--dump-raw` Flag
- `<repo-name>-raw.txt`: Complete original GitIngest output with Summary, Tree structure, and File Contents

Each output file maintains the original structure from GitIngest, providing you with:
- Repository summary (name, URL, branch, commit)
- Complete directory tree structure
- File contents organized by category

## Requirements

- Python 3.10+
- GitIngest 0.1.4 or higher
- Typer 0.15.2 or higher

## License

MIT License. See [LICENSE](LICENSE) for more information.
