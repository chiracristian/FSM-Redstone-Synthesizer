from pyeda.inter import *
from pyeda.boolalg.expr import ExprComplement, Or, And
from transition_table import TransitionTable

from sop_expression import SOPExpression, ProductTerm, LiteralState

def synthesize_logic(table: TransitionTable) -> dict[str, SOPExpression]:
    """
    Returns a dictionary mapping 'QN_next' and 'OUT_N' to minimized SOPExpressions.
    """
    # 1. Define PyEDA variables
    inputs = [exprvar(f'i{i}') for i in range(table.num_inputs)]
    states = [exprvar(f's{i}') for i in range(table.num_state_vars)]
    
    # 2. Build the truth table mapping
    # We need to solve for each Next State bit and each Output bit separately
    num_targets = table.num_state_vars + table.num_outputs
    expressions = {}

    for bit_index in range(num_targets):
        # Determine if we are targeting a Next State bit or an Output bit
        is_state = bit_index < table.num_state_vars
        label = f"q{bit_index}_next" if is_state else f"out{bit_index - table.num_state_vars}"
        
        # Build the ON-set for Espresso
        on_set = []
        for row in table.rows:
            target_bits = row["state_next"] if is_state else row["output"]
            if target_bits[bit_index if is_state else (bit_index - table.num_state_vars)] == 1:
                # Combine input and state_t bits to form the minterm
                combined_bits = row["input"] + row["state_t"]
                on_set.append("".join(map(str, combined_bits)))
        
        # 3. Minimize using Espresso
        # truthtable takes variables and the ON-set strings
        tt = truthtable(inputs + states, on_set)
        minimized_expr, = espresso_exprs(tt.to_expr())
        
        # 4. Convert PyEDA Expression back to SOPExpression class
        expressions[label] = _convert_to_sop(minimized_expr, table.num_inputs, table.num_state_vars)

    return expressions

def _convert_to_sop(pyeda_expr, n_in: int, n_st: int) -> SOPExpression:
    sop = SOPExpression()
    
    # PyEDA returns Or(And(...), And(...))
    # If there's only one term, it might just be an And or a Literal
    terms = pyeda_expr.xs if isinstance(pyeda_expr, Or) else [pyeda_expr]
    
    for term in terms:
        in_lits = [LiteralState.ABSENT] * n_in
        st_lits = [LiteralState.ABSENT] * n_st
        
        # Extract literals from the And term
        literals = term.xs if isinstance(term, And) else [term]
        for lit in literals:
            name = lit.name if not hasattr(lit, 'node') else lit.node.name
            # Check if it's negated
            is_neg = isinstance(lit, ExprComplement)
            
            idx = int(name[1:])
            state = LiteralState.NEGATED if is_neg else LiteralState.POSITIVE
            
            if name.startswith('i'):
                in_lits[idx] = state
            else:
                st_lits[idx] = state
                
        sop.add_term(ProductTerm(in_lits, st_lits))
    return sop
