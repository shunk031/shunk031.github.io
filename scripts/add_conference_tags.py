#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "ruamel-yaml>=0.19.1",
# ]
# ///
"""
Add conference tags to publication entries.

Usage:
    uv run scripts/add_conference_tags.py --dry-run  # Preview changes
    uv run scripts/add_conference_tags.py            # Apply changes
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ruamel.yaml import YAML

# Configuration
PUB_DIR = Path(__file__).parent.parent / "content" / "publication"

# Conference tag mapping for consistency with existing tags
CONFERENCE_TAG_MAPPING = {
    "NLP": "ANLP",
    "YANS": "YANS",
    "MIRU": "MIRU",
    "IPSJ": "IPSJ",
}


def parse_frontmatter(content: str) -> Tuple[Dict, str, str]:
    """
    Parse YAML frontmatter and return (metadata, frontmatter_lines, body).

    Returns:
        metadata: Parsed YAML data
        frontmatter_lines: Original frontmatter text (without --- delimiters)
        body: Content after frontmatter
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False

    # Split by --- delimiters
    parts = content.split("---\n", 2)

    if len(parts) < 3:
        raise ValueError("Invalid frontmatter format")

    frontmatter_text = parts[1]
    body = parts[2]

    # Parse metadata
    metadata = yaml.load(frontmatter_text)

    return metadata, frontmatter_text, body


