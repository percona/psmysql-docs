#!/usr/bin/env python3
"""
Add Lumo‑style front‑matter to every Markdown file under a source tree
and write the results to a separate destination directory or update files in place.

The script automatically:
- Extracts titles, descriptions, and metadata from markdown files
- Determines technical preview status for documents and individual variables/values
- Generates slugs, categories, sections, and tags
- Uses git to determine when files were introduced (optional)
- Adds comprehensive front-matter including all required fields

USAGE EXAMPLES:

1. Update files in place with git-based version detection:
   python3 add_front_matter.py --src docs --in-place --use-git

2. Update files in place with a fixed version (fallback for files git can't determine):
   python3 add_front_matter.py --src docs --in-place --use-git --introduced-in "8.4.6-6"

3. Write to a separate destination directory with fixed version:
   python3 add_front_matter.py --src docs --dst /path/to/output --introduced-in "8.4.6-6"

4. Update files in place with fixed version (no git):
   python3 add_front_matter.py --src docs --in-place --introduced-in "8.4.6-6"

ARGUMENTS:
  --src PATH          Source directory containing *.md files (default: docs/percona-server/8.4)
  --dst PATH          Destination directory (required unless --in-place is used)
  --in-place          Update source files directly instead of writing to destination
  --introduced-in VER Version string for 'since' field (required unless --use-git is used)
  --use-git           Use git to automatically determine version for each file based on commit dates

NOTES:
- Release-notes files are automatically skipped
- Files with existing front-matter are regenerated with new format
- Technical preview variables and values are automatically detected and added to front-matter
- The script looks for mkdocs.yml or mkdocs-base.yml to determine categories/sections
"""

import argparse
import pathlib
import re
import subprocess
import sys
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ----------------------------------------------------------------------
# Configuration – tweak if you need different defaults or keywords
# ----------------------------------------------------------------------
DEFAULT_STATUS = "stable"          # fallback when we don't detect preview

TECH_PREVIEW_PHRASES = [
    r"\btech[-\s]?preview\b",
    r"\bexperimental\b",
    r"\bbeta\b",
]

# If you have a curated list of known preview variables, put them here.
KNOWN_PREVIEW_VARIABLES: List[str] = []   # e.g. ["rocksdb_use_write_buffer_manager"]

