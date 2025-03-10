#!/usr/bin/env python3
"""
GitIngest Output to llms.txt Converter

This script converts any GitIngest digest output file into llms.txt and llms-full.txt formats
following the llms.txt specification.

Usage:
    python converter.py input_digest.txt
"""

from json import JSONDecodeError
import re
import sys
import os
from typing import Dict, List, Tuple, Optional
from gitingest import ingest


def parse_gitingest_output(input_data: str, is_text: Optional[bool] = False) -> Dict:
    """
    Parse a GitIngest output file and extract key components.

    Args:
        input_data: Path to the GitIngest output file or straight content data
        is_text: Whether the input_data is a path or the entire contents

    Returns:
        Dictionary containing parsed components
    """
    print("Parsing GitIngest output...")

    if is_text:
        content = input_data
    else:
        with open(input_data, "r", encoding="utf-8") as f:
            content = f.read()

    # Extract repository information
    repo_info = {}

    # Try to find repository name
    repo_match = re.search(r"Repository:\s*(.+)", content)
    if repo_match:
        repo_info["name"] = repo_match.group(1).strip()
    else:
        dir_match = re.search(r"Directory:\s*(.+)", content)
        if dir_match:
            repo_info["name"] = os.path.basename(dir_match.group(1).strip())
        else:
            # Default if we can't find a repo or directory name
            repo_info["name"] = os.path.basename(input_data).replace(".txt", "")

    # Try to extract branch/commit info
    branch_match = re.search(r"Branch:\s*(.+)", content)
    if branch_match:
        repo_info["branch"] = branch_match.group(1).strip()

    commit_match = re.search(r"Commit:\s*(.+)", content)
    if commit_match:
        repo_info["commit"] = commit_match.group(1).strip()

    # Extract directory structure
    structure_match = re.search(
        r"Directory structure:(.*?)(?=\n\n=+\nFile:|\Z)", content, re.DOTALL
    )
    if structure_match:
        repo_info["structure"] = structure_match.group(1).strip()

    # Extract file information
    file_blocks = re.findall(
        r"={48}\nFile: (.*?)\n={48}\n(.*?)(?=\n\n={48}|\Z)", content, re.DOTALL
    )
    repo_info["files"] = file_blocks

    # Count files by extension
    extensions = {}
    for file_path, _ in file_blocks:
        ext = os.path.splitext(file_path)[-1].lower()
        if ext:
            extensions[ext] = extensions.get(ext, 0) + 1
        else:
            extensions["no_extension"] = extensions.get("no_extension", 0) + 1

    repo_info["extensions"] = extensions

    # Try to infer the main programming language
    if extensions:
        main_language = get_main_language(extensions)
        if main_language:
            repo_info["main_language"] = main_language

    return repo_info


def get_main_language(extensions: Dict[str, int]) -> Optional[str]:
    """
    Infer the main programming language based on file extensions.

    Args:
        extensions: Dictionary of extensions and their counts

    Returns:
        The inferred main language or None
    """
    print("Inferring main language...")
    # Map of extensions to languages
    ext_to_lang = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
        ".c": "C",
        ".cpp": "C++",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".rb": "Ruby",
        ".php": "PHP",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".scala": "Scala",
        ".sh": "Shell",
        ".pl": "Perl",
        ".r": "R",
        ".html": "HTML",
        ".css": "CSS",
        ".sql": "SQL",
    }

    # Filter to known programming languages
    known_exts = {ext: count for ext, count in extensions.items() if ext in ext_to_lang}

    if not known_exts:
        return None

    # Return the language with the most files
    main_ext = max(known_exts.items(), key=lambda x: x[1])[0]
    return ext_to_lang.get(main_ext)


