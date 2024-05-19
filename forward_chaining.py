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