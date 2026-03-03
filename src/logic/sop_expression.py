from dataclasses import dataclass
from enum import Enum, auto

class LiteralState(Enum):
    ABSENT = auto()   # Variable is not in the product (Don't care)
    POSITIVE = auto() # Variable (e.g., Q0)
    NEGATED = auto()  # Variable bar (e.g., !Q0)

class SOPOutputType(Enum):
    NEXT_STATE_VARIABLE = auto()
    EXTERNAL_OUTPUT = auto()

class SOPOutput:
    def __init__(self, output_type: SOPOutputType, index: int):
        self.output_type = output_type
        self.index = index

    def __repr__(self):
        if self.output_type == SOPOutputType.NEXT_STATE_VARIABLE:
            return f"\nQ{self.index}(t+1)"
        elif self.output_type == SOPOutputType.EXTERNAL_OUTPUT:
            return f"\nO{self.index}"

class ProductTerm:
    """Represents a single AND gate (e.g., I0 & !Q1 & Q2)"""
    def __init__(self, inputs: list[LiteralState], states: list[LiteralState]):
        self.inputs = inputs  # Matches the length of num_inputs
        self.states = states  # Matches the length of num_state_vars

    def _format_term(self, lits, prefix):
        parts = []
        for i, state in enumerate(lits):
            if state == LiteralState.POSITIVE:
                parts.append(f"{prefix}{i}")
            elif state == LiteralState.NEGATED:
                parts.append(f"!{prefix}{i}")
        return parts

    def __repr__(self):
        # Format states (Q) then inputs (I) as requested
        state_parts = self._format_term(self.states, "Q")
        input_parts = self._format_term(self.inputs, "I")
        
        combined = state_parts + input_parts
        return "*".join(combined) if combined else "1"

class SOPExpression:
    """Represents an OR of multiple ProductTerms"""
    def __init__(self):
        self.terms: list[ProductTerm] = []

    def add_term(self, term: ProductTerm):
        self.terms.append(term)

    def __repr__(self):
        if not self.terms:
            return "0 (Always False)"
        # Joins terms with a + to represent the OR plane
        return " + ".join(repr(t) for t in self.terms)
