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