# ----------------------------------------------------------------------
# Helper utilities (unchanged from the original version)
# ----------------------------------------------------------------------
def load_markdown(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_description(content: str, max_length: int = 200) -> str:
    """Extract a one-sentence description from the content."""
    # Remove front-matter if present
    if content.lstrip().startswith("---"):
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if i > 0 and line.strip() == "---":
                content = "\n".join(lines[i+1:])
                break
    
    # Remove markdown includes and other directives
    content = re.sub(r'--8<--.*', '', content)
    content = re.sub(r'--8<---.*', '', content)
    
    # Find the first paragraph after the main heading
    lines = content.splitlines()
    in_paragraph = False
    paragraph_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip headings, code blocks, lists, etc.
        if not line or line.startswith("#") or line.startswith("```") or line.startswith("*") or line.startswith("-") or line.startswith("!"):
            if in_paragraph and paragraph_lines:
                break
            continue
        
        # Start collecting paragraph text
        in_paragraph = True
        # Remove markdown links but keep text
        line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
        paragraph_lines.append(line)
        
        if len(" ".join(paragraph_lines)) > max_length:
            break
    
    description = " ".join(paragraph_lines).strip()
    # Truncate to max_length and ensure it ends with a period
    if len(description) > max_length:
        description = description[:max_length].rsplit('.', 1)[0] + '.'
    elif description and not description.endswith(('.', '!', '?')):
        description += '.'
    
    return description if description else ""


def generate_slug(file_path: pathlib.Path) -> str:
    """Generate a URL slug from the filename."""
    return file_path.stem


def get_category_and_section(file_path: pathlib.Path, mkdocs_path: Optional[pathlib.Path] = None) -> Tuple[Optional[str], Optional[str]]:
    """Determine category and section from mkdocs.yml or file path."""
    # Try to load from mkdocs.yml if provided
    if mkdocs_path and mkdocs_path.exists():
        try:
            with open(mkdocs_path, 'r', encoding='utf-8') as f:
                mkdocs_content = f.read()
            
            filename = file_path.name
            # Simple parsing - look for the filename in the nav structure
            # This is a simplified parser; a full YAML parser would be better
            lines = mkdocs_content.split('\n')
            current_category = None
            current_section = None
            
            for i, line in enumerate(lines):
                # Look for top-level categories (lines starting with "  - Category:")
                if re.match(r'^\s+-\s+(\w+):', line):
                    current_category = re.match(r'^\s+-\s+(\w+):', line).group(1)
                    current_section = None
                # Look for sections (nested under categories)
                elif re.match(r'^\s+-\s+(\w+[^:]*):', line) and current_category:
                    # Check if next lines contain our filename
                    for j in range(i+1, min(i+20, len(lines))):
                        if filename in lines[j]:
                            current_section = re.match(r'^\s+-\s+([^:]+):', line).group(1).strip()
                            return current_category, current_section
                # Direct file reference
                elif filename in line and current_category:
                    return current_category, current_section
            
        except Exception:
            pass
    
    # Fallback: infer from file path/name
    filename_lower = file_path.stem.lower()
    if 'install' in filename_lower or 'apt' in filename_lower or 'yum' in filename_lower or 'docker' in filename_lower:
        return "Install", None
    elif 'upgrade' in filename_lower or 'downgrade' in filename_lower:
        return "Upgrade", None
    elif 'sql' in filename_lower or 'database' in filename_lower or 'table' in filename_lower:
        return "Develop", None
    elif 'secure' in filename_lower or 'encrypt' in filename_lower or 'ssl' in filename_lower:
        return "Secure", None
    elif 'backup' in filename_lower or 'restore' in filename_lower:
        return "Back up and restore", None
    elif 'replicate' in filename_lower or 'replication' in filename_lower:
        return "Replicate", None
    elif 'monitor' in filename_lower or 'slow' in filename_lower:
        return "Monitor", None
    elif 'troubleshoot' in filename_lower or 'error' in filename_lower:
        return "Troubleshoot", None
    
    return None, None


def get_last_modified(file_path: pathlib.Path, repo_root: Optional[pathlib.Path] = None) -> Optional[str]:
    """Get the last modified date from git."""
    if not repo_root:
        return None
    
    try:
        rel_path = file_path.resolve().relative_to(repo_root.resolve())
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ai", "--", str(rel_path)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode == 0 and result.stdout.strip():
            date_str = result.stdout.strip().split()[0]  # Get YYYY-MM-DD
            return date_str
    except Exception:
        pass
    
    return None


def generate_tags(content: str, filename: str) -> List[str]:
    """Generate tags based on content and filename."""
    tags = ["percona-server"]
    
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    # Add tags based on filename patterns
    if 'myrocks' in filename_lower:
        tags.append("myrocks")
        tags.append("rocksdb")
    if 'audit' in filename_lower:
        tags.append("audit-log")
    if 'encrypt' in filename_lower:
        tags.append("encryption")
    if 'ssl' in filename_lower or 'tls' in filename_lower:
        tags.append("ssl")
    if 'replication' in filename_lower or 'replicate' in filename_lower:
        tags.append("replication")
    if 'backup' in filename_lower:
        tags.append("backup")
    if 'install' in filename_lower:
        tags.append("installation")
    if 'upgrade' in filename_lower:
        tags.append("upgrade")
    if 'sql' in filename_lower:
        tags.append("sql")
    if 'docker' in filename_lower:
        tags.append("docker")
    if 'apt' in filename_lower or 'deb' in filename_lower:
        tags.append("apt")
        tags.append("debian")
    if 'yum' in filename_lower or 'rpm' in filename_lower:
        tags.append("yum")
        tags.append("rhel")
        tags.append("centos")
    
    # Add tags based on content
    if 'tech-preview' in content_lower or 'experimental' in content_lower:
        tags.append("tech-preview")
    
    return sorted(list(set(tags)))


def get_git_introduced_version(file_path: pathlib.Path, repo_root: pathlib.Path) -> Optional[str]:
    """
    Use git to determine when a file was first introduced.
    Returns the version string based on git tags or commit dates, or None if git info is unavailable.
    """
    try:
        # Resolve paths to absolute
        file_path = file_path.resolve()
        repo_root = repo_root.resolve()
        
        # Get the relative path from repo root
        try:
            rel_path = file_path.relative_to(repo_root)
        except ValueError:
            # File is not in the repo, return None
            return None
        
        # Find the first commit that added this file (with date)
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%H|%ai", "--", str(rel_path)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            return None
        
        # Get the first commit hash and date
        first_line = result.stdout.strip().split('\n')[0]
        if '|' not in first_line:
            return None
        
        first_commit, commit_date = first_line.split('|', 1)
        commit_date = commit_date.strip()
        
        # Try to find tags first
        tag_result = subprocess.run(
            ["git", "tag", "--contains", first_commit, "--sort=-version:refname"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if tag_result.returncode == 0 and tag_result.stdout.strip():
            tags = tag_result.stdout.strip().split('\n')
            version_tags = [t for t in tags if re.match(r'^\d+\.\d+\.\d+', t)]
            if version_tags:
                return version_tags[0]
        
        # If no tags, try to find tags before this commit
        all_tags_result = subprocess.run(
            ["git", "tag", "--sort=-version:refname"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if all_tags_result.returncode == 0 and all_tags_result.stdout.strip():
            tags = all_tags_result.stdout.strip().split('\n')
            version_tags = [t for t in tags if re.match(r'^\d+\.\d+\.\d+', t)]
            
            for tag in version_tags:
                tag_commit_result = subprocess.run(
                    ["git", "rev-list", "-n", "1", tag],
                    cwd=repo_root,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if tag_commit_result.returncode == 0:
                    tag_commit = tag_commit_result.stdout.strip()
                    merge_base_result = subprocess.run(
                        ["git", "merge-base", "--is-ancestor", tag_commit, first_commit],
                        cwd=repo_root,
                        capture_output=True,
                        timeout=5,
                    )
                    if merge_base_result.returncode == 0:
                        return tag
        
        # If still no tags, use commit date to infer version
        # Parse the date (format: 2023-07-27 18:53:21 +0300)
        try:
            from datetime import datetime
            # Extract just the date part (YYYY-MM-DD)
            date_part = commit_date.split()[0]
            commit_datetime = datetime.strptime(date_part, "%Y-%m-%d")
            
            # Map dates to versions based on known release dates
            # Percona Server 8.4.0 was released around August 2024
            # Adjust these dates based on actual release dates
            if commit_datetime >= datetime(2025, 9, 1):
                return "8.4.6-6"
            elif commit_datetime >= datetime(2025, 5, 1):
                return "8.4.5-5"
            elif commit_datetime >= datetime(2025, 3, 1):
                return "8.4.4-4"
            elif commit_datetime >= datetime(2024, 12, 1):
                return "8.4.3-3"
            elif commit_datetime >= datetime(2024, 11, 1):
                return "8.4.2-2"
            elif commit_datetime >= datetime(2024, 8, 1):
                return "8.4.0-1"
            # For files introduced before 8.4, return None
            # The caller should handle this - either use fallback or leave empty
            return None
            
        except (ValueError, ImportError):
            return None
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return None
    except Exception:
        return None


def is_tech_preview(content: str) -> bool:
    # 1️⃣ Phrase search
    for pat in TECH_PREVIEW_PHRASES:
        if re.search(pat, content, flags=re.IGNORECASE):
            return True

    # 2️⃣ Heading‑based detection
    heading_pat = re.compile(r"^(#+)\s+(.*)", flags=re.MULTILINE)
    for m in heading_pat.finditer(content):
        _, title = m.group(1), m.group(2).lower()
        if any(word in title for word in ("variable", "option", "feature")):
            # Grab a short snippet after the heading
            snippet = content[m.end():m.end() + 500]
            for pat in TECH_PREVIEW_PHRASES:
                if re.search(pat, snippet, flags=re.IGNORECASE):
                    return True

    # 3️⃣ Whitelist check (optional)
    if KNOWN_PREVIEW_VARIABLES:
        for var in KNOWN_PREVIEW_VARIABLES:
            if re.search(rf"`{re.escape(var)}`", content):
                return True
            if re.search(rf"\b{re.escape(var)}\b", content):
                return True

    return False


def extract_technical_preview_items(content: str) -> Dict[str, List[str]]:
    """
    Extract variables and values that are marked as technical preview.
    Returns a dict with 'variables' and 'values' keys containing lists.
    """
    preview_variables = []
    preview_values = []
    
    # Pattern 1: "This variable is [tech preview]" or "The variable is in [tech preview] mode"
    # Look for variable names in headings (## variable_name) followed by tech preview mention
    variable_heading_pattern = re.compile(r'^##+\s+([^\n]+)', re.MULTILINE)
    tech_preview_pattern = re.compile(
        r'(?:this\s+variable|the\s+variable).*?tech[-\s]?preview|tech[-\s]?preview.*?(?:this\s+variable|the\s+variable)',
        re.IGNORECASE
    )
    
    # Find all variable headings
    for match in variable_heading_pattern.finditer(content):
        heading_text = match.group(1).strip()
        # Extract variable name (remove markdown links, code formatting)
        var_name = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', heading_text)
        var_name = re.sub(r'`([^`]+)`', r'\1', var_name)
        var_name = var_name.strip()
        
        # Check if the section after this heading mentions tech preview
        section_start = match.end()
        # Look ahead up to 500 characters for tech preview mention
        section_text = content[section_start:section_start + 500]
        if tech_preview_pattern.search(section_text):
            # Also check for explicit "This variable is tech preview" pattern
            explicit_pattern = re.compile(
                r'(?:this\s+variable|the\s+variable).*?is.*?\[tech[-\s]?preview\]|'
                r'the\s+variable.*?is\s+in\s+\[tech[-\s]?preview\].*?mode',
                re.IGNORECASE
            )
            if explicit_pattern.search(section_text):
                preview_variables.append(var_name)
    
    # Pattern 2: "The 'X' value is in [tech preview] mode" or "value X is tech preview"
    # Look for quoted values or values in specific contexts
    value_patterns = [
        # Pattern: "The 'MAJORITY' value is in [tech preview] mode"
        re.compile(r"the\s+['\"]([^'\"]+)['\"]\s+value\s+is\s+in\s+\[tech[-\s]?preview\].*?mode", re.IGNORECASE),
        # Pattern: "value X is tech preview"
        re.compile(r"value\s+['\"]([^'\"]+)['\"].*?tech[-\s]?preview", re.IGNORECASE),
        # Pattern: "The X value is tech preview"
        re.compile(r"the\s+['\"]([^'\"]+)['\"]\s+value.*?tech[-\s]?preview", re.IGNORECASE),
    ]
    
    for pattern in value_patterns:
        for match in pattern.finditer(content):
            value = match.group(1).strip()
            if value and value not in preview_values:
                preview_values.append(value)
    
    # Pattern 3: Look for variables mentioned with tech preview in the same sentence/paragraph
    # "variable_name is tech preview" or "variable_name (tech preview)"
    inline_var_pattern = re.compile(
        r'`?([a-z_][a-z0-9_]*)`?\s+(?:is|are|\().*?tech[-\s]?preview',
        re.IGNORECASE
    )
    for match in inline_var_pattern.finditer(content):
        var_name = match.group(1)
        if var_name and var_name not in preview_variables:
            # Verify it's actually a variable mention (not just any word)
            if len(var_name) > 3 and '_' in var_name:  # Variables typically have underscores
                preview_variables.append(var_name)
    
    return {
        "variables": sorted(list(set(preview_variables))),
        "values": sorted(list(set(preview_values)))
    }


def build_front_matter(
    title: str,
    description: str,
    slug: str,
    category: Optional[str],
    section: Optional[str],
    since: Optional[str],
    stability: str,
    technical_preview: bool,
    tags: List[str],
    author: str,
    last_modified: Optional[str],
    draft: bool = False,
    related: Optional[List[str]] = None,
    technical_preview_items: Optional[Dict[str, List[str]]] = None
) -> str:
    """Build comprehensive front-matter in the new template format."""
    fm = {
        "title": title,
    }
    
    # Description
    if description:
        fm["description"] = description
    
    # Slug
    fm["slug"] = slug
    
    # Category and section
    if category:
        fm["category"] = category
    if section:
        fm["section"] = section
    
    # Version information
    if since:
        fm["since"] = since
        fm["until"] = None  # null = still current (will be output as null in YAML)
    
    # Stability
    fm["stability"] = stability
    fm["technical_preview"] = technical_preview
    
    # Tags
    if tags:
        fm["tags"] = tags
    
    # Author
    fm["author"] = author
    
    # Last modified
    if last_modified:
        fm["last_modified"] = last_modified
    
    # Draft
    fm["draft"] = draft
    
    # Related pages (optional)
    if related:
        fm["related"] = related
    
    # Technical preview items (variables and values)
    if technical_preview_items:
        if technical_preview_items.get("variables"):
            fm["technical_preview_variables"] = technical_preview_items["variables"]
        if technical_preview_items.get("values"):
            fm["technical_preview_values"] = technical_preview_items["values"]
    
    return yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)


def process_file(src_path: pathlib.Path, src_root: pathlib.Path, dst_root: Optional[pathlib.Path] = None, in_place: bool = False, introduced_in: str = "", use_git: bool = False, repo_root: Optional[pathlib.Path] = None, mkdocs_path: Optional[pathlib.Path] = None) -> None:
    """
    Read src_path, compute front‑matter, and write the result to the
    corresponding location under dst_root (preserving sub‑directories) or
    update the file in place if in_place is True.
    Processes all files, including blank ones and those with existing front-matter.
    """
    try:
        raw = load_markdown(src_path)
    except Exception as e:
        print(f"⚠️  Error reading {src_path}: {e}, treating as empty")
        raw = ""

    # Strip existing front-matter if present (we'll regenerate it)
    content = raw
    if content.lstrip().startswith("---"):
        # Find the end of the front-matter block
        lines = content.splitlines()
        if len(lines) > 0 and lines[0].strip() == "---":
            # Look for the closing ---
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    # Skip the front-matter and any blank lines after it
                    content = "\n".join(lines[i+1:]).lstrip()
                    if content and not content.startswith("\n"):
                        content = "\n" + content
                    break

    # Handle empty/blank files
    if not content.strip():
        content = ""

    # ----- Title -------------------------------------------------------
    # Check if this is a MyRocks-related file
    is_myrocks = src_path.stem.lower().startswith("myrocks")
    
    heading = extract_first_heading(content)
    if heading:
        # Only add "RocksDB: " prefix for MyRocks files
        title = f"RocksDB: {heading}" if is_myrocks else heading
    else:
        # Generate title from filename
        title = src_path.stem.replace("_", " ").replace("-", " ").title()
        if not title:
            title = "Untitled"
        # Only add "RocksDB: " prefix for MyRocks files
        if is_myrocks:
            title = f"RocksDB: {title}"

    # ----- Status -------------------------------------------------------
    # For empty files, default to stable
    if not content.strip():
        status = DEFAULT_STATUS
    else:
        status = "tech-preview" if is_tech_preview(content) else DEFAULT_STATUS

    # ----- Determine introduced_in version ------------------------------
    file_introduced_in = introduced_in
    if use_git and repo_root:
        git_version = get_git_introduced_version(src_path, repo_root)
        if git_version:
            file_introduced_in = git_version
        else:
            # Git couldn't determine version (e.g., pre-8.4 files)
            # Only use fallback if provided, otherwise leave empty
            if introduced_in:
                file_introduced_in = introduced_in
            else:
                # No version determined - this will need manual review
                file_introduced_in = ""
    
    # Extract "since" from introduced_in (e.g., "8.4.6-6" -> "8.4")
    since = None
    if file_introduced_in:
        # Extract major.minor from version (e.g., "8.4.6-6" -> "8.4")
        match = re.match(r'^(\d+\.\d+)', file_introduced_in)
        if match:
            since = match.group(1)
    
    # ----- Gather all front-matter data ----------------------------------
    description = extract_description(content)
    slug = generate_slug(src_path)
    category, section = get_category_and_section(src_path, mkdocs_path)
    last_modified = get_last_modified(src_path, repo_root) if repo_root else None
    tags = generate_tags(content, src_path.name)
    
    # Map status to stability and technical_preview
    stability = "stable" if status == "stable" else "tech-preview"
    technical_preview = (status == "tech-preview")
    
    # Extract technical preview variables and values (even if doc itself is stable)
    technical_preview_items = extract_technical_preview_items(content)
    # Only include if there are items found
    if not technical_preview_items.get("variables") and not technical_preview_items.get("values"):
        technical_preview_items = None
    
    # Default author
    author = "Percona Documentation Team"
    
    # ----- Build front‑matter -------------------------------------------
    yaml_block = build_front_matter(
        title=title,
        description=description,
        slug=slug,
        category=category,
        section=section,
        since=since,
        stability=stability,
        technical_preview=technical_preview,
        tags=tags,
        author=author,
        last_modified=last_modified,
        draft=False,
        technical_preview_items=technical_preview_items
    )
    
    # Ensure proper spacing between front-matter and content
    if content.strip():
        new_content = f"---\n{yaml_block}---\n\n{content}"
    else:
        # For blank files, just add front-matter
        new_content = f"---\n{yaml_block}---\n"

    # ----- Write to destination or update in place ---------------------
    if in_place:
        # Update the source file directly
        src_path.write_text(new_content, encoding="utf-8")
        output_path = src_path
    else:
        # Preserve the relative path under the source root.
        rel_path = src_path.relative_to(src_root)
        dst_path = dst_root / rel_path
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        dst_path.write_text(new_content, encoding="utf-8")
        output_path = dst_path
    
    if not content.strip():
        print(f"✅ {src_path} → {output_path} (status={status}, blank file)")
    else:
        print(f"✅ {src_path} → {output_path} (status={status})")


# ----------------------------------------------------------------------
# Argument parsing & main driver
# ----------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add Lumo front‑matter to Percona‑Server Markdown files "
                    "and write the transformed files to a separate directory."
    )
    parser.add_argument(
        "--src",
        default="docs/percona-server/8.4",
        help="Source directory containing the original *.md files (default: %(default)s)",
    )
    parser.add_argument(
        "--dst",
        default=None,
        help="Destination directory where transformed files will be written (required unless --in-place is used)",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Update files in place instead of writing to a destination directory",
    )
    parser.add_argument(
        "--introduced-in",
        default=None,
        help="Version string for the 'introduced_in' field in front-matter (used as fallback if --use-git is enabled)",
    )
    parser.add_argument(
        "--use-git",
        action="store_true",
        help="Use git to automatically determine introduced_in version for each file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    src_root = pathlib.Path(args.src).resolve()
    
    if not args.in_place and not args.dst:
        print("❌ Error: Either --dst must be specified or --in-place must be used")
        sys.exit(1)
    
    if not args.use_git and not args.introduced_in:
        print("❌ Error: --introduced-in is required unless --use-git is enabled")
        sys.exit(1)
    
    # If using git, introduced_in is optional (only used as fallback for files git can't determine)
    if args.use_git:
        print(f"ℹ️  Using git to determine versions (fallback: {args.introduced_in or 'none'})")
    
    # Find git repository root
    repo_root = None
    if args.use_git:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=src_root,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                repo_root = pathlib.Path(result.stdout.strip())
                print(f"📦 Using git repository at {repo_root}")
            else:
                print("⚠️  Not in a git repository, --use-git will be ignored")
                args.use_git = False
        except Exception:
            print("⚠️  Could not detect git repository, --use-git will be ignored")
            args.use_git = False

    if not src_root.exists():
        print(f"❌ Source directory does not exist: {src_root}")
        sys.exit(1)

    if not src_root.is_dir():
        print(f"❌ Source path is not a directory: {src_root}")
        sys.exit(1)

    # Find all Markdown files recursively
    all_md_files = list(src_root.rglob("*.md"))
    
    # Filter out release-notes files
    md_files = [f for f in all_md_files if "release-notes" not in f.parts]
    
    if not md_files:
        print(f"⚠️  No Markdown files found in {src_root} (excluding release-notes)")
        return
    
    skipped_count = len(all_md_files) - len(md_files)
    if skipped_count > 0:
        print(f"ℹ️  Skipping {skipped_count} release-notes file(s)")

    if args.in_place:
        print(f"📁 Processing {len(md_files)} Markdown file(s) in place from {src_root}\n")
        dst_root = None
    else:
        dst_root = pathlib.Path(args.dst).resolve()
        print(f"📁 Processing {len(md_files)} Markdown file(s) from {src_root}")
        print(f"📁 Writing to {dst_root}\n")

    # Try to find mkdocs.yml or mkdocs-base.yml
    mkdocs_path = None
    for mkdocs_file in ["mkdocs.yml", "mkdocs-base.yml"]:
        potential_path = src_root.parent / mkdocs_file
        if potential_path.exists():
            mkdocs_path = potential_path
            break
    
    introduced_in = args.introduced_in or ""
    for md_file in md_files:
        try:
            process_file(md_file, src_root, dst_root, in_place=args.in_place, 
                        introduced_in=introduced_in, use_git=args.use_git, 
                        repo_root=repo_root, mkdocs_path=mkdocs_path)
        except Exception as e:
            print(f"❌ Error processing {md_file}: {e}")
            continue

    print(f"\n✅ Done! Processed {len(md_files)} file(s)")


if __name__ == "__main__":
    main()