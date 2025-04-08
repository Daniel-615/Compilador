
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CHAR COMMA DIVIDE DO DOT ELSE EQUALS FLOAT FOR GLOBAL GT IDENTIFIER IF INT LBRACE LOCAL LPAREN LT MINUS NUMBER PLUS QUOTE RBRACE RELOP RPAREN SEMICOLON TIMES WHILEprogram : statement\n| program statementstatement : declaration\n| assignment\n| while_loop\n| expression SEMICOLONdeclaration : GLOBAL INT IDENTIFIER SEMICOLON\n| LOCAL INT IDENTIFIER SEMICOLON\n| INT IDENTIFIER SEMICOLON\n| INT IDENTIFIER EQUALS expression SEMICOLONassignment : IDENTIFIER EQUALS expression SEMICOLONexpression : expression PLUS term\n| expression MINUS term\n| termterm : term TIMES factor\n| term DIVIDE factor\n| factorfactor : NUMBER\n| IDENTIFIERcondition : IDENTIFIER RELOP expressionwhile_loop : WHILE LPAREN condition RPAREN LBRACE program RBRACE'
    
_lr_action_items = {'GLOBAL':([0,1,2,3,4,5,15,16,30,38,40,41,44,45,47,48,],[7,7,-1,-3,-4,-5,-2,-6,-9,-7,-11,-8,-10,7,7,-21,]),'LOCAL':([0,1,2,3,4,5,15,16,30,38,40,41,44,45,47,48,],[10,10,-1,-3,-4,-5,-2,-6,-9,-7,-11,-8,-10,10,10,-21,]),'INT':([0,1,2,3,4,5,7,10,15,16,30,38,40,41,44,45,47,48,],[8,8,-1,-3,-4,-5,19,22,-2,-6,-9,-7,-11,-8,-10,8,8,-21,]),'IDENTIFIER':([0,1,2,3,4,5,8,15,16,17,18,19,21,22,23,24,25,30,31,38,40,41,43,44,45,47,48,],[9,9,-1,-3,-4,-5,20,-2,-6,27,27,29,27,33,35,27,27,-9,27,-7,-11,-8,27,-10,9,9,-21,]),'WHILE':([0,1,2,3,4,5,15,16,30,38,40,41,44,45,47,48,],[11,11,-1,-3,-4,-5,-2,-6,-9,-7,-11,-8,-10,11,11,-21,]),'NUMBER':([0,1,2,3,4,5,15,16,17,18,21,24,25,30,31,38,40,41,43,44,45,47,48,],[14,14,-1,-3,-4,-5,-2,-6,14,14,14,14,14,-9,14,-7,-11,-8,14,-10,14,14,-21,]),'$end':([1,2,3,4,5,15,16,30,38,40,41,44,48,],[0,-1,-3,-4,-5,-2,-6,-9,-7,-11,-8,-10,-21,]),'RBRACE':([2,3,4,5,15,16,30,38,40,41,44,47,48,],[-1,-3,-4,-5,-2,-6,-9,-7,-11,-8,-10,48,-21,]),'SEMICOLON':([6,9,12,13,14,20,26,27,28,29,32,33,36,37,39,],[16,-19,-14,-17,-18,30,-12,-19,-13,38,40,41,-15,-16,44,]),'PLUS':([6,9,12,13,14,26,27,28,32,36,37,39,46,],[17,-19,-14,-17,-18,-12,-19,-13,17,-15,-16,17,17,]),'MINUS':([6,9,12,13,14,26,27,28,32,36,37,39,46,],[18,-19,-14,-17,-18,-12,-19,-13,18,-15,-16,18,18,]),'EQUALS':([9,20,],[21,31,]),'TIMES':([9,12,13,14,26,27,28,36,37,],[-19,24,-17,-18,24,-19,24,-15,-16,]),'DIVIDE':([9,12,13,14,26,27,28,36,37,],[-19,25,-17,-18,25,-19,25,-15,-16,]),'LPAREN':([11,],[23,]),'RPAREN':([12,13,14,26,27,28,34,36,37,46,],[-14,-17,-18,-12,-19,-13,42,-15,-16,-20,]),'RELOP':([35,],[43,]),'LBRACE':([42,],[45,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,45,],[1,47,]),'statement':([0,1,45,47,],[2,15,2,15,]),'declaration':([0,1,45,47,],[3,3,3,3,]),'assignment':([0,1,45,47,],[4,4,4,4,]),'while_loop':([0,1,45,47,],[5,5,5,5,]),'expression':([0,1,21,31,43,45,47,],[6,6,32,39,46,6,6,]),'term':([0,1,17,18,21,31,43,45,47,],[12,12,26,28,12,12,12,12,12,]),'factor':([0,1,17,18,21,24,25,31,43,45,47,],[13,13,13,13,13,36,37,13,13,13,13,]),'condition':([23,],[34,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement','program',1,'p_program','parser.py',12),
  ('program -> program statement','program',2,'p_program','parser.py',13),
  ('statement -> declaration','statement',1,'p_statement','parser.py',20),
  ('statement -> assignment','statement',1,'p_statement','parser.py',21),
  ('statement -> while_loop','statement',1,'p_statement','parser.py',22),
  ('statement -> expression SEMICOLON','statement',2,'p_statement','parser.py',23),
  ('declaration -> GLOBAL INT IDENTIFIER SEMICOLON','declaration',4,'p_declaration','parser.py',27),
  ('declaration -> LOCAL INT IDENTIFIER SEMICOLON','declaration',4,'p_declaration','parser.py',28),
  ('declaration -> INT IDENTIFIER SEMICOLON','declaration',3,'p_declaration','parser.py',29),
  ('declaration -> INT IDENTIFIER EQUALS expression SEMICOLON','declaration',5,'p_declaration','parser.py',30),
  ('assignment -> IDENTIFIER EQUALS expression SEMICOLON','assignment',4,'p_assignment','parser.py',48),
  ('expression -> expression PLUS term','expression',3,'p_expression','parser.py',52),
  ('expression -> expression MINUS term','expression',3,'p_expression','parser.py',53),
  ('expression -> term','expression',1,'p_expression','parser.py',54),
  ('term -> term TIMES factor','term',3,'p_term','parser.py',61),
  ('term -> term DIVIDE factor','term',3,'p_term','parser.py',62),
  ('term -> factor','term',1,'p_term','parser.py',63),
  ('factor -> NUMBER','factor',1,'p_factor','parser.py',70),
  ('factor -> IDENTIFIER','factor',1,'p_factor','parser.py',71),
  ('condition -> IDENTIFIER RELOP expression','condition',3,'p_condition','parser.py',75),
  ('while_loop -> WHILE LPAREN condition RPAREN LBRACE program RBRACE','while_loop',7,'p_while_loop','parser.py',82),
]
