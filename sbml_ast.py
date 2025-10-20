class SemanticError(Exception):
  def __init__(self, message=None):
    super().__init__(message)
  
  def __str__(self):
    return "SEMANTIC ERROR"

  def __repr__(self):
    return "SEMANTIC ERROR"

def _is_int(x): return isinstance(x, int) and not isinstance(x, bool)
def _is_num(x): return isinstance(x, (int, float)) and not isinstance(x, bool)
def _is_str(x): return isinstance(x, str)
def _is_bool(x): return isinstance(x, bool)
def _is_List(x): return isinstance(x, list)
def _is_tuple(x): return isinstance(x, tuple)

class Node:
  def evaluate(self): raise NotImplementedError()
  def __str__(self):
    return self.__class__.__name__
  
class Int(Node):
  def __init__(self, v): self.value = int(v)
  def evaluate(self): return self.value
  def __str__(self):
    return  f"Int({self.value})"

class Real(Node):
  def __init__(self, v): self.value = float(v)
  def evaluate(self): return self.value
  def __str__(self):
    return  f"Real({self.value})"

class String(Node):
    def __init__(self, s): self.value = str(s)
    def evaluate(self):  return self.value
    def __str__(self):   
      return f"String('{self.value}')"

class Bool(Node):
    def __init__(self, b): self.value = bool(b)
    def evaluate(self): return self.value
    def __str__(self):     
      return f"Bool({self.value})"
    
class List(Node):
  def __init__(self, element_nodes): self.value = element_nodes
  def evaluate(self): return [e.evaluate() for e in self.value]
  def __str__(self):
    elements_str = ', '.join(str(node) for node in self.value)
    return f"List[{elements_str}]"

class Tuple(Node):
  def __init__(self, element_nodes): self.value = element_nodes
  def evaluate(self): return tuple([e.evaluate() for e in self.value])
  def __str__(self):
    elements_str = ', '.join(str(node) for node in self.value)
    return f"Tuple({elements_str})"
  
class BinOp(Node):
  def __init__(self, operator, left, right):
    self.operator = operator
    self.left = left
    self.right = right
  def evaluate(self): 
    left_value = self.left.evaluate()
    right_value = self.right.evaluate()

    if self.operator == '+':
      if _is_num(left_value) and _is_num(right_value):
        return left_value + right_value
      elif _is_str(left_value) and _is_str(right_value):
        return left_value + right_value
      elif _is_List(left_value) and _is_List(right_value):
        return left_value + right_value
      else: 
        raise SemanticError("Type missmatch for + operator")

    elif self.operator == '-':
      if _is_num(left_value) and _is_num(right_value):
        return left_value - right_value
      else: 
        raise SemanticError("Type missmatch for - operator")
      
    elif self.operator == '*':
      if _is_num(left_value) and _is_num(right_value):
        return left_value * right_value
      else: 
        raise SemanticError("Type missmatch for * operator")
      
    elif self.operator == '**':
      if _is_num(left_value) and _is_num(right_value):
        return left_value ** right_value
      else: 
        raise SemanticError("Type missmatch for ** operator")
      
    elif self.operator == '/':
      if right_value == 0:
        raise SemanticError("Division by zero error")
      elif _is_num(left_value) and _is_num(right_value) and right_value != 0:
        return float(left_value) / float(right_value)
      else: 
        raise SemanticError("Type missmatch for / operator")
      
    elif self.operator == 'div':
      if right_value == 0:
        raise SemanticError("Division by zero error")
      elif _is_int(left_value) and _is_int(right_value) and right_value != 0:
        return left_value // right_value
      else:
        raise SemanticError("Type missmatch for div operator")
      
    elif self.operator == 'mod':
      if right_value == 0:
        raise SemanticError("Division by zero error")
      elif _is_int(left_value) and _is_int(right_value) and right_value != 0:
        return left_value % right_value
      else:
        raise SemanticError("Type missmatch for mod operator")
    
    elif self.operator == 'andalso':
      if _is_bool(left_value) and _is_bool(right_value):
        return left_value and right_value
      else:
        raise SemanticError("Type missmatch for andalso operator")
      
    elif self.operator == 'orelse':
      if _is_bool(left_value) and _is_bool(right_value):
        return left_value or right_value
      else:
        raise SemanticError("Type missmatch for orelse operator") 
      
    elif self.operator == '==':
      if _is_num(left_value) and _is_num(right_value):
        return left_value == right_value
      elif _is_str(left_value) and _is_str(right_value):
        return left_value == right_value
      else:
        raise SemanticError("Type missmatch for == operator")
      
    elif self.operator == '<>':
      if _is_num(left_value) and _is_num(right_value):
        return left_value != right_value
      elif _is_str(left_value) and _is_str(right_value):
        return left_value != right_value
      else:
        raise SemanticError("Type missmatch for <> operator")
      
    elif self.operator == '<':
      if _is_num(left_value) and _is_num(right_value):
        return left_value < right_value
      elif _is_str(left_value) and _is_str(right_value):
        return left_value < right_value
      else:
        raise SemanticError("Type missmatch for < operator")

    elif self.operator == '<=':
      if _is_num(left_value) and _is_num(right_value):
        return left_value <= right_value
      elif _is_str(left_value) and _is_str(right_value):
        return left_value <= right_value
      else:
        raise SemanticError("Type missmatch for <= operator")
      
    elif self.operator == '>':
      if _is_num(left_value) and _is_num(right_value):
        return left_value > right_value
      elif _is_str(left_value) and _is_str(right_value):
        return left_value > right_value
      else:
        raise SemanticError("Type missmatch for > operator")
      
    elif self.operator == '>=':
      if _is_num(left_value) and _is_num(right_value):
        return left_value >= right_value
      elif _is_str(left_value) and _is_str(right_value):
        return left_value >= right_value
      else:
        raise SemanticError("Type missmatch for >= operator")
      
    elif self.operator == '::':
      if _is_List(right_value):
          return [left_value] + right_value
      else:
          raise SemanticError("Type mismatch for :: operator")
    
    elif self.operator == 'in':
      if _is_str(right_value) or _is_List(right_value):
        return left_value in right_value
      else: 
        raise SemanticError("Type mismatch for in operator")
    
    else:
      raise SemanticError(f"Unrecognized Operator: {self.operator}")
  
  def __str__(self):
    return f"BinOp(left:{str(self.left)} {self.operator} right:{str(self.right)})"
    
