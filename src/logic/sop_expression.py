from enum import Enum, auto

class LiteralState(Enum):
    ABSENT = auto()   # Variable is not in the product (Don't care)
    POSITIVE = auto() # Variable (e.g., Q0)
    NEGATED = auto()  # Variable bar (e.g., !Q0)

class ProductTerm:
    """Represents a single AND gate (e.g., I0 & !Q1 & Q2)"""
    def __init__(self, inputs: list[LiteralState], states: list[LiteralState]):
        self.inputs = inputs  # Matches the length of num_inputs
        self.states = states  # Matches the length of num_state_vars

    def __repr__(self):
        return f"Product(In:{self.inputs}, St:{self.states})"

class SOPExpression:
    """Represents an OR of multiple ProductTerms"""
    def __init__(self):
        self.terms: list[ProductTerm] = []

    def add_term(self, term: ProductTerm):
        self.terms.append(term)

    def __repr__(self):
        return f"SOP with {len(self.terms)} terms"
