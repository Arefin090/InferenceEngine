import sys
import os
from engine import parse_file, truth_table_method
from forward_chaining import forward_chain
from backward_chaining import backward_chain
from kbclass import PropDefiniteKB 


# Main function to handle command-line arguments and execute the appropriate method
def main():
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <filename> <method>")
        sys.exit(1)
    
    filename = sys.argv[1]
    method = sys.argv[2]
    print(f"Reading file: {filename}")
    try:
        kb_sentences, query = parse_file(filename)
    except Exception as e:
        print(f"Error opening or reading the file: {e}")
        sys.exit(1)

    print("Knowledge Base:", kb_sentences)
    print("Query:", query)
    
    if method == "TT":
        result, details = truth_table_method(kb_sentences, query)
        
        print("Result:", result)
        print("Details:", details)
        
        if result:
            print(f"YES: {details}")
        else:
            print("NO")
    else:
        kb = PropDefiniteKB()
        kb.set_method(method)
        for sentence in kb_sentences:
            kb.tell(sentence)
        print(f"Initial Facts after parsing: {kb.initial_facts}")
            
        if method == "FC":
            result = kb.forward_chain(query) # Do forward chaining to infer facts
            print(f"YES: {', '.join(kb.derived_order)}" if query in kb.inferred else "NO")
        elif method == "BC":
            if kb.ask(query):
                print(f"YES: {', '.join(kb.derived_order)}")
            else:
                print("NO")
        else:
            print(f"Unsupported Method: {method}") # Validation

if __name__ == "__main__":
    main()