def categorize_files(files: List[Tuple[str, str]]) -> Dict[str, List[Tuple[str, str]]]:
    """
    Categorize files by type for better organization in llms.txt.

    Args:
        files: List of (file_path, content) tuples

    Returns:
        Dictionary of categorized files
    """
    print("Categorizing files...")
    categories = {
        "docs": [],  # Documentation files
        "config": [],  # Configuration files
        "source": [],  # Source code files
        "tests": [],  # Test files
        "scripts": [],  # Script files
        "other": [],  # Other files
    }

    for file_path, content in files:
        path_lower = file_path.lower()

        # Documentation
        if any(path_lower.endswith(ext) for ext in [".md", ".rst", ".txt", ".docx", ".pdf"]) or any(
            name in path_lower
            for name in ["readme", "documentation", "docs/", "license", "contributing"]
        ):
            categories["docs"].append((file_path, content))

        # Configuration
        elif any(
            path_lower.endswith(ext) for ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"]
        ) or any(name in path_lower for name in [".config", "config.", "settings.", ".env"]):
            categories["config"].append((file_path, content))

        # Tests
        elif "test" in path_lower or "spec" in path_lower:
            categories["tests"].append((file_path, content))

        # Scripts
        elif any(path_lower.endswith(ext) for ext in [".sh", ".bat", ".ps1", ".cmd"]):
            categories["scripts"].append((file_path, content))

        # Source code (assuming anything else with a recognized programming extension)
        elif any(
            path_lower.endswith(ext)
            for ext in [
                ".py",
                ".js",
                ".ts",
                ".java",
                ".c",
                ".cpp",
                ".cs",
                ".go",
                ".rs",
                ".rb",
                ".php",
                ".swift",
                ".kt",
                ".scala",
            ]
        ):
            categories["source"].append((file_path, content))

        # Everything else
        else:
            categories["other"].append((file_path, content))

    return categories


def extract_repo_description(files: List[Tuple[str, str]]) -> str:
    """
    Extract a repository description from README or other documentation files.

    Args:
        files: List of (file_path, content) tuples

    Returns:
        Repository description or a generic description
    """
    print("Extracting repository description...")
    # Look for README files first
    readme_files = [
        (path, content)
        for path, content in files
        if os.path.basename(path).lower().startswith("readme")
    ]

    if readme_files:
        # Try to extract the first paragraph after a heading
        content = readme_files[0][1]

        # Find the first heading
        heading_match = re.search(r"^#+ .*$", content, re.MULTILINE)
        if heading_match:
            # Find the first paragraph after the heading
            para_match = re.search(
                r"^\s*$\s*(.*?)^\s*$", content[heading_match.end() :], re.MULTILINE | re.DOTALL
            )
            if para_match:
                description = para_match.group(1).strip()
                # Truncate to a reasonable length
                if len(description) > 200:
                    description = description[:197] + "..."
                return description

        # If we can't find a structured paragraph, grab the first non-empty line
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                return line

    # Check for package.json or pyproject.toml for descriptions
    for path, content in files:
        if path.endswith("package.json"):
            try:
                import json

                package_data = json.loads(content)
                if "description" in package_data:
                    return package_data["description"]
            except JSONDecodeError:
                pass

        elif path.endswith("pyproject.toml"):
            match = re.search(r'description\s*=\s*["\'](.+?)["\']', content)
            if match:
                return match.group(1)

    # Generic fallback
    return "A software repository with no explicit description found."


