# Contributing to Fluxative

Thank you for considering contributing to Fluxative! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the [Issues](https://github.com/JakePIXL/Fluxative/issues)
- If not, create a new issue using the bug report template
- Include detailed steps to reproduce the bug
- Include sample input files if possible (with sensitive data removed)
- Specify your environment (OS, Python version)

### Suggesting Features

- Check if the feature has already been suggested in the [Issues](https://github.com/JakePIXL/Fluxative/issues)
- If not, create a new issue using the feature request template
- Describe the feature in detail and why it would be valuable

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting: `ruff check .` and `ruff format .`
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Clone the repository
   ```
   git clone https://github.com/JakePIXL/Fluxative.git
   cd Fluxative
   ```

2. Install in development mode
   ```
   pip install -e .
   ```

3. Install development dependencies
   ```
   pip install -e ".[dev]"
   ```

## Coding Standards

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return types
- Write docstrings for all functions, classes, and modules
- Keep line length to 100 characters
- Use descriptive variable names
- Group imports: standard library, third-party, local

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

## Documentation

- Update documentation when changing functionality
- Use clear and consistent language
- Include examples where appropriate

Thank you for your contributions!
