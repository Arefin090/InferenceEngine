import re
from itertools import product

# Function to parse the input file and extract the knowledge base (KB) and query
def parse_file(filename):
    with open(filename, 'r') as file:
        content = file.read().splitlines()
    tell_index = content.index('TELL')
    ask_index = content.index('ASK')
    knowledge_base = [line.strip() for line in content[tell_index + 1:ask_index][0].split(';') if line.strip()]
    query = content[ask_index + 1].strip()
    return knowledge_base, query

# Function to extract all unique symbols from the KB and query
def extract_symbols(kb, query):
    symbols = set()
    pattern = re.compile(r'\b\w+\b')
    for sentence in kb:
        symbols.update(pattern.findall(sentence))
    symbols.update(pattern.findall(query))
    return list(symbols)

# Function to generate all possible truth assignments for the symbols
def generate_models(symbols):
    return [dict(zip(symbols, values)) for values in product([True, False], repeat=len(symbols))]

# Function to correctly replace logical operators and symbols in a sentence
def transform_sentence(sentence, model):
    for symbol, value in model.items():
        sentence = re.sub(r'\b{}\b'.format(symbol), str(value), sentence)
    sentence = sentence.replace('~', ' not ')
    sentence = sentence.replace('&', ' and ')
    sentence = sentence.replace('|', ' or ')
    sentence = re.sub(r'(\w+)\s*=>\s*([\w\s\(\)&|~]+)', r'(not \1 or \2)', sentence)
    sentence = re.sub(r'(\w+)\s*<=>\s*([\w\s\(\)&|~]+)', r'(\1 == \2)', sentence)
    sentence = re.sub(r'(\([\w\s\(\)&|~]+\))\s*=>\s*([\w\s\(\)&|~]+)', r'(not \1 or \2)', sentence)
    sentence = re.sub(r'(\([\w\s\(\)&|~]+\))\s*<=>\s*([\w\s\(\)&|~]+)', r'(\1 == \2)', sentence)
    return sentence

# Function to evaluate the KB under a given model
def evaluate_kb(kb, model):
    return all(evaluate_clause(clause, model) for clause in kb)

# Helper function to evaluate a single clause under a given model
def evaluate_clause(clause, model):
    try:
        transformed_clause = transform_sentence(clause, model)
        return eval(transformed_clause)
    except Exception as e:
        print(f"Error evaluating clause: {transformed_clause} with model {model}")
        raise e

# Function to evaluate the query under a given model
def evaluate_query(query, model):
    return evaluate_clause(query, model)

# Truth Table (TT) method implementation
def truth_table_method(kb, query):
    symbols = extract_symbols(kb, query)
    models = generate_models(symbols)
    
    valid_models = []
    for model in models:
        if evaluate_kb(kb, model):
            valid_models.append(model)
            print(f"Model: {model} satisfies KB")
    
    query_transformed = transform_sentence(query, {sym: sym for sym in symbols})
    
    query_true = all(evaluate_clause(query_transformed, model) for model in valid_models) if valid_models else False
    
    for model in valid_models:
        query_result = evaluate_clause(query_transformed, model)
        print(f"Model: {model}, Query {query} is {query_result}")
    
    return query_true, len(valid_models)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    method = sys.argv[2]
    kb, query = parse_file(filename)
    
    print("Knowledge Base:", kb)
    print("Query:", query)
    
    if method == "TT":
        result, details = truth_table_method(kb, query)
        
        print("Result:", result)
        print("Details:", details)
        
        if result:
            print(f"YES: {details}")
        else:
            print("NO")
    else:
        print("Invalid method")
        sys.exit(1)
