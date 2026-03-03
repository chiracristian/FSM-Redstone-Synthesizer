from pyeda.inter import *
from pyeda.boolalg.expr import Complement, Or, And
from pyeda.inter import *
from pyeda.boolalg.expr import OrOp, AndOp

from logic.transition_table import TransitionTable
from logic.sop_expression import *

def synthesize_logic(table: TransitionTable) -> dict[SOPOutput, SOPExpression]:
    """
    Returns a dictionary mapping SOPOutput objects to minimized SOPExpressions.
    """
    inputs = [exprvar(f'i{i}') for i in range(table.num_inputs)]
    states = [exprvar(f's{i}') for i in range(table.num_state_vars)]
    
    num_targets = table.num_state_vars + table.num_outputs
    expressions = {}

    for bit_index in range(num_targets):
        # 1. Create the structured key
        if bit_index < table.num_state_vars:
            output_key = SOPOutput(SOPOutputType.NEXT_STATE_VARIABLE, bit_index)
            target_bit_idx = bit_index
        else:
            idx = bit_index - table.num_state_vars
            output_key = SOPOutput(SOPOutputType.EXTERNAL_OUTPUT, idx)
            target_bit_idx = idx
        
        # 2. Build ON-set as before
        on_set_exprs = []
        for row in table.rows:
            target_bits = row["state_next"] if bit_index < table.num_state_vars else row["output"]
            if target_bits[target_bit_idx] == 1:
                combined_bits = row["input"] + row["state_t"]
                minterm_lits = []
                for i, bit in enumerate(combined_bits):
                    var = (inputs + states)[i]
                    minterm_lits.append(var if bit == 1 else ~var)
                on_set_exprs.append(And(*minterm_lits))
        
        # 3. Minimize
        if not on_set_exprs:
            minimized_expr = expr(0) 
        else:
            minimized_results = espresso_exprs(Or(*on_set_exprs))
            minimized_expr = minimized_results[0]
        
        # 4. Store using the SOPOutput object
        expressions[output_key] = _convert_to_sop(minimized_expr, table.num_inputs, table.num_state_vars)

    return expressions

def _convert_to_sop(pyeda_expr, n_in: int, n_st: int) -> SOPExpression:
    sop = SOPExpression()
    
    if pyeda_expr.is_zero():
        return sop # Returns an empty SOP (0 terms = false)
    if pyeda_expr.is_one():
        # A term with all ABSENT variables evaluates to True naturally in Redstone
        sop.add_term(ProductTerm([LiteralState.ABSENT] * n_in, [LiteralState.ABSENT] * n_st))
        return sop
    
    # We now correctly check against OrOp and AndOp classes
    terms = pyeda_expr.xs if isinstance(pyeda_expr, OrOp) else [pyeda_expr]
    
    for term in terms:
        in_lits = [LiteralState.ABSENT] * n_in
        st_lits = [LiteralState.ABSENT] * n_st
        
        # Extract literals from the AndOp term
        literals = term.xs if isinstance(term, AndOp) else [term]
        
        for lit in literals:
            # The ultimate safe extraction: cast to string
            # In PyEDA, variables look like 'i0' and complements look like '~i0'
            lit_str = str(lit)
            is_neg = lit_str.startswith('~')
            clean_name = lit_str.replace('~', '')
            
            idx = int(clean_name[1:])
            state = LiteralState.NEGATED if is_neg else LiteralState.POSITIVE
            
            if clean_name.startswith('i'):
                in_lits[idx] = state
            else:
                st_lits[idx] = state
                
        sop.add_term(ProductTerm(in_lits, st_lits))
    return sop