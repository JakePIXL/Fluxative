#!/usr/bin/env python3
"""
GitIngest Output to llms-ctx.txt Converter/Expander

This script takes llms.txt and llms-full.txt files generated from a GitIngest digest
and creates expanded context files (llms-ctx.txt and llms-ctx-full.txt) by including
the actual file contents from the original GitIngest digest.

Usage:
    python expander.py gitingest_digest.txt llms.txt llms-full.txt
    python expander.py <application_name>
"""

import re
import sys
import os
from typing import Dict


def extract_file_contents(gitingest_file: str) -> Dict[str, str]:
    """
    Extract file paths and their contents from a GitIngest output file.

    Args:
        gitingest_file: Path to the GitIngest output file

    Returns:
        Dictionary mapping file paths to their contents
    """
    print(f"Extracting file contents from {gitingest_file}...")
    file_contents = {}

    try:
        with open(gitingest_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Extract file blocks
    file_blocks = re.findall(
        r"={48}\nFile: (.*?)\n={48}\n(.*?)(?=\n\n={48}|\Z)", content, re.DOTALL
    )

    for file_path, file_content in file_blocks:
        # Clean up the file path (remove any leading/trailing whitespace)
        file_path = file_path.strip()
        file_contents[file_path] = file_content

    print(f"Extracted {len(file_contents)} files")
    return file_contents


def expand_links(content: str, file_contents: Dict[str, str]) -> str:
    """
    Expand markdown links with file content from the GitIngest digest.

    Args:
        content: llms.txt content with markdown links
        file_contents: Dictionary mapping file paths to their contents

    Returns:
        Expanded content with file contents
    """
    print("Expanding links with file contents...")
    # Find all markdown links
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    expanded_content = content

    link_count = 0
    for link_text, link_path in links:
        # Check if we have this file's content
        if link_path in file_contents:
            file_content = file_contents[link_path]

            # Format the content section
            formatted_content = f"\n\n## Content of {link_path}\n\n```\n{file_content}\n```\n"

            # Replace directly without using regex to avoid escape sequence issues
            search_text = f"[{link_text}]({link_path})"
            expanded_content = expanded_content.replace(
                search_text, search_text + formatted_content
            )
            link_count += 1

    print(f"Expanded {link_count} links with file contents")
    return expanded_content


def generate_ctx_file(llms_txt_path: str, gitingest_file: str, ctx_output_path: str) -> None:
    """
    Generate a context file by expanding the llms.txt file with file contents.

    Args:
        llms_txt_path: Path to the llms.txt file
        gitingest_file: Path to the original GitIngest digest
        ctx_output_path: Path where the output context file will be written
    """
    print(f"\nProcessing {llms_txt_path} to create {ctx_output_path}...")

    if not os.path.exists(llms_txt_path):
        print(f"Error: {llms_txt_path} not found")
        return

    # Read the llms.txt file
    try:
        with open(llms_txt_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading llms file: {e}")
        return

    # Extract file contents from the GitIngest digest
    file_contents = extract_file_contents(gitingest_file)

    # Expand links in the content
    expanded_content = expand_links(content, file_contents)

    # Write the expanded content to the output file
    try:
        with open(ctx_output_path, "w", encoding="utf-8") as f:
            f.write(expanded_content)
        print(f"Successfully generated {ctx_output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")


def main():
    """Main function"""
    print("Starting llms-ctx generation...")

    if len(sys.argv) < 4 and not len(sys.argv) == 2:
        print("Usage: python expander.py gitingest_digest.txt llms.txt llms-full.txt")
        print("Usage: python expander.py <application_name>")
        sys.exit(1)

    if len(sys.argv) == 2:
        base_name = sys.argv[1]
        gitingest_file = f"./{base_name}-temp.txt"
        llms_txt_path = f"./{base_name}-llms.txt"
        llms_full_txt_path = f"./{base_name}-llms-full.txt"
    else:
        gitingest_file = sys.argv[1]
        llms_txt_path = sys.argv[2]
        llms_full_txt_path = sys.argv[3]
        base_name = os.path.splitext(os.path.basename(llms_txt_path))[0]

    if not os.path.exists(gitingest_file):
        print(f"Error: GitIngest file {gitingest_file} not found")
        sys.exit(1)

    if not os.path.exists(llms_txt_path):
        print(f"Error: llms.txt file {llms_txt_path} not found")
        sys.exit(1)

    if not os.path.exists(llms_full_txt_path):
        print(f"Error: llms-full.txt file {llms_full_txt_path} not found")
        sys.exit(1)

    # Output file paths
    ctx_output_path = f"{base_name}-ctx.txt"
    base_name_full = os.path.splitext(os.path.basename(llms_full_txt_path))[0]
    ctx_full_output_path = f"{base_name_full}-ctx.txt"

    # Generate context files
    generate_ctx_file(llms_txt_path, gitingest_file, ctx_output_path)
    generate_ctx_file(llms_full_txt_path, gitingest_file, ctx_full_output_path)

    print("\nExpansion process complete!")
    print("Generated files:")
    print(f"  - {ctx_output_path}")
    print(f"  - {ctx_full_output_path}")


if __name__ == "__main__":
    main()
