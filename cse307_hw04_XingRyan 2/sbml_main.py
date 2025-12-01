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

    try:
        root = p.parser.parse(source, lexer = p.lexer)
        if root is None:
            raise SyntaxError
    except:
        print("SYNTAX ERROR")
        return

    try:
        ENV.clear()
    except NameError:
        pass

    if mode == '-P':            
        try:

            ENV.clear()
            print(root)
        except SemanticError:
            print("SEMANTIC ERROR")
        except:
            print("SEMANTIC ERROR")
        return
    
        # try:
        #     root.evaluate()
        #     print(root)
        # except SemanticError:
        #     print("SEMANTIC ERROR")
        # except:
        #     print("SEMANTIC ERROR")
        # return

    if mode == '-E':
        try:

            ENV.clear()
            root.evaluate()
        except SemanticError:
            print("SEMANTIC ERROR")
        except:
            print("SEMANTIC ERROR")
        return

if __name__ == "__main__":
    main()