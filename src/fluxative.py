#!/usr/bin/env python3
"""
Fluxative Tool

This script integrates converter.py and expander.py to generate standardized context files
for LLMs from either a local repository or a GitHub URL.

It can generate the following:
    - llms.txt: Basic repository summary
    - llms-ctx.txt: Basic summary with file contents

with --full-context enabled:
    - llms-full.txt: Comprehensive repository summary
    - llms-ctx-full.txt: Comprehensive summary with file contents

Usage:
    python fluxative.py <repo_path_or_url> [output_directory]
"""

import sys
import os
import shutil
import tempfile
from typing import Optional
from typing_extensions import Annotated
from urllib.parse import urlparse

# Import from local modules
from typing import Dict
from src.converter import parse_gitingest_output, generate_llms_txt
from src.expander import generate_ctx_file

import typer

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

try:
    from gitingest import ingest
except ImportError:
    print("Error: gitingest module not found. Please install it with: pip install gitingest")
    sys.exit(1)


def get_repo_name(repo_path_or_url: str) -> str:
    """
    Extract a repository name from either a path or URL.

    Args:
        repo_path_or_url: Local path or URL to a git repository

    Returns:
        Repository name for use in file naming and directory creation
    """

    # Check if its the CWD
    if repo_path_or_url == ".":
        path = os.path.normpath(os.getcwd())
        return os.path.basename(path)

    # Else Check if it's a URL

    parsed_url = urlparse(repo_path_or_url)

    if parsed_url.scheme and parsed_url.netloc:
        # It's a URL, extract the last part of the path
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) >= 2:  # Format: username/repo
            return path_parts[-1]  # Return the repo part
        elif len(path_parts) == 1:
            return path_parts[0]
        else:
            return "repo"  # Fallback
    else:
        # It's a local path, extract the directory name
        path = os.path.normpath(repo_path_or_url)
        return os.path.basename(path)


def process_repository(
    repo_path_or_url: str,
    output_dir: Optional[str] = None,
    full_context: bool = False,
    dump_raw: bool = False,
) -> tuple[str, Dict]:
    """
    Process a repository to generate LLM context files.

    Args:
        repo_path_or_url: Local path or URL to a git repository
        output_dir: Optional directory to save output files

    Returns:
        Path to the directory containing the generated files
    """
    print(f"Processing repository: {repo_path_or_url}")

    # Extract repo name for naming output files
    repo_name = get_repo_name(repo_path_or_url)

    # Create output directory
    if output_dir:
        # Use specified output directory
        output_path = os.path.join(output_dir, f"{repo_name}-docs")
    else:
        # Use current directory
        output_path = os.path.join(os.getcwd(), f"{repo_name}-docs")

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    print(f"Output directory: {output_path}")

    # Create a temporary directory for intermediate files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Run gitingest on the repository
        print(f"Running gitingest on {repo_path_or_url}...")
        try:
            summary, tree, content = ingest(repo_path_or_url)

            # Write the complete gitingest output to a temporary file
            # Preserving the full structure: Summary, Tree, and Content
            gitingest_output = f"{summary}\n\n{tree}\n\n{content}"
            gitingest_file = os.path.join(temp_dir, f"{repo_name}-temp.txt")

            with open(gitingest_file, "w", encoding="utf-8") as f:
                f.write(gitingest_output)

            print(f"Generated gitingest output at {gitingest_file}")

            # Save the raw gitingest output to the final directory as well
            raw_output_file = os.path.join(output_path, f"{repo_name}-raw.txt")
            with open(raw_output_file, "w", encoding="utf-8") as f:
                f.write(gitingest_output)
            print(f"Saved raw gitingest output to {raw_output_file}")

            # Parse the GitIngest output
            repo_info = parse_gitingest_output(gitingest_file, is_text=False)

            # Store the raw structure elements in repo_info to preserve it
            repo_info["summary"] = summary
            repo_info["tree"] = tree
            repo_info["name"] = repo_name

            # Generate llms.txt and llms-full.txt
            llms_txt_path = os.path.join(temp_dir, f"{repo_name}-llms.txt")
            llms_full_txt_path = os.path.join(temp_dir, f"{repo_name}-llms-full.txt")

            generate_llms_txt(repo_info, llms_txt_path, full_version=False)
            if full_context:
                generate_llms_txt(repo_info, llms_full_txt_path, full_version=True)

            # Generate context files
            ctx_output_path = os.path.join(temp_dir, f"{repo_name}-llms-ctx.txt")
            ctx_full_output_path = os.path.join(temp_dir, f"{repo_name}-llms-full-ctx.txt")

            generate_ctx_file(llms_txt_path, gitingest_file, ctx_output_path)
            if full_context:
                generate_ctx_file(llms_full_txt_path, gitingest_file, ctx_full_output_path)

            # Copy files to output directory
            for file in [
                llms_txt_path,
                llms_full_txt_path,
                ctx_output_path,
                ctx_full_output_path,
            ]:
                output_file = os.path.join(output_path, os.path.basename(file))
                shutil.copy(file, output_file)
                print(f"Copied {file} to {output_file}")

            print("\nGeneration process complete!")
            print(f"All output files are in: {output_path}")

            return output_path, repo_info

        except Exception as e:
            print(f"Error processing repository: {e}")
            sys.exit(1)


@app.command(no_args_is_help=True)
def main(
    repo_path_or_url: Annotated[str, typer.Argument(help="Local path or URL to a git repository")],
    output_dir: Annotated[
        Optional[str],
        typer.Option(
            "--output-dir", "-o", help="Directory to save output files (default: current directory)"
        ),
    ] = None,
    dump_raw: Annotated[
        bool, typer.Option("--dump-raw", "-d", help="Dump raw GitIngest output")
    ] = False,
    full_context: Annotated[
        bool, typer.Option("--full-context", "-f", help="Generate full context files")
    ] = False,
):
    """
    Generate LLM context files from a repository.
    """

    # Process the repository
    output_path, repo_info = process_repository(repo_path_or_url, output_dir)

    repo_name = repo_info["name"]
    print(f"Files generated in: {output_path}")
    print(f"  - {repo_name}-raw.txt (Original GitIngest output with full structure)")
    print(f"  - {repo_name}-llms.txt (Basic repository summary)")
    print(f"  - {repo_name}-llms-full.txt (Comprehensive repository summary)")
    print(f"  - {repo_name}-llms-ctx.txt (Basic summary with file contents)")
    print(f"  - {repo_name}-llms-full-ctx.txt (Comprehensive summary with file contents)")


if __name__ == "__main__":
    app()
