import re

def parse_clauses(clauses):
    parsed_clauses = []
    for clause in clauses:
        clause = transform_clause(clause)
        parsed_clauses.append(set(re.split(r'\s*\|\|\s*', clause)))
    return parsed_clauses

def negate_query(query):
    query = transform_clause(query)
    negated_query = set()
    literals = re.split(r'\s*\|\|\s*', query)
    for literal in literals:
        if literal.startswith('not '):
            negated_query.add(literal[4:])
        else:
            negated_query.add(f'not {literal}')
    return negated_query

def transform_clause(clause):
    clause = clause.replace(' ', '')
    clause = re.sub(r'(\w+)=>([\w\(\)&|~]+)', r'(not \1 or \2)', clause)
    clause = re.sub(r'(\w+)<=>([\w\(\)&|~]+)', r'(\1 and \2) or (not \1 and not \2)', clause)
    clause = clause.replace('~', ' not ')
    clause = clause.replace('&', ' and ')
    clause = clause.replace('||', ' or ')
    return clause

def resolve(ci, cj):
    resolvents = []
    for di in ci:
        for dj in cj:
            if di == f'not {dj}' or f'not {di}' == dj:
                resolvent = (ci - {di}) | (cj - {dj})
                if not resolvent:
                    return [{}]
                resolvents.append(resolvent)
    return resolvents

def resolution_method(kb, query):
    clauses = parse_clauses(kb)
    negated_query = negate_query(query)
    clauses.append(negated_query)
    
    print("Initial Clauses:")
    for clause in clauses:
        print(clause)
    
    while True:
        new_resolvents = set()
        n = len(clauses)
        for i in range(n):
            for j in range(i + 1, n):
                resolvents = resolve(clauses[i], clauses[j])
                if {} in resolvents:
                    return True, len(clauses)
                new_resolvents.update(frozenset(resolvent) for resolvent in resolvents)
        
        print("New Resolvents:")
        for resolvent in new_resolvents:
            print(resolvent)
        
        if new_resolvents.issubset(set(map(frozenset, clauses))):
            return False, len(clauses)
        clauses.extend(map(set, new_resolvents))
