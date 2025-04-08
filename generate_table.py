# -----------------------------------------------------------------------------
# Script: generate_table.py
#
# Description:
# Inserts a Markdown table of MyRocks variable names into `docs/variables.md`
# by reading `myrocks-variables.yaml` and preserving the structure of the
# original `variables.md.backup` file.
#
# Usage:
#   $ python3.11 generate_table.py
#
# Requirements:
#   - Python 3.11+
#   - PyYAML (`pip install pyyaml`)
#
# Input files:
#   - myrocks-variables.yaml: Contains the list of MyRocks variable names.
#   - docs/variables.md.backup: Original markdown content. Add or update 
#     variable references here. This script uses it as the base for the final file.
#
# Output file:
#   - docs/variables.md: Final markdown file with the inserted variable table.
# -----------------------------------------------------------------------------

import yaml
import re

def read_original_content(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Creating a new file.")
        return ""

def find_insertion_point(content):
    # Find the position after the bullet points in the introduction
    # This pattern looks for the last line that starts with a bullet point (*)
    bullet_matches = list(re.finditer(r'^\s*\*.*$', content, re.MULTILINE))
    
    if not bullet_matches:
        # If no bullet points found, look for the end of an introductory paragraph
        paragraph_ends = list(re.finditer(r'\n\n', content))
        if paragraph_ends:
            # Return the end of the first paragraph if no bullets found
            return paragraph_ends[0].end()
        else:
            # If no clear paragraphs, just append to the end
            return len(content)
    
    # Return the position after the last bullet point plus a newline
    last_bullet = bullet_matches[-1]
    return last_bullet.end()

def generate_variable_table():
    # Load the YAML file
    with open("myrocks-variables.yaml", "r") as f:
        variables = yaml.safe_load(f)
    
    # Sort the variable names alphabetically
    sorted_vars = sorted(variables.keys())
    
    # Generate Markdown table
    table_lines = ["| Variable |", "|----------|"]
    for var in sorted_vars:
        table_lines.append(f"| [`{var}`](#{var}) |")
    
    return "\n".join(table_lines)

def main():
    # Read the original content from variables.md.backup
    original_content = read_original_content("docs/variables.md.backup")
    
    # Find the appropriate insertion point
    insertion_point = find_insertion_point(original_content)
    
    # Generate the variable table
    variable_table = generate_variable_table()
    
    # Combine content with the table inserted at the appropriate position
    new_content = (
        original_content[:insertion_point] + 
        "\n\n" + variable_table + "\n\n" + 
        original_content[insertion_point:]
    )
    
    # Write the combined content back to variables.md
    with open("docs/variables.md", "w") as out:
        out.write(new_content)
    
    print("✅ Markdown table inserted into docs/variables.md while preserving existing content")

if __name__ == "__main__":
    main()
