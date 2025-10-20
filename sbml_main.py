# sbml_main.py
# Name: [Your Name]
# Student ID: [Your Student ID]
# CSE 307 - Homework 03

import sys
import sbml_parser as p
from sbml_ast import SemanticError

def main():
    # Ensure correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python3 sbml_main.py [-P|-E] <input_file_name.txt>")
        return

    # Parse command-line arguments
    mode = sys.argv[1]
    input_file = sys.argv[2]

    if mode not in ['-P', '-E']:
        print("Invalid mode. Use -P for print or -E for evaluate.")
        return

    try:
        # Open the input file
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    # Process each line in the input file
    for line in lines:
        s = line.strip()
        if not s:
            continue  # Skip empty lines

        try:
            # Parse the line to construct the AST
            node = p.parse_line(s)
        except Exception:
          print("SYNTAX ERROR")
          continue

        if mode == '-P':
            try:
                node.evaluate()
                print(node)
            except SemanticError:
                print("SEMANTIC ERROR")
            except Exception as e:
                print(f"SEMANTIC ERROR")
            # Print the AST representation
        elif mode == '-E':
            try:
                # Evaluate the expression
                val = node.evaluate()
                # Print strings in quotes, as per the instructions
                print(repr(val) if isinstance(val, str) else val)
            except SemanticError:
                print("SEMANTIC ERROR")
            except Exception as e:
                print(f"SEMANTIC ERROR")

if __name__ == "__main__":
    main()