def generate_llms_txt(repo_info: Dict, output_file: str, full_version: bool = False) -> None:
    """
    Generate llms.txt or llms-full.txt file from parsed repository information.

    Args:
        repo_info: Dictionary containing parsed repo information
        output_file: Path where the output file will be written
        full_version: Whether to generate the full version with additional content
    """
    print(f"Generating {output_file}...")
    # Prepare content
    content = []

    # Add original summary if available
    if "summary" in repo_info:
        content.append(repo_info["summary"])
        content.append("")  # Empty line after summary

    # Add original tree structure if available
    if "tree" in repo_info:
        content.append("## Directory Structure")
        content.append("")
        content.append(repo_info["tree"])
        content.append("")  # Empty line after tree

    # Title (H1)
    repo_name = repo_info.get("name", "Unknown Repository")
    content.append(f"# {repo_name}")

    # Description (blockquote)
    if "files" in repo_info:
        description = extract_repo_description(repo_info["files"])
    else:
        description = "A software repository."
    content.append(f"> {description}")
    content.append("")  # Empty line after description

    # General information about the repository
    if "main_language" in repo_info:
        content.append(f"This is a {repo_info['main_language']} project.")

    if "branch" in repo_info:
        content.append(f"Default branch: {repo_info['branch']}")

    if "commit" in repo_info:
        content.append(f"Current commit: {repo_info['commit']}")

    # Add file stats
    if "extensions" in repo_info:
        content.append("")
        content.append("File types in this repository:")
        for ext, count in sorted(repo_info["extensions"].items(), key=lambda x: -x[1]):
            display_ext = ext if ext != "no_extension" else "files with no extension"
            content.append(f"- {display_ext}: {count} files")

    content.append("")

    # Categorize files
    if "files" in repo_info:
        categorized = categorize_files(repo_info["files"])

        # Documentation section
        if categorized["docs"]:
            content.append("## Documentation")
            for path, _ in categorized["docs"]:
                content.append(f"- [{path}]({path}): Documentation file")
            content.append("")

        # Source code section
        if categorized["source"]:
            content.append("## Source Code")
            if full_version:
                # In full version, include ALL source files
                for path, _ in sorted(categorized["source"]):
                    content.append(f"- [{path}]({path}): Source file")
            else:
                # In basic version, limit to 10 files
                for path, _ in sorted(categorized["source"])[:10]:
                    content.append(f"- [{path}]({path}): Source file")

                if len(categorized["source"]) > 10:
                    content.append(f"- ... and {len(categorized['source']) - 10} more source files")

            content.append("")

        # Configuration section
        if categorized["config"]:
            content.append("## Configuration")
            for path, _ in categorized["config"]:
                content.append(f"- [{path}]({path}): Configuration file")
            content.append("")

        # Scripts section (only in full version if not important)
        if categorized["scripts"] and (full_version or len(categorized["scripts"]) <= 5):
            content.append("## Scripts")
            for path, _ in categorized["scripts"]:
                content.append(f"- [{path}]({path}): Script file")
            content.append("")

        # Tests section (only in full version by default)
        if categorized["tests"] and full_version:
            content.append("## Tests")
            # In full version, include ALL test files
            for path, _ in categorized["tests"]:
                content.append(f"- [{path}]({path}): Test file")
            content.append("")

        # Other files (only in full version)
        if categorized["other"] and full_version:
            content.append("## Optional")
            # In full version, include ALL files in the Optional section
            for path, _ in categorized["other"]:
                content.append(f"- [{path}]({path}): Additional file")

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"Generated {output_file}")


def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("Usage: python converter.py input_digest.txt")
        sys.exit(1)

    if sys.argv[1].find("-"):
        input_file = sys.argv[1]
        is_text = False
        base_name = os.path.splitext(input_file)[0]

        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} not found")
            sys.exit(1)

    else:
        summary, tree, content = ingest(sys.argv[2])

        captured_data = f"{summary}\n\n{tree}\n\n{content}"
        base_name = sys.argv[2].split("/")[-1]

        temp_file = f"{base_name}-temp.txt"
        with open(temp_file, "w+", encoding="utf-8") as f:
            f.write(captured_data)

        input_file = captured_data
        is_text = True

    # Output file paths
    llms_txt_path = f"{base_name}-llms.txt"
    llms_full_txt_path = f"{base_name}-llms-full.txt"

    # Parse the GitIngest output
    repo_info = parse_gitingest_output(input_file, is_text)

    # Generate llms.txt
    generate_llms_txt(repo_info, llms_txt_path, full_version=False)

    # Generate llms-full.txt
    generate_llms_txt(repo_info, llms_full_txt_path, full_version=True)

    print("Conversion complete!")
    print(f"Generated: {llms_txt_path}")
    print(f"Generated: {llms_full_txt_path}")


if __name__ == "__main__":
    main()
