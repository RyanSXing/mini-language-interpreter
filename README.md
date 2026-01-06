# SBML Interpreter

Interpreter for a small block-structured language (SBML), written in Python.
It parses SBML source code into an abstract syntax tree (AST) and evaluates it with support for variables, expressions, conditionals, loops, and user-defined functions.

> Example: computing the greatest common divisor (GCD)
> **Input:**
>
> ```sbml
> fun gcd(a, b) =
> {
>   t = b;
>   b = a mod b;
>   if (b == 0)
>   {
>     output = t;
>   }
>   else
>   {
>     output = gcd(t, b);
>   }
> }
> output;
> {
>   print(gcd(32, 18));
> }
> ```
>
> **Output:**
>
> ```text
> 2
> ```

---

## Features

* **Lexer & Parser**

  * Tokenizes SBML source code.
  * Builds an AST for programs, blocks, statements, and expressions.

* **AST Evaluation**

  * Environment stack for variables and scopes.
  * Function definitions and recursive calls.
  * `output` variable used to return values from functions.

* **Language Constructs**

  * Integer variables and assignments.
  * Arithmetic: `+`, `-`, `*`, `/`, `mod`
  * Comparisons: `==`, `!=`, `<`, `<=`, `>`, `>=`
  * `if` / `else`
  * `while` loops
  * `fun` function definitions
  * `print(...)` built-in

* **Semantic Error Checking**

  * Duplicate function names.
  * Invalid programs (parser / semantic errors) reported as `SEMANTIC ERROR` (following the assignment spec).

---

## Project Structure

```text
.
├── sbml_ast.py      # AST node classes and evaluation logic
├── sbml_parser.py   # Lexer and parser that build the AST
├── sbml_main.py     # Command-line entry point / driver
└── CSE307-S20-HWA05.pdf  # Original assignment specification (optional)
```

---

## Getting Started

### Prerequisites

* Python 3.x

No external dependencies should be required beyond the standard library.

### Running the Interpreter

Depending on how `sbml_main.py` is written, you’ll typically run the interpreter in one of these ways:

1. **Passing a source file as an argument**

   ```bash
   python3 sbml_main.py program.sbml
   ```

2. **Reading SBML from standard input**

   ```bash
   python3 sbml_main.py < program.sbml
   ```

On semantic or parsing errors, the interpreter prints:

```text
SEMANTIC ERROR
```

as required by the assignment.

---

## Example

Create a file `gcd.sbml`:

```sbml
fun gcd(a, b) =
{
  t = b;
  b = a mod b;
  if (b == 0)
  {
    output = t;
  }
  else
  {
    output = gcd(t, b);
  }
}
output;
{
  print(gcd(32, 18));
}
```

Run:

```bash
python3 sbml_main.py gcd.sbml
```

Expected output:

```text
2
```

---

## Implementation Details

* **Program Loading**

  * `sbml_main.py` reads the entire SBML program, passes it to the parser, and then evaluates the resulting `Program` object.

* **Function Table**

  * All function definitions are collected before program execution (e.g., in a global `FUNCTIONS` dictionary).
  * Duplicate function names raise a semantic error.

* **Environments / Scopes**

  * An environment stack tracks variable bindings.
  * New blocks and function calls push a new environment; exiting them pops it.
  * This supports nested scopes and recursion.

* **Error Handling**

  * Parsing or semantic issues raise custom exceptions (e.g., `SemanticError`).
  * The main driver catches these and prints `SEMANTIC ERROR` to match the spec.

---

## Possible Extensions

* Add more data types (strings, booleans as first-class values, arrays).
* Add `return` statements instead of using `output`.
* Improve error messages (line/column numbers, hints).
* Add a REPL (interactive prompt) for SBML.

---

## Acknowledgements

This interpreter was implemented as part of a programming languages course assignment based on a provided SBML specification. The language design and original problem description come from course materials; the parser, AST, and evaluator implementations are my own.
