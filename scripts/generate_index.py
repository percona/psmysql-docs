#!/usr/bin/env python3

"""
generate_index.py - Generate an index of Markdown files in the top-level docs/ directory.

How to run:

    cd scripts
    python3 generate_index.py

Run from the root directory of your project.
"""

import os

def strip_prefixes(s):
    prefixes = ('The ', 'Work with ')
    s_lower = s.lower()
    for prefix in prefixes:
        if s_lower.startswith(prefix.lower()):
            return s[len(prefix):]
    return s

# Define path to docs/ and the output file
script_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.abspath(os.path.join(script_dir, '..', 'docs'))
index_file_path = os.path.join(docs_dir, 'index-contents.md')

# Files to exclude
exclude_files = {'404.md', 'index-contents.md'}

# Delete old index file
if os.path.exists(index_file_path):
    os.remove(index_file_path)
    print(f"Deleted existing index file: {index_file_path}")

index_content = '# Index\n\n'

# Only list .md files in the top-level docs directory
file_entries = []

for file in os.listdir(docs_dir):
    if file.endswith('.md') and file not in exclude_files:
        filepath = os.path.join(docs_dir, file)
        relative_path = os.path.relpath(filepath, docs_dir).replace(os.sep, '/')

        display_name = ''
        try:
            with open(filepath, 'r', encoding='utf-8') as md_file:
                for line in md_file:
                    if line.strip().startswith('# '):
                        display_name = line.strip()[2:].strip()
                        break
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            continue

        if not display_name:
            display_name = os.path.splitext(file)[0]

        sort_key = strip_prefixes(display_name).strip().lower()
        file_entries.append((sort_key, display_name, relative_path))

file_entries.sort()

for _, display_name, relative_path in file_entries:
    index_content += f'- [{display_name}]({relative_path})\n'

# Write the new index
with open(index_file_path, 'w', encoding='utf-8') as index_file:
    index_file.write(index_content)

print(f"Index generated at {index_file_path}")