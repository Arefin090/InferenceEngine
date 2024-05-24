import re

class Expr:
    """A logical expression that can be a symbol or an operation applied to arguments."""
    def __init__(self, op, *args):
        self.op = str(op)
        self.args = list(map(expr, args))
    
    def __repr__(self):
        if len(self.args) == 0:  # Constant
            return self.op
        elif len(self.args) == 1:  # Unary operator
            return f'({self.op}{self.args[0]})'
        else:  # Binary operator
            return f'({self.args[0]} {self.op} {self.args[1]})'

def expr(s):
    """Convert a string into an expression."""
    if isinstance(s, Expr):
        return s
    s = s.replace(' ', '')
    if s.isalnum():
        return Expr(s)
    s = re.sub(r'([()~&|<=>])', r' \1 ', s)
    tokens = s.split()
    return parse_expr(tokens)

def parse_expr(tokens):
    """Parse tokens into an expression."""
    def parse_sub_expr():
        token = tokens.pop(0)
        if token == '(':
            sub_expr = parse_sub_expr()
            tokens.pop(0)  # remove ')'
            return sub_expr
        elif token == '~':
            return Expr('~', parse_sub_expr())
        else:
            return Expr(token)

    def parse_tokens():
        if not tokens:
            return None
        left = parse_sub_expr()
        while tokens and tokens[0] in ('&', '|', '=>', '<=>'):
            op = tokens.pop(0)
            right = parse_sub_expr()
            left = Expr(op, left, right)
        return left

    return parse_tokens()

def eliminate_implications(s):
    """Change implications into equivalent form with only &, |, and ~ as logical operators."""
    if not s.args or s.op.isalnum():
        return s  # Atoms are unchanged.
    args = list(map(eliminate_implications, s.args))
    a, b = args[0], args[-1]
    if s.op == '=>':
        return Expr('|', Expr('~', a), b)
    elif s.op == '<=>':
        return Expr('&', Expr('|', Expr('~', a), b), Expr('|', Expr('~', b), a))
    elif s.op == '~':
        return Expr('~', a)
    else:
        return Expr(s.op, *args)

def move_not_inwards(s):
    """Rewrite sentence s by moving negation sign inward."""
    if s.op == '~':
        def NOT(b):
            return move_not_inwards(Expr('~', b))
        a = s.args[0]
        if a.op == '~':
            return move_not_inwards(a.args[0])  # ~~A ==> A
        if a.op == '&':
            return Expr('|', *map(NOT, a.args))
        if a.op == '|':
            return Expr('&', *map(NOT, a.args))
        return s
    elif s.op.isalnum() or not s.args:
        return s
    else:
        return Expr(s.op, *map(move_not_inwards, s.args))

def distribute_and_over_or(s):
    """Given a sentence s consisting of conjunctions and disjunctions of literals, return an equivalent sentence in CNF."""
    if s.op == '|':
        s = associate('|', s.args)
        if s.op != '|':
            return distribute_and_over_or(s)
        if len(s.args) == 0:
            return False
        if len(s.args) == 1:
            return distribute_and_over_or(s.args[0])
        conj = next((arg for arg in s.args if arg.op == '&'), None)
        if not conj:
            return s
        others = [a for a in s.args if a is not conj]
        rest = associate('|', others)
        return associate('&', [distribute_and_over_or(Expr('|', c, rest)) for c in conj.args])
    elif s.op == '&':
        return associate('&', list(map(distribute_and_over_or, s.args)))
    else:
        return s

def associate(op, args):
    """Associate the same operation by flattening nested operations of the same type."""
    args = dissociate(op, args)
    if len(args) == 0:
        return False
    if len(args) == 1:
        return args[0]
    return Expr(op, *args)

def dissociate(op, args):
    """Dissociate a set of arguments for a given operator."""
    result = []
    for arg in args:
        if arg.op == op:
            result.extend(dissociate(op, arg.args))
        else:
            result.append(arg)
    return result

def to_cnf(s):
    """Convert a propositional logical sentence to conjunctive normal form."""
    s = expr(s)
    print(f"Expression: {s}")
    s = eliminate_implications(s)
    print(f"After eliminating implications: {s}")
    s = move_not_inwards(s)
    print(f"After moving NOT inwards: {s}")
    s = distribute_and_over_or(s)
    print(f"CNF: {s}")
    return s

def parse_clauses(knowledge_base):
    """Parse the knowledge base into a list of clauses."""
    clauses = []
    for sentence in knowledge_base:
        sentence = to_cnf(sentence)
        conjuncts = dissociate('&', [sentence])
        for conjunct in conjuncts:
            disjuncts = dissociate('|', [conjunct])
            clauses.append(set(map(str, disjuncts)))
    return clauses

def negate_query(query):
    """Negate the query and return it as a clause."""
    query_expr = expr(query)
    negated_query = move_not_inwards(Expr('~', query_expr))
    negated_clauses = dissociate('&', [negated_query])
    return [set(map(str, dissociate('|', [clause]))) for clause in negated_clauses]

def resolve(clause1, clause2):
    """Resolve two clauses and return the resolvents."""
    resolvents = []
    for literal in clause1:
        if literal.startswith('~'):
            complement = literal[1:]
        else:
            complement = '~' + literal
        if complement in clause2:
            resolvent = (clause1 | clause2) - {literal, complement}
            if len(resolvent) == 0:
                return [resolvent]
            resolvents.append(resolvent)
    return resolvents

def resolution_method(kb_sentences, query):
    """Apply the resolution algorithm to check if the query is entailed by the knowledge base."""
    kb_clauses = parse_clauses(kb_sentences)
    negated_query_clauses = negate_query(query)
    clauses = kb_clauses + negated_query_clauses

    new = set()
    steps = 0
    print("Initial Clauses:")
    for clause in clauses:
        print(clause)
    print("\nStarting Resolution Process...\n")
    while True:
        steps += 1
        new = set()
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            print(f"Resolving {ci} and {cj} -> {resolvents}")
            if set() in resolvents:  # Found an empty clause
                print("\nEmpty clause found. The query is entailed by the KB.")
                return True, steps
            new.update(frozenset(resolvent) for resolvent in resolvents)
        if new.issubset(set(map(frozenset, clauses))):  # No new clauses added
            print("\nNo new clauses added. The query is not entailed by the KB.")
            return False, steps
        clauses.extend(map(set, new))

