class NFAState:
    def __init__(self):
        self.transitions = {}  # Dictionary to hold transitions (e.g., {'a': state1, 'b': state2})
        self.epsilon_transitions = []  # Epsilon transitions (ε)

class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

def regex_to_nfa(regex):
    """Convert a regular expression to NFA using Thompson's construction."""
    
    def create_basic_nfa(symbol):
        """Create an NFA for a single symbol."""
        start_state = NFAState()
        accept_state = NFAState()
        start_state.transitions[symbol] = accept_state
        return NFA(start_state, accept_state)

    def concatenate_nfa(nfa1, nfa2):
        """Concatenate two NFAs."""
        nfa1.accept_state.epsilon_transitions.append(nfa2.start_state)
        return NFA(nfa1.start_state, nfa2.accept_state)

    def union_nfa(nfa1, nfa2):
        """Create a union (OR) of two NFAs."""
        start_state = NFAState()
        accept_state = NFAState()
        start_state.epsilon_transitions.append(nfa1.start_state)
        start_state.epsilon_transitions.append(nfa2.start_state)
        nfa1.accept_state.epsilon_transitions.append(accept_state)
        nfa2.accept_state.epsilon_transitions.append(accept_state)
        return NFA(start_state, accept_state)

    def kleene_star_nfa(nfa):
        """Apply Kleene star (*) to an NFA."""
        start_state = NFAState()
        accept_state = NFAState()
        start_state.epsilon_transitions.append(nfa.start_state)
        start_state.epsilon_transitions.append(accept_state)
        nfa.accept_state.epsilon_transitions.append(nfa.start_state)
        nfa.accept_state.epsilon_transitions.append(accept_state)
        return NFA(start_state, accept_state)

    stack = []  # Stack to hold intermediate NFAs

    # Iterate over each character in the regular expression
    for char in regex:
        if char.isalnum():  # Handle basic symbols (letters, digits)
            stack.append(create_basic_nfa(char))
        elif char == '.':  # Concatenation operator (for example "ab" => NFA for "a" followed by NFA for "b")
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concatenate_nfa(nfa1, nfa2))
        elif char == '|':  # Union operator (for example "a|b")
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union_nfa(nfa1, nfa2))
        elif char == '*':  # Kleene star operator (for example "a*")
            nfa = stack.pop()
            stack.append(kleene_star_nfa(nfa))
    
    # The final NFA should be the only one remaining on the stack
    return stack.pop()

def display_nfa(nfa, visited=None):
    """Display the NFA transitions and epsilon transitions."""
    if visited is None:
        visited = set()

    def print_state(state, visited):
        if state in visited:
            return
        visited.add(state)

        for symbol, next_state in state.transitions.items():
            print(f"State {id(state)} -- {symbol} --> State {id(next_state)}")
            print_state(next_state, visited)

        for next_state in state.epsilon_transitions:
            print(f"State {id(state)} -- ε --> State {id(next_state)}")
            print_state(next_state, visited)

    print(f"Start state: {id(nfa.start_state)}")
    print(f"Accept state: {id(nfa.accept_state)}")
    print_state(nfa.start_state, visited)

# Example usage:
regex = "ab|c*"  # Sample regular expression (can be modified)
nfa = regex_to_nfa(regex)
display_nfa(nfa)
