import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine import extract_propositions, check_entailment
from src.parser import parse_input


def main(file_path, method):
    # Parse the input file to get the knowledge base and the query
    kb, query = parse_input(file_path)
    propositions = extract_propositions(kb)

    if method == 'TT':
        is_entailed, model_count = check_entailment(kb, query, propositions)
        if is_entailed:
            print(f"YES: {model_count}")
        else:
            print("NO")

# Note: Additional cases for FC and BC will be added later

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <filename> <method>")
    else:
        file_path = sys.argv[1]
        method = sys.argv[2]
        main(file_path, method)
