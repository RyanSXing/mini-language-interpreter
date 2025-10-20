#Ryan Xing 116607537

import sys
import sbml_parser as p
from sbml_ast import SemanticError

def main():
    if len(sys.argv) != 3:
        print("Improper Command Line Argument")
        return

    mode = sys.argv[1]
    input_file = sys.argv[2]  

    if mode not in ['-P', '-E']:
        print("Improper Command Line Argument")
        return

    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    for line in lines:
        s = line.strip()
        if not s:
            continue 

        try:
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
        elif mode == '-E':
            try:
                val = node.evaluate()
                print(repr(val) if isinstance(val, str) else val)
            except SemanticError:
                print("SEMANTIC ERROR")
            except Exception as e:
                print(f"SEMANTIC ERROR")

if __name__ == "__main__":
    main()