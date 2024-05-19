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
            super().__init__()  # Call the initializer of the base class
            self.inferred = set()  # Initialize the inferred facts set as an instance variable
            self.method = None  # Specifies the chaining method
            self.derived_order = []  # List the order of the derivations
            self.initial_facts = set() # Set to track initial facts

        def set_method(self, method):
            if method in ["BC", "FC"]:
                self.method = method
            else:
                raise ValueError("Unsupported Method specified")

        def ask(self, query):
            if self.method == "BC":
                return self.backward_chain(query)
            elif self.method == "FC":
                return query in self.inferred  # Check the already inferred facts
            else:
                raise ValueError("Unsupported method specified")

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
            