def extract_conference_info(
    publication_short: str, date: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract conference name and year from publication_short.

    Handles formats:
    - "NAME YYYY" (e.g., "NLP 2025", "YANS 2024")
    - "NAMEYYYY" (e.g., "ECCV2024", "KDD2019")
    - "NAMEYYYY SUFFIX" (e.g., "ACL2020 SRW", "AACL-IJCNLP2020 SRW")

    Returns:
        (conference_name, year) or (None, None) if extraction fails
    """
    if not publication_short or not publication_short.strip():
        return None, None

    # Remove trailing suffixes like " SRW", " Workshop"
    cleaned = re.sub(r"\s+(SRW|Workshop)$", "", publication_short.strip())

    # Pattern 1: "NAME YYYY" format
    match = re.match(r"^([A-Za-z\-]+)\s+(\d{4})$", cleaned)
    if match:
        conf_name = match.group(1)
        year = match.group(2)
        return conf_name, year

    # Pattern 2: "NAMEYYYY" format
    match = re.match(r"^([A-Za-z\-]+?)(\d{4})$", cleaned)
    if match:
        conf_name = match.group(1)
        year = match.group(2)
        return conf_name, year

    # Fallback: try to extract year from date field
    if date:
        year_match = re.match(r"^(\d{4})", date)
        if year_match:
            return cleaned, year_match.group(1)

    return None, None


def should_process_publication(metadata: Dict) -> bool:
    """
    Determine if a publication should be processed.

    Returns: True if publication is a conference/workshop paper
    """
    # Check publication_types
    pub_types = metadata.get("publication_types", [])
    if not pub_types:
        return False

    valid_types = ["article", "presentation", "paper-conference"]

    # Must have at least one valid type
    if not any(pt in pub_types for pt in valid_types):
        return False

    # Exclude article-journal and thesis
    if "article-journal" in pub_types or "thesis" in pub_types:
        return False

    # Check if publication_short is not empty
    pub_short = metadata.get("publication_short", "")
    if not pub_short or not pub_short.strip():
        return False

    # Check for exclusion tags
    tags = metadata.get("tags", [])
    if not tags:
        tags = []

    exclusion_tags = ["Preprint", "Journal", "Thesis", "Dissertation"]

    if any(tag in tags for tag in exclusion_tags):
        return False

    return True


def get_base_tag(conference_name: str) -> str:
    """
    Get the base tag for a conference.
    Returns mapped tag if exists, otherwise the conference name itself.
    """
    return CONFERENCE_TAG_MAPPING.get(conference_name, conference_name)


def get_tags_to_add(
    conference_name: str, year: str, existing_tags: List[str]
) -> List[str]:
    """
    Determine which tags to add.

    Returns:
        List of tags to add (may be empty if all tags already exist)
    """
    if not conference_name or not year:
        return []

    base_tag = get_base_tag(conference_name)
    year_tag = f"{conference_name}{year}"

    tags_to_add = []

    # Check if base tag exists
    # Need to check both the mapped base_tag and the conference_name
    has_base_tag = base_tag in existing_tags or conference_name in existing_tags

    if not has_base_tag:
        # Add the conference name (not the mapped base tag)
        tags_to_add.append(conference_name)

    # Always add year-tagged version if not exists
    if year_tag not in existing_tags:
        tags_to_add.append(year_tag)

    return tags_to_add


def modify_tags_in_frontmatter(frontmatter_text: str, tags_to_add: List[str]) -> str:
    """
    Add tags to the frontmatter while preserving formatting.

    Uses regex to find the tags line and append new tags at the end of the array.
    """
    if not tags_to_add:
        return frontmatter_text

    # Find the tags line
    # Pattern matches: tags: ["tag1", "tag2", "tag3"]
    pattern = r"(tags:\s*\[)([^\]]*)\]"

    def replace_tags(match):
        prefix = match.group(1)
        existing_tags = match.group(2)

        # Add comma if there are existing tags
        if existing_tags.strip():
            separator = ", "
        else:
            separator = ""

        # Format new tags with quotes
        new_tags_str = ", ".join(f'"{tag}"' for tag in tags_to_add)

        return f"{prefix}{existing_tags}{separator}{new_tags_str}]"

    modified = re.sub(pattern, replace_tags, frontmatter_text)

    return modified


def process_publication(pub_dir: Path, dry_run: bool = True) -> Optional[Dict]:
    """
    Process a single publication directory.

    Returns:
        Dictionary with processing results, or None if skipped
    """
    index_file = pub_dir / "index.md"

    if not index_file.exists():
        return None

    # Read file
    try:
        content = index_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {index_file}: {e}")
        return None

    # Parse frontmatter
    try:
        metadata, frontmatter_text, body = parse_frontmatter(content)
    except Exception as e:
        print(f"Error parsing frontmatter in {index_file}: {e}")
        return None

    # Check if should process
    if not should_process_publication(metadata):
        return None

    # Extract conference info
    pub_short = metadata.get("publication_short", "")
    date = metadata.get("date", "")
    conference_name, year = extract_conference_info(pub_short, date)

    if not conference_name or not year:
        print(
            f"Warning: Could not extract conference info from '{pub_short}' in {pub_dir.name}"
        )
        return None

    # Determine tags to add
    existing_tags = metadata.get("tags", [])
    if existing_tags is None:
        existing_tags = []

    tags_to_add = get_tags_to_add(conference_name, year, existing_tags)

    if not tags_to_add:
        return None

    # Modify frontmatter
    new_frontmatter = modify_tags_in_frontmatter(frontmatter_text, tags_to_add)
    new_content = f"---\n{new_frontmatter}---\n{body}"

    result = {
        "file": str(index_file.relative_to(PUB_DIR.parent)),
        "dir": pub_dir.name,
        "publication_short": pub_short,
        "conference": conference_name,
        "year": year,
        "tags_before": existing_tags,
        "tags_to_add": tags_to_add,
    }

    if not dry_run:
        try:
            index_file.write_text(new_content, encoding="utf-8")
            result["status"] = "modified"
        except Exception as e:
            print(f"Error writing {index_file}: {e}")
            result["status"] = "error"
            result["error"] = str(e)
    else:
        result["status"] = "dry-run"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Add conference tags and year-tagged versions to publications"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without modifying files"
    )
    args = parser.parse_args()

    if not PUB_DIR.exists():
        print(f"Error: Publication directory not found: {PUB_DIR}")
        return 1

    results = []
    skipped = []

    for pub_dir in sorted(PUB_DIR.iterdir()):
        if not pub_dir.is_dir():
            continue

        # Skip special directories
        if pub_dir.name.startswith("_") or pub_dir.name == "CLAUDE.md":
            continue

        result = process_publication(pub_dir, dry_run=args.dry_run)
        if result:
            results.append(result)
        else:
            skipped.append(pub_dir.name)

    # Print summary
    print("=" * 80)
    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
    else:
        print("EXECUTION MODE - Files have been modified")
    print("=" * 80)
    print()

    print(f"Processed {len(results)} publications")
    print(f"Skipped {len(skipped)} publications")
    print()

    if results:
        print("=" * 80)
        print(
            "Publications to be modified:" if args.dry_run else "Modified publications:"
        )
        print("=" * 80)
        print()

        for r in results:
            print(f"Directory: {r['dir']}")
            print(f"  File: {r['file']}")
            print(f"  Publication: {r['publication_short']}")
            print(f"  Conference: {r['conference']} {r['year']}")
            print(f"  Tags to add: {', '.join(r['tags_to_add'])}")
            print()

    if skipped and args.dry_run:
        print("=" * 80)
        print("Skipped publications (not conference/workshop or missing info):")
        print("=" * 80)
        print()
        for s in skipped:
            print(f"  - {s}")
        print()

    return 0


if __name__ == "__main__":
    exit(main())
