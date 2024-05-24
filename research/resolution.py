class Expr:
    def __init__(self, op, *args):
        self.op = op # Operator of the expressions
        self.args = args # Arguments of the expressions

    def __repr__(self):
        if not self.args: # If there are no arguments, return the operator itself
            return self.op
        elif len(self.args) == 1: # Unary Operator
            return self.op + repr(self.args[0])
        else: # Binary Operator
            return '(' + (' ' + self.op + ' ').join(map(repr, self.args)) + ')'

    def __invert__(self):
        return Expr('~', self) # Negation

    def __or__(self, other):
        return Expr('|', self, other) # Disjunction

    def __and__(self, other):
        return Expr('&', self, other) # Conjunction

    def __eq__(self, other):
        return Expr('<=>', self, other) # Equivalence 

    def __rshift__(self, other):
        return Expr('==>', self, other) # Implication

    def __lshift__(self, other):
        return Expr('<==', self, other) # Reverse Implication

def expr(x):
    if isinstance(x, Expr):
        return x
    elif isinstance(x, str):
        return Expr(x) # Convert string to Expr
    raise ValueError(f"Cannot convert {x} to an Expr")

def is_symbol(s):
    return isinstance(s, str) and s[0].isalpha() # Check if string is a symbol

def unique(seq):
    return list(set(seq)) # Return unique elements in a sequence 

def remove_all(item, seq):
    return [x for x in seq if x != item] # Remove all instances of item from sequence

def to_cnf(s):
    s = expr(s)
    s = eliminate_implications(s) # Eliminate Implications
    s = move_not_inwards(s) # Move negation inwards
    return distribute_and_over_or(s) # Distribute AND over OR

def eliminate_implications(s):
    s = expr(s)
    if not s.args or is_symbol(s.op):
        return s # Atoms are unchanged
    args = list(map(eliminate_implications, s.args))
    a, b = args[0], args[-1]
    if s.op == '==>':
        return b | ~a # p => q is equivalent to ~p | q
    elif s.op == '<==':
        return a | ~b # q <= p is equivalent to ~q | p
    elif s.op == '<=>':
        return (a | ~b) & (b | ~a) # p <=> q is equivalent to (p => q) & (q => p)
    elif s.op == '^':
        assert len(args) == 2
        return (a & ~b) | (~a & b) # p XOR q is equivalent to (p & ~q) | (~p & q)
    else:
        assert s.op in ('&', '|', '~') 
        return Expr(s.op, *args) # keep the same operator

def move_not_inwards(s):
    s = expr(s)
    if s.op == '~': # Negation
        def NOT(b):
            return move_not_inwards(~b)
        a = s.args[0]
        if a.op == '~':
            return move_not_inwards(a.args[0]) # ~~A is equivalent to A
        if a.op == '&':
            return associate('|', list(map(NOT, a.args))) # De morgan's law
        if a.op == '|':
            return associate('&', list(map(NOT, a.args))) # Same de morgan law
        return s
    elif is_symbol(s.op) or not s.args:
        return s # Returns if its a symbol or has no arguments
    else:
        return Expr(s.op, *list(map(move_not_inwards, s.args))) # Recursively  apply to arguments

def distribute_and_over_or(s):
    s = expr(s)
    if s.op == '|':
        s = associate('|', s.args)
        if s.op != '|':
            return distribute_and_over_or(s)
        if len(s.args) == 0:
            return False
        if len(s.args) == 1:
            return distribute_and_over_or(s.args[0])
        conj = first(arg for arg in s.args if arg.op == '&')
        if not conj:
            return s
        others = [a for a in s.args if a is not conj]
        rest = associate('|', others)
        return associate('&', [distribute_and_over_or(c | rest)
                               for c in conj.args])
    elif s.op == '&':
        return associate('&', list(map(distribute_and_over_or, s.args)))
    else:
        return s

def associate(op, args):
    args = dissociate(op, args)
    if len(args) == 0:
        return _op_identity[op]
    elif len(args) == 1:
        return args[0]
    else:
        return Expr(op, *args)

_op_identity = {'&': True, '|': False, '+': 0, '*': 1}

def dissociate(op, args):
    result = []

    def collect(subargs):
        for arg in subargs:
            if arg.op == op:
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result

def conjuncts(s):
    return dissociate('&', [s]) # Returns the conjuncts in the sentence

def disjuncts(s):
    return dissociate('|', [s]) # Return the disjuncts in the sentence
 
def pl_resolution(kb, alpha): 
    clauses = kb.clauses + conjuncts(to_cnf(~expr(alpha))) # Add negation of alpha to clauses
    new = set()
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj) # Resolve pairs of clauses
            if False in resolvents: # Found an empty clause
                return True
            new = new.union(set(resolvents))
        if new.issubset(set(clauses)): # No new clauses
            return False
        for c in new:
            if c not in clauses:
                clauses.append(c)

def pl_resolve(ci, cj):
    clauses = []
    for di in disjuncts(ci):
        for dj in disjuncts(cj):
            if di == ~dj or ~di == dj: # Complementary literals
                clauses.append(associate('|', unique(remove_all(di, disjuncts(ci)) + remove_all(dj, disjuncts(cj)))))
    return clauses

def parse_kb_and_query(file_content): # Separate parsing for simplicity
    lines = file_content.strip().split('\n')
    kb_sentences = []
    query = None
    mode = None

    for line in lines:
        if line.startswith('TELL'):
            mode = 'TELL'
            continue
        elif line.startswith('ASK'):
            mode = 'ASK'
            continue
        
        if mode == 'TELL':
            kb_sentences.append(line.strip().rstrip(';'))
        elif mode == 'ASK':
            query = line.strip().rstrip(';')

    return ' & '.join(kb_sentences), query



