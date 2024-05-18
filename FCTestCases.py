import unittest
import string

from ForwardChainingActual import PropDefiniteKB 

class TestForwardChaining(unittest.TestCase): # Defining test class for Forward Chaining
    def setUp(self):
        self.kb = PropDefiniteKB() # Initialize the knowledge base instance
        self.kb.set_method('FC')  # Sets the method to forward chaining

    def test_basic_chain(self): # Basic linear chain of implications 
        rules = [
            "A => B",
            "B => C",
            "C => D"
        ]
        self.kb.tell("A") # Sets the initial fact
        for rule in rules:
            self.kb.tell(rule) # Add implication rules to the KB
        self.kb.forward_chain()  # Apply forward chaining to derive conclusions 
        self.assertTrue(self.kb.ask("D")) # Verify that 'D' was correctly derived.
    
    def test_complex_dependencies(self):   # Complex dependencies with conjunctions
        rules = [
            "A & B => C",
            "C & D => E"
        ]
        facts = ["A", "B", "D"]
        for fact in facts:
            self.kb.tell(fact) # Add initial facts to the KB
        for rule in rules:
            self.kb.tell(rule) # Add complex rules to the KB
        self.kb.forward_chain()  # Start Forward Chaining
        self.assertTrue(self.kb.ask("E")) # Verify that E is derived from the rules and facts

    def test_circular_dependencies(self): # Test case for circular dependency handling
        rules = [ # Rule set that creates a loop
            "A => B",
            "B => A"
        ]
        for rule in rules:
            self.kb.tell(rule) # Add initial fact, starting the loop
        self.kb.tell("A")
        self.kb.forward_chain() # Start Forward Chaining
        self.assertTrue(self.kb.ask("B")) # Check if B can still be derived despite the loop

    def test_negations_and_false_paths(self): # Test case for ensuring rules that shouldn't be triggered are not being triggered
        # rules that should not be triggered here;
        rules = [
        "A => B",
        "B & C => D"
        ]
        self.kb.tell("A") # Add fact A
        for rule in rules:
            self.kb.tell(rule) # Add rules where D should not be derived because C is missing
        self.kb.forward_chain() # Forward chaining
        self.assertFalse(self.kb.ask("D")) # Ensure D is not derived since C is not present

    def test_empty_and_minimal_input(self):  # Test case for an empty knowledge base
        self.assertFalse(self.kb.ask("A")) # Check if asking for A in an empty KB returns false

    def test_large_knowledge_base(self):   # Test case for large knowledge base with many rules
        # the said large set of rules and facts
        previous_fact = None
        for letter in string.ascii_uppercase:  # Creates a chain from A to Z
            fact = f"{letter}"
            if previous_fact:
                rule = f"{previous_fact} => {fact}"
                self.kb.tell(rule) # Tell the rule to the KB
            previous_fact = fact
        self.kb.tell("A")  # Start the chain by telling A
        self.kb.forward_chain()
        self.assertTrue(self.kb.ask("Z")) # Ensure Z can be derived at the end of the chain

class TestBackwardChaining(unittest.TestCase): # Define test class for backward chaining
    def setUp(self):
        self.kb = PropDefiniteKB() # Initialize the knowledge base instance
        self.kb.set_method('BC') # Set the method to backward chaining

    def test_basic_derivation(self): # Test basic derivation
        self.kb.tell("a => b")
        self.kb.inferred.add("a")  # Add a to inferred facts
        self.assertTrue(self.kb.ask("b")) # Verify that b can be derived from a
 
    def test_chaining_multiple_rules(self):    # Test chaining multiple rules
        rules = ["a => b", "b => c", "c => d"]
        for rule in rules:
            self.kb.tell(rule)
        self.kb.inferred.add("a") # Start from a
        self.assertTrue(self.kb.ask("d")) # Verify that d can be derived from a through multiple rules

    def test_complex_dependencies(self):   # Test handling of complex dependencies 
        self.kb.tell("a & b => x")
        self.kb.tell("x & c => y")
        for fact in ["a", "b", "c"]:
            self.kb.inferred.add(fact) # Add facts to derive y
        self.assertTrue(self.kb.ask("y"))   # Verify derivation to y


    def test_unmet_premise(self):  # Test where not all premises are met 
        self.kb.tell("a & b => x")
        self.kb.inferred.add("a") # Only 'a' is present, 'b' is missing
        self.assertFalse(self.kb.ask("x"))  # Verify 'x' cannot be derived

    def test_cyclic_dependencies(self):  # Test handling cyclic dependencies
        self.kb.tell("a => b")
        self.kb.tell("b => a")
        self.kb.inferred.add("a") # Starting from a
        self.assertTrue(self.kb.ask("b")) # Verify that b can still be derived

    def test_negative_case(self):     # Test negative case where the query cannot be derived
        self.kb.tell("a => b")
        self.assertFalse(self.kb.ask("c"))  # Ensure c cannot be derived since it's unrelated to any rule
        
if __name__ == '__main__':
    unittest.main()
