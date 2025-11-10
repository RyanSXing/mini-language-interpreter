#Ryan Xing 116607537

import sys
import sbml_parser as p
from sbml_ast import SemanticError, ENV

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
            source = file.read()
    except FileNotFoundError:
        print("Improper command line argument")
        return

    # 3. Parse once
    try:
        # parser is built inside sbml_parser
        # start symbol should be 'program'
        root = p.parser.parse(source, lexer = p.lexer)
        if root is None:
            raise SyntaxError
    except:
        print("SYNTAX ERROR")
        return

    # 4. Reset environment before execution/analysis
    try:
        ENV.clear()
    except NameError:
        # if ENV not imported / not used, ignore
        pass

    # 5. Mode: -P (pretty-print AST or SEMANTIC ERROR)
    if mode == '-P':
        try:
            # Evaluate to detect semantic issues (per your previous behavior)
            root.evaluate()
            print(root)
        except SemanticError:
            print("SEMANTIC ERROR")
        except:
            # Any unexpected runtime -> semantic error by spec convention
            print("SEMANTIC ERROR")
        return

    # 6. Mode: -E (execute program)
    if mode == '-E':
        try:
            # Block.evaluate() runs statements; Print nodes handle their own output.
            ENV.clear()
            root.evaluate()
        except SemanticError:
            print("SEMANTIC ERROR")
        except:
            print("SEMANTIC ERROR")
        return

if __name__ == "__main__":
    main()