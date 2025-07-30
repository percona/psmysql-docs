"""
Generate an A–Z documentation index that lists:
  * Markdown files (by title) grouped under their starting letter.
  * Keywords/phrases (from db_terms.txt) grouped under their starting letter,
    each linking to all docs in which the term appears.

What's new in this version
==========================
• **Multi‑word terms supported**: Lines in `db_terms.txt` may contain spaces (e.g., "tech preview", "storage engine").
• **Original capitalization preserved**: How you write the term in `db_terms.txt` is how it appears in the generated index.
• **Case‑insensitive matching**: Terms match regardless of capitalization in Markdown content.
• **Whitespace‑flexible phrase matching**: Internal whitespace in a term (spaces/tabs/newlines) is matched with `\s+` so a term can wrap lines in Markdown and still match.
• **Code blocks ignored**: Fenced code (``` ... ```) and inline code (`...`) are stripped before matching so code examples do not create false positives.
• **Backward compatible single‑word behavior**: Single tokens in `db_terms.txt` work exactly as before.

Usage
-----
1. Put your canonical keyword/phrase list (one per line) in `db_terms.txt`.
2. Run this script from the project root (the directory that contains `docs/`).
3. The script writes `docs/index-keywords.md`.

Notes / Recommendations
-----------------------
* Blank lines and lines that start with `#` (comment) in `db_terms.txt` are ignored.
* Duplicate terms (case-insensitive) keep the first casing encountered.
* If you have overlapping terms (e.g., "engine" and "storage engine"), **both** can be listed; each is matched independently.
* Very common short words (e.g., "the") will match widely—avoid including those.

"""

import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple, Pattern

DEBUG = False
DB_TERMS_FILE = "db_terms.txt"

# ---------------------------------------------------------------------------
# Loading & preparing DB terms
# ---------------------------------------------------------------------------

