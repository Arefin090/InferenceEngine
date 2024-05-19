import sys
from engine import parse_file, truth_table_method
from kbclass import PropDefiniteKB
from backward_chaining import backward_chain
from forward_chaining import forward_chain

# Main function to handle command-line arguments and execute the appropriate method
def main():
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <filename> <method>")
        sys.exit(1)
    
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
    elif method == "FC":
        kb.forward_chain(query) # Do forward chaining to infer facts
        print(f"YES: {', '.join(kb.derived_order)}" if query in kb.inferred else "NO")
    elif method == "BC":
        if kb.ask(query):
            print(f"YES: {', '.join(kb.derived_order)}")
        else:
            print("NO")
    else:
        print(f"Unsupported Method: {method}") # Validation

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: Python <script.py> <filename> <method>") # validation
    else:
        filename = sys.argv[1]
        method = sys.argv[1]
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename) # absolute file pathing
        main(file_path, method)

