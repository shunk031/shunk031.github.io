#!/usr/bin/env python3
"""
Script to add conference tags to publication frontmatter.

Usage:
    python scripts/add_conference_tags.py --dry-run  # Preview changes
    python scripts/add_conference_tags.py            # Apply changes
"""

import argparse
import re
from pathlib import Path
from typing import Tuple, List, Dict, Any
from io import StringIO
from ruamel.yaml import YAML


class ConferenceTagAdder:
    """Handles adding conference tags to publications."""

    # Conference name mapping
    CONF_NAME_MAP = {
        "NLP": "ANLP",  # Special case: NLP → ANLP
    }

    # Publication types to process
    CONFERENCE_TYPES = {"paper-conference", "presentation", "article"}
    SKIP_TYPES = {"article-journal", "thesis"}

    # Journal patterns to skip even if publication_type is "article"
    JOURNAL_PATTERNS = {
        "IEEE Access",
        "APIN",
        "Appl. Sci.",
        "Applied Sciences",
    }

    def __init__(self, content_dir: Path):
        self.content_dir = content_dir
        self.stats = {
            "processed": 0,
            "modified": 0,
            "unchanged": 0,
            "skipped": 0,
            "errors": 0,
        }
        # Initialize ruamel.yaml with format preservation
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.default_flow_style = None
        self.yaml.width = 4096  # Prevent line wrapping
        self.yaml.allow_duplicate_keys = True  # Handle files with duplicate keys

    def parse_publication_short(self, pub_short: str) -> Tuple[str, str]:
        """Extract conference name and year from publication_short."""
        if not pub_short:
            return "", ""

        # Strip award information
        pub_short = re.sub(r"\s*\*（[^）]*）\*", "", pub_short).strip()

        # Remove SRW suffix
        pub_short = re.sub(r"\s+SRW$", "", pub_short)

        # Pattern 1: Space-separated "NAME YEAR"
        match = re.match(r"^([A-Z]+)\s+(\d{4})$", pub_short)
        if match:
            return match.group(1), match.group(2)

        # Pattern 2: Concatenated "NAMEYEAR"
        match = re.match(r"^([A-Z]+[A-Z-]*)(\d{4})$", pub_short)
        if match:
            return match.group(1), match.group(2)

        # Pattern 3: Hyphenated conference "NAME1-NAME2YEAR"
        match = re.match(r"^([A-Z]+-[A-Z]+)(\d{4})$", pub_short)
        if match:
            return match.group(1), match.group(2)

        # Pattern 4: Just conference name (no year)
        match = re.match(r"^([A-Z]+)$", pub_short)
        if match:
            return match.group(1), ""

        # Unable to parse
        return "", ""

    def should_process(self, frontmatter: Dict[str, Any]) -> bool:
        """Determine if publication should get conference tags."""
        pub_types = frontmatter.get("publication_types", [])

        # Skip if thesis
        if "thesis" in pub_types:
            return False

        # Skip if journal
        if "article-journal" in pub_types:
            return False

        # For "article" type, check if it's actually a journal
        pub_short = frontmatter.get("publication_short", "")
        if "article" in pub_types and pub_short in self.JOURNAL_PATTERNS:
            return False

        # Process if conference type or article (non-journal)
        return any(t in pub_types for t in self.CONFERENCE_TYPES)

    def add_conference_tags(
        self, existing_tags: List[str], conf_name: str, year: str
    ) -> List[str]:
        """Add conference tags while preserving existing tags and avoiding duplicates."""
        new_tags = existing_tags.copy() if existing_tags else []

        # Add conference name tag if not present
        if conf_name and conf_name not in new_tags:
            new_tags.append(conf_name)

        # Add conference+year tag if year exists and not present
        if year:
            conf_year_tag = f"{conf_name}{year}"
            if conf_year_tag not in new_tags:
                new_tags.append(conf_year_tag)

        return new_tags

    def split_frontmatter(self, content: str) -> Tuple[Any, str]:
        """Split content into frontmatter dict and body."""
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError("Invalid frontmatter format")

        # Use ruamel.yaml to load with comment preservation
        stream = StringIO(parts[1])
        frontmatter = self.yaml.load(stream)
        body = parts[2]
        return frontmatter, body

    def merge_frontmatter(self, frontmatter: Any, body: str) -> str:
        """Merge frontmatter and body back."""
        stream = StringIO()
        self.yaml.dump(frontmatter, stream)
        fm_str = stream.getvalue()
        # Remove trailing newline if present
        if fm_str.endswith("\n"):
            fm_str = fm_str[:-1]
        return f"---\n{fm_str}\n---{body}"

    def process_publication(
        self, pub_dir: Path, dry_run: bool = False
    ) -> Dict[str, Any]:
        """Process a single publication directory."""
        index_path = pub_dir / "index.md"

        if not index_path.exists():
            return {"status": "skip", "reason": "no index.md"}

        try:
            # Read file
            content = index_path.read_text(encoding="utf-8")

            # Extract frontmatter
            frontmatter, body = self.split_frontmatter(content)

            # Check if should process
            if not self.should_process(frontmatter):
                pub_types = frontmatter.get("publication_types", [])
                return {
                    "status": "skip",
                    "reason": f"not a conference (types: {pub_types})",
                }

            # Extract conference info
            pub_short = frontmatter.get("publication_short", "")
            if not pub_short:
                return {"status": "skip", "reason": "empty publication_short"}

            conf_name, year = self.parse_publication_short(pub_short)
            if not conf_name:
                return {
                    "status": "skip",
                    "reason": f"cannot parse: '{pub_short}'",
                }

            # Map conference name
            conf_name = self.CONF_NAME_MAP.get(conf_name, conf_name)

            # Add tags
            existing_tags = frontmatter.get("tags", [])
            new_tags = self.add_conference_tags(existing_tags, conf_name, year)

            # Check if modified
            if new_tags == existing_tags:
                return {"status": "unchanged", "reason": "tags already present"}

            # Update frontmatter
            frontmatter["tags"] = new_tags

            # Write back if not dry run
            if not dry_run:
                new_content = self.merge_frontmatter(frontmatter, body)
                index_path.write_text(new_content, encoding="utf-8")

            return {
                "status": "modified",
                "conf_name": conf_name,
                "year": year,
                "added_tags": [t for t in new_tags if t not in existing_tags],
            }

        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def process_all(self, dry_run: bool = False) -> None:
        """Process all publications."""
        pub_dirs = [
            d for d in self.content_dir.iterdir() if d.is_dir() and d.name != ".git"
        ]

        # Filter out _index.md
        pub_dirs = [d for d in pub_dirs if not d.name.startswith("_")]

        print(f"Processing {len(pub_dirs)} publication directories...")
        if dry_run:
            print("[DRY RUN MODE - No changes will be made]\n")

        for pub_dir in sorted(pub_dirs):
            result = self.process_publication(pub_dir, dry_run)

            # Update stats and print
            if result["status"] == "modified":
                self.stats["modified"] += 1
                added = ", ".join(result["added_tags"])
                print(f"✓ {pub_dir.name}: Added [{added}]")
            elif result["status"] == "unchanged":
                self.stats["unchanged"] += 1
                print(f"○ {pub_dir.name}: {result['reason']}")
            elif result["status"] == "skip":
                self.stats["skipped"] += 1
                # Don't print skip messages by default (too verbose)
                # Uncomment if you want to see them:
                # print(f"- {pub_dir.name}: {result['reason']}")
            elif result["status"] == "error":
                self.stats["errors"] += 1
                print(f"✗ {pub_dir.name}: Error - {result['reason']}")

            self.stats["processed"] += 1

        # Print summary
        print("\n" + "=" * 60)
        print("Summary:")
        print(f"  Total processed: {self.stats['processed']}")
        print(f"  Modified:        {self.stats['modified']}")
        print(f"  Unchanged:       {self.stats['unchanged']}")
        print(f"  Skipped:         {self.stats['skipped']}")
        print(f"  Errors:          {self.stats['errors']}")
        print("=" * 60)

        if dry_run:
            print("\nThis was a dry run. Run without --dry-run to apply changes.")


def main():
    parser = argparse.ArgumentParser(description="Add conference tags to publications")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=Path("content/publication"),
        help="Path to publication directory",
    )

    args = parser.parse_args()

    adder = ConferenceTagAdder(args.content_dir)
    adder.process_all(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
