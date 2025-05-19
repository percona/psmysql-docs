"""
generate_yaml.py

This script extracts variable names from a Markdown file and generates a structured YAML file.

# ------------------------------
# How to Use This Script
# ------------------------------

1. Make sure the input Markdown file exists at: docs/variables.md  
   The file must contain links formatted like this:
   [`VARIABLE_NAME`](#variable_name)

2. Run the script using Python 3.11:

   $ python3.11 generate_yaml.py

3. The script creates (or overwrites) a YAML file named:
   myrocks-variables.yaml

This YAML file can be used as a source of structured variable names for generating documentation tables.
"""

import re
import yaml

def parse_variables_from_md(md_file):
    """
    Extracts variable names from a Markdown file and builds a dictionary.
        
    This function looks for Markdown link patterns like:
    [`VARIABLE_NAME`](#variable_name)
    """
    variables = {}

    with open(md_file, "r") as file:
        md_content = file.read()

        # Regex pattern to extract variable names and links
        pattern = r'\[`([a-zA-Z0-9_]+)`\]\(#([a-zA-Z0-9_]+)\)'
        
        matches = re.findall(pattern, md_content)
        
        # Loop through matches and format them into a dictionary
        for match in matches:
            variable_name, link = match
            # The link itself could be used as the description or you can format it
            description = f"Link: {link}"  # Or customize description extraction logic as needed
            variables[variable_name] = description
    
    return variables

def write_yaml(variables, yaml_file):
    """
    Writes the extracted variable dictionary to a YAML file.
    """
    with open(yaml_file, "w") as file:
        yaml.dump(variables, file, default_flow_style=False)

def main():
    md_file = "docs/variables.md"  # Path to the markdown file
    yaml_file = "myrocks-variables.yaml"  # Output YAML file

    variables = parse_variables_from_md(md_file)
    write_yaml(variables, yaml_file)

    print(f"YAML file '{yaml_file}' has been generated successfully.")

if __name__ == "__main__":
    main()