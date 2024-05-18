import sys
import os
from collections import defaultdict

def parse_kb_file(file_path):  # Parses the knowledge base file
    kb = PropDefiniteKB()  # Creates instance of PropDefiniteKB
    query = None  # Initializes Query with None to store any queries found in the file
    try:
        with open(file_path, 'r') as file:  # Opens the file in read mode
            mode = None  # Initializes mode to None which will be used to determine the current section of the file tell or ask
            for line in file:  # Iterates through each line in the file
                line = line.strip()  # Strips the whitespace from the start and end of the line
                if 'TELL' in line:
                    mode = 'tell'  # Set mode to tell when the line contains tell
                    continue  # Skips to the next iteration
                elif 'ASK' in line:
                    mode = 'ask'  # Sets mode to ask when the line contains ask
                    continue  # Skips the line with ASK

                if mode == 'tell' and line:
                    instructions = line.split(';')  # Splits the line into separate instructions at each semicolon
                    for instruction in instructions:
                        if instruction.strip():  # Ensure instruction is not empty
                            kb.tell(instruction.strip())  # Add the instruction to the KB
                elif mode == 'ask' and line:  # Store the line as a query if in ask mode and the line is not empty
                    query = line.strip()  # Directly store the query line
    except IOError:
        print(f"Error opening or reading the file: {file_path}")  # Error message
    return kb, query

class KB:  # Base Class for KB
    def __init__(self):
        self.clauses = []  # Initializes empty list to store kb clauses

    def tell(self, sentence):
        # Adds a sentence to the KB
        raise NotImplementedError("This method should be overridden by subclasses")

    def ask(self, query):
        # Asks the KB if a query can be derived
        raise NotImplementedError("This method should be overridden by subclasses")

    def retract(self, sentence):
        # Removes a sentence from KB
        raise NotImplementedError("This method should be overridden by subclasses")


class PropDefiniteKB(KB):  # Subclass of KB which will handle propositional definite kb
    def __init__(self):
        super().__init__()  # Calls the initializer of the base class
        self.inferred = set()  # Initializes the inferred facts set as an instance variable
        self.method = None  # Specifies the chaining method
        self.derived_order = []  # List the order of the derivations
        self.initial_facts = set() # Set to track initial facts

    def set_method(self, method):
        if method in ["BC", "FC"]:
            self.method = method
        else:
            raise ValueError("Unsupported Method specified") # Validation

    def ask(self, query):
        if self.method == "BC":
            return self.backward_chain(query)
        elif self.method == "FC":
            return query in self.inferred  # Check the already inferred facts
        else:
            raise ValueError("Unsupported method specified") # Validation

    def tell(self, sentence):  # Parses and stores rules and facts from the sentence
        if '=>' in sentence:
            premise, conclusion = sentence.split('=>')  # Splits sentence into premise and conclusion at =>
            premises = set(prem.strip() for prem in premise.split('&'))  # Creates set of premises split at &
            self.clauses.append((premises, conclusion.strip()))  # Add rule to the kb
        else:
            fact = sentence.strip()
            self.inferred.add(fact)  # Directly adds facts to inferred
            self.initial_facts.add(fact) # Track initial facts given
            print(f"Fact added to inferred: {fact}")
            
    def forward_chain(self, query=None):  # Apply forward chaining to infer all possible facts
        added = True
        self.derived_order.extend(sorted(self.initial_facts)) # Checks that initial facts are added to the derived order list
        while added:
            added = False  # Reset flag to false
            to_infer = []  # Tracks the new inferred facts in this loop
            print(f"Current inferred facts: {self.inferred}")
            for premises, conclusion in self.clauses:
                if premises.issubset(self.inferred):  # Checks if all premises are already inferred
                    if conclusion not in self.inferred:  # Checks if conclusion is not already inferred
                        to_infer.append(conclusion)  # Tracks the order of each derivation
                        added = True  # Sets the flag to True to show new fact was inferred
                        print(f"Derived new fact: {conclusion}")  # Debug Statements here;
                    else:
                        print(f"Already Derived: {conclusion}")  # Debug Output
                else:
                    print(f"Failed to derive new fact from premises: {premises} for conclusion: {conclusion}")
            for fact in to_infer:  # Adds all new facts to inferred and derived order
                self.inferred.add(fact) 
                if fact not in self.derived_order:
                    self.derived_order.append(fact)
            to_infer.clear() # Clear the list
        if query and query in self.derived_order:
            self.derived_order.remove(query)
            self.derived_order.append(query)

    def backward_chain(self, query):
        print(f"Attempting to derive: {query}")
        if query in self.inferred:  # Check if the query is already a known fact
            print(f"{query} is already inferred")
            if query not in self.derived_order:
                self.derived_order.append(query)
            return True

        for premises, conclusion in self.clauses:  # Checks if there are any rules that can conclude query
            if conclusion == query:
                print(f"Found rule: {premises} => {conclusion}")
                if all(self.backward_chain(prem) for prem in premises):  # Checks if all premises can be derived
                    self.inferred.add(query)
                    print(f"Derived {query} from {premises}")
                    for prem in premises:
                        if prem not in self.initial_facts and prem not in self.derived_order:
                            self.derived_order.append(prem)
                    if query not in self.derived_order:
                        self.derived_order.append(query) # Adds the query to the order list
                    return True
                else:
                    print(f"Failed to derive all premises for {query}")
        print(f"Failed to derive {query}")
        return False

    def retract(self, sentence):
        self.clauses = [clause for clause in self.clauses if clause[1] != sentence]  # Removes a sentence's clause from the KB
        self.inferred.discard(sentence)  # remove from inferred if it was directly inferred
        if sentence in self.derived_order:
            self.derived_order.remove(sentence)



def main(file_path, method):
    kb, query = parse_kb_file(file_path)  # Parsing here
    print("Initial Facts after parsing:", kb.inferred)  # This should include 'p2'.
    kb.set_method(method)  # Set the chaining method

    if method == "FC":
        kb.forward_chain(query)  # Do forward chaining to infer facts
        print(f"YES: {', '.join(kb.derived_order)}" if query in kb.inferred else "NO")
    elif method == "BC":
        if kb.ask(query):
            print(f"YES: {', '.join(kb.derived_order)}")
        else:
            print("NO")
    else:
        print(f"Unsupported Method: {method}")  # Print an error message if the method is not supported

if __name__ == "__main__":  # Script starts
    if len(sys.argv) != 3:
        print("Usage: Python <script.py> <filename> <method>")  # Prints out a validation statement
    else:
        filename = sys.argv[1]
        method = sys.argv[2]
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)  # makes the file path
        main(file_path, method)  # Calls the main func
