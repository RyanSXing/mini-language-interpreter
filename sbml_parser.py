tokens = (
  'INT','REAL','STRING','BOOL',
  'LPAREN','RPAREN','LBRACK', 'RBRACK', 'COMMA', 'HASH',
  'EXP', 'TIMES', 'DIV','INTDIV', 'MOD', 'PLUS', 'MINUS',
  'IN', 'CONS',
  'NOT', 'ANDALSO', 'ORELSE',
  'LESSTHAN', 'LESSTHANEQUAL', 'EQUALSTO', 'NOTEQUAL', 'GREATERTHANEQUAL', 'GREATERTHAN'
)

t_LESSTHANEQUAL     = r'<='
t_GREATERTHANEQUAL  = r'>='
t_EQUALSTO          = r'=='
t_NOTEQUAL          = r'<>'
t_LESSTHAN          = r'<'
t_GREATERTHAN       = r'>'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_COMMA   = r','
t_HASH    = r'\#'

t_EXP     = r'\*\*'
t_TIMES   = r'\*'
t_DIV     = r'/'
t_INTDIV  = r'div'
t_MOD     = r'mod'
t_PLUS    = r'\+'
t_MINUS   = r'-'

t_IN      = r'in'
t_CONS    = r'::'
t_NOT     = r'not'
t_ANDALSO = r'andalso'
t_ORELSE  = r'orelse'

def t_STRING(t):
    r'(?:"[^"\n]*"|\'[^\'\n]*\')'
    t.value = t.value[1:-1]  
    return t

def t_BOOL(t):
  r'True|False'
  t.value = (t.value == 'True')
  return t

def t_REAL(t):
  r'((\d+\.\d*)|(\.\d+)|(\d+\.\d+))([eE][+-]?\d+)?'
  try:
    t.value = float(t.value)
  except ValueError:
    print("Integer value too large %d", t.value)
    t.value = 0.0
  return t

def t_INT(t):
  r'\d+'
  try:
    t.value = int(t.value)
  except:
    print("Integer value too large %d", t.value)
    t.value = 0
  return t



t_ignore = " \t"

def t_newline(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_error(t):
  #print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

import ply.lex as lex 
lexer = lex.lex()

precedence = (
  ('left', 'ORELSE'),
  ('left', 'ANDALSO'),
  ('right', 'NOT'),
  ('nonassoc', 'LESSTHAN', 'LESSTHANEQUAL','EQUALSTO','NOTEQUAL','GREATERTHANEQUAL','GREATERTHAN'),
  ('right', 'CONS'),
  ('left', 'IN'),
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES','DIV','INTDIV','MOD'),
  ('right', 'EXP'),
  ('left', 'HASH'),
  ('left', 'LBRACK', 'RBRACK')
)

import sbml_ast as ast

start = 'expr'

def p_expr_int(t):
  'expr : INT'
  t[0] = ast.Int(t[1])

def p_expr_real(t):
  'expr : REAL'
  t[0] = ast.Real(t[1])

def p_expr_str(t):
  'expr : STRING'
  t[0] = ast.String(t[1])

def p_expr_bool(t):
  'expr : BOOL'
  t[0] = ast.Bool(t[1])

def p_expr_paren(t):
  'expr : LPAREN expr RPAREN'
  t[0] = t[2]

def p_expr_singleton_tuple(t):
  'expr : LPAREN expr COMMA RPAREN'
  t[0] = ast.Tuple([t[2]])

def p_expr_tuple(t):
  'expr : LPAREN expr COMMA tuple_list RPAREN'
  t[0] = ast.Tuple([t[2]] + t[4])

def p_tuple_list(t):
  'tuple_list : expr COMMA tuple_list'
  t[0] = [t[1]] + t[3]

def p_tuple_list_end(t):
  'tuple_list : expr'
  t[0] = [t[1]]

def p_expr_empty_list(t):
  'expr : LBRACK RBRACK'
  t[0] = ast.List([])

def p_expr_list(t):
  'expr : LBRACK list_elements RBRACK'
  t[0] = ast.List(t[2])

def p_list_elements(t):
  'list_elements : expr COMMA list_elements'
  t[0] = [t[1]] + t[3]

def p_list_elements_end(t):
  'list_elements : expr' 
  t[0] = [t[1]]

def p_expr_binop(t):
  '''expr : expr PLUS expr
          | expr MINUS expr
          | expr TIMES expr
          | expr EXP expr
          | expr DIV expr
          | expr INTDIV expr
          | expr MOD expr
          | expr ANDALSO expr
          | expr ORELSE expr
          | expr EQUALSTO expr
          | expr NOTEQUAL expr
          | expr LESSTHAN expr
          | expr LESSTHANEQUAL expr
          | expr GREATERTHAN expr
          | expr GREATERTHANEQUAL expr
          | expr CONS expr
          | expr IN expr'''
  t[0] = ast.BinOp(t[2], t[1], t[3])

def p_expr_index(t):
  'expr : expr LBRACK expr RBRACK'
  t[0] = ast.Index(t[1], t[3])

def p_expr_tuple_index(t):
  'expr : HASH INT LPAREN expr RPAREN'
  t[0] = ast.TupleIndex(t[4], ast.Int(t[2]))

def p_expr_unary_not(t):
  'expr : NOT expr'
  t[0] = ast.UnaryOp('not', t[2])

def p_expr_unary_minus(t):
  'expr : MINUS expr %prec NOT'
  t[0] = ast.UnaryOp('-', t[2])

def p_error(t):
  raise SyntaxError("SYNTAX ERROR")

import ply.yacc as yacc
parser = yacc.yacc()

def parse_line(s):
  return parser.parse(s)