class UnaryOp(Node):
  def __init__(self, operator, operand):
    self.operator = operator
    self.operand = operand
  def evaluate(self):
      value = self.operand.evaluate()

      if self.operator == 'not':
        if _is_bool(value):
          return not value
        else:
          raise SemanticError("Type missmatch for not operator")
      elif self.operator == '-':
        if _is_num(value):
          return -value
        else: 
          raise SemanticError("Type missmatch for unary -")
      else:
        raise SemanticError(f"Unrecognized Operator: {self.operator}")
  def __str__(self):
    return f"UnaryOp({self.operator}, operand={self.operand})"

class Index(Node):
  def __init__(self, sequence, index):
    self.sequence = sequence
    self.index = index
  def evaluate(self):
    index_value = self.index.evaluate()
    sequence_value = self.sequence.evaluate()

    if _is_int(index_value):
      if _is_str(sequence_value):
        if index_value < 0 or index_value >= len(sequence_value):
          raise SemanticError("Index out of bounds")
        return sequence_value[index_value]
      elif _is_List(sequence_value):
        if index_value < 0 or index_value >= len(sequence_value):
          raise SemanticError("Index out of bounds")
        return sequence_value[index_value]
      else:
        raise SemanticError("Type mismatch sequence value must be a str or a list")
    else:
      raise SemanticError("Type mismatch index value must be a INT")
  def __str__(self):
    return f"Index({self.sequence}[{self.index}])"
  
class TupleIndex(Node):
  def __init__(self, tuple_sequence, index):
    self.tuple_sequence = tuple_sequence
    self.index = index
  def evaluate(self):
    index_value = self.index.evaluate()
    tuple_value = self.tuple_sequence.evaluate()

    if _is_int(index_value):
      if _is_tuple(tuple_value):
        if index_value < 1 or index_value > len(tuple_value):
          raise SemanticError("Index out of bounds")
        return tuple_value[index_value-1]
      else:
        raise SemanticError("Type mismatch sequence value must be a tuple")
    else:
      raise SemanticError("Type mismatch index value must be a INT")
  def __str__(self):
    return f"TupleIndex({self.tuple_sequence}[{self.index}])"
  