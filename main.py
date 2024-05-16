import sys
from engine import parse_file, truth_table_method

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

if __name__ == "__main__":
    main()