def load_db_terms() -> Dict[str, str]:
    """Load terms from DB_TERMS_FILE.

    Returns a dict mapping lowercase term -> *original* term string (trimmed),
    preserving the first capitalization seen.

    Lines that are blank or start with '#' are skipped.
    """
    if not os.path.exists(DB_TERMS_FILE):
        print(f"'{DB_TERMS_FILE}' not found. Creating an empty file.")
        open(DB_TERMS_FILE, 'w', encoding='utf-8').close()
        return {}

    terms: Dict[str, str] = {}
    with open(DB_TERMS_FILE, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            key = line.lower()
            # keep the *first* capitalization encountered for a given lowercase key
            terms.setdefault(key, line)
    return terms


# ---------------------------------------------------------------------------
# Content preprocessing (strip code blocks / inline code)
# ---------------------------------------------------------------------------

def strip_code(content: str) -> str:
    """Remove fenced and inline code segments from Markdown content.

    This reduces false positives when scanning for terms.
    """
    # Remove fenced code blocks ```...``` (greedy across newlines)
    content = re.sub(r"```[\s\S]*?```", " ", content)
    # Remove inline code `...`
    content = re.sub(r"`[^`]+`", " ", content)
    return content


# ---------------------------------------------------------------------------
# Build regex patterns for each term
# ---------------------------------------------------------------------------

def _term_to_regex(term: str) -> str:
    """Convert a term (possibly multi-word) to a regex string.

    Rules:
      * Match case-insensitively (applied when compiled).
      * Enforce word boundaries at start & end (\b) for alnum/underscore tokens.
      * Internal whitespace in the term becomes "\s+" in regex.
      * Other punctuation characters in the term are escaped literally.

    Examples:
      'MySQL' -> r'\bMySQL\b'
      'tech preview' -> r'\btech\s+preview\b'
      'xtrabackup-plugin' -> r'\bxtrabackup\-plugin\b'

    NOTE: If you *intentionally* want to match inside words, include a '*' at
    the start/end yourself and call this function differently. For now we keep
    it simple & safe.
    """
    # Split on whitespace to decide where to allow flexible spacing
    parts = re.split(r"\s+", term.strip())
    escaped_parts = [re.escape(p) for p in parts if p]
    if not escaped_parts:
        return ""  # shouldn't happen; caller guards

    body = r"\s+".join(escaped_parts) if len(escaped_parts) > 1 else escaped_parts[0]

    # Wrap with word boundaries. We deliberately use \b; this behaves well for
    # alnum/_ boundaries. If your term starts/ends with punctuation, \b may not
    # behave exactly as expected, but it's still usually fine. We could enhance
    # with lookarounds if needed later.
    return rf"\b{body}\b"


def build_term_patterns(db_terms: Dict[str, str]) -> Dict[str, Pattern[str]]:
    """Compile regex patterns (IGNORECASE) for each term.

    Returns dict mapping lowercase-term -> compiled Pattern.
    """
    patterns: Dict[str, Pattern[str]] = {}
    for lterm, orig in db_terms.items():
        regex_str = _term_to_regex(orig)
        if not regex_str:
            continue
        patterns[lterm] = re.compile(regex_str, re.IGNORECASE)
    return patterns


# ---------------------------------------------------------------------------
# Extract title from Markdown
# ---------------------------------------------------------------------------

def extract_title(content: str, filename: str) -> str:
    """Extract the first Markdown H1 (#) heading; fallback to filename."""
    match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    return match.group(1).strip() if match else filename


# ---------------------------------------------------------------------------
# Keyword/phrase detection in content
# ---------------------------------------------------------------------------

def extract_keywords(content: str, db_terms: Dict[str, str], patterns: Dict[str, Pattern[str]]) -> List[str]:
    """Return a list of *original-case* db terms found in content.

    Matching is case-insensitive; internal whitespace in the term is flexible.
    Code blocks and inline code are ignored.
    """
    text = strip_code(content)
    found: List[str] = []
    for lterm, pat in patterns.items():
        if pat.search(text):
            found.append(db_terms[lterm])  # original capitalization
    # Deduplicate while preserving original order
    seen = set()
    unique = []
    for t in found:
        if t.lower() in seen:
            continue
        seen.add(t.lower())
        unique.append(t)
    return sorted(unique, key=str.lower)


# ---------------------------------------------------------------------------
# Scan docs tree
# ---------------------------------------------------------------------------

def scan_markdown_files(
    docs_dir: str,
    db_terms: Dict[str, str],
    patterns: Dict[str, Pattern[str]],
) -> Tuple[List[Tuple[str, str]], Dict[str, List[str]], Dict[str, str]]:
    """Scan Markdown files and map found keywords to files.

    Returns:
        file_data   : list of (title, rel_path)
        keyword_map : term -> [rel_paths...]
        title_map   : rel_path -> title
    """
    file_data: List[Tuple[str, str]] = []
    keyword_map: Dict[str, List[str]] = defaultdict(list)
    title_map: Dict[str, str] = {}

    for root, _, files in os.walk(docs_dir):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            if filename == 'index-keywords.md':
                continue

            rel_path = os.path.relpath(os.path.join(root, filename), docs_dir)

            # Skip release notes subtree
            if rel_path.startswith("release-notes" + os.sep):
                continue

            full_path = os.path.join(root, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            title = extract_title(content, filename)
            kws = extract_keywords(content, db_terms, patterns)

            file_data.append((title, rel_path))
            title_map[rel_path] = title

            if DEBUG and kws:
                print(f"[DEBUG] {rel_path}: {kws}")

            for kw in kws:
                keyword_map[kw].append(rel_path)

    # Deduplicate and sort rel_paths per keyword
    for kw in keyword_map:
        keyword_map[kw] = sorted(set(keyword_map[kw]))

    return file_data, keyword_map, title_map


# ---------------------------------------------------------------------------
# Index generation
# ---------------------------------------------------------------------------

def generate_alphabetical_index(
    file_data: List[Tuple[str, str]],
    keyword_map: Dict[str, List[str]],
    title_map: Dict[str, str],
) -> str:
    """Generate the Markdown index grouped by initial letter."""
    index_content = "# Documentation Index by Alphabet\n\n"

    # Group files by first letter of title
    files_by_letter: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for title, path in file_data:
        letter = title[0].upper() if title else '#'
        files_by_letter[letter].append((title, path))

    # Group keywords by first letter (use display case; safe to index 0)
    kws_by_letter: Dict[str, List[str]] = defaultdict(list)
    for kw in keyword_map.keys():
        letter = kw[0].upper() if kw else '#'
        kws_by_letter[letter].append(kw)

    for letter in (chr(c) for c in range(ord('A'), ord('Z') + 1)):
        files = files_by_letter.get(letter, [])
        kws = kws_by_letter.get(letter, [])
        if not files and not kws:
            continue

        index_content += f"## {letter}\n\n"

        if files:
            index_content += "**Files:**\n\n"
            for title, path in sorted(files, key=lambda x: x[0].lower()):
                index_content += f"* [{title}]({path})\n"
            index_content += "\n"

        if kws:
            index_content += "**Keywords:**\n\n"
            for kw in sorted(kws, key=str.lower):
                linked_titles = ", ".join(
                    f"[{title_map[p]}]({p})" for p in keyword_map[kw]
                )
                index_content += f"* **{kw}** — {linked_titles}\n"
            index_content += "\n"

    return index_content


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    docs_dir = 'docs'

    if not os.path.exists(docs_dir):
        print(f"Error: '{docs_dir}' not found.")
        return

    db_terms = load_db_terms()  # lower -> original
    patterns = build_term_patterns(db_terms)

    file_data, keyword_map, title_map = scan_markdown_files(docs_dir, db_terms, patterns)
    index_content = generate_alphabetical_index(file_data, keyword_map, title_map)

    index_path = os.path.join(docs_dir, 'index-keywords.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f"A–Z index with titles and keyword links generated: {index_path}")


if __name__ == "__main__":
    main()
