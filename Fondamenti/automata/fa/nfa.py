#!/usr/bin/env python3
"""Classes and methods for working with nondeterministic finite automata."""

import copy
import queue
import random

import automata.base.automaton_exceptions as ae
import automata.fa.fa_exceptions as fae
import automata.fa.fa as fa
import automata.fa.dfa as dfa
import automata.fa.nfa_configuration as nfac
import automata.fa.dfa_in_nfa_configuration as dnfac


class NFA(fa.FA):
    """
    A nondeterministic finite automaton (possibly with epsilon transitions).

    Created by:
        NFA(): definition provided as call parameters
        NFA.load(file): definition provided in yaml file
        NFA.from_dfa(nda): derived from given DFA
        NFA.from_epsilon_nfa(nfa): derived from given NFA by eliminating
        epsilon-transitions
        *NFA.from_rg(rg): derived from given regular grammar
        *NFA.from_regex(regex): derived from given regular expression
        *NFA.union(nfa1, nfa2): union of languages
        *NFA.intersection(nfa1, nfa2): intersection of languages
        *NFA.concat(nfa1, nfa2): concatenation of languages
        *NFA.compl(nfa): complement of language
        *NFA.kleene(nfa): Kleene closure of language

    A NFA is coded as follows:
        - states are defined as strings
        - the set of states is a Python set of strings
        - initial state is a string
        - final states is a Python set of strings
        - input symbols are strings
        - transition function is a Python dictionary where
            - keys are strings
            - values are Python dicts where
                - keys are input symbols or the empty string ''
                - values are Python sets of strings
                delta(q1,a)={q2, q3} is coded as delta['q1']['a']={'q2','q3'}
                delta(q1,a)={} is coded as delta['q1']['a']=set()
                delta(q1,epsilon)={q2, q3} is coded as delta['q1']['']={'q2','q3'}

    """

# -----------------------------------------------------------------------------
# Instantiation

    def __init__(self, *, states, input_symbols, delta,
                 initial_state, final_states):
        """Initialize a complete NFA."""
        super().__init__(states, input_symbols, initial_state, final_states)
        self.delta = NFA._transitions_from_delta(delta)
        self.validate()

    @classmethod
    def from_dfa(cls, dfa):
        """Initialize this NFA as one equivalent to the given DFA."""
        return dfa.nfa

    @classmethod
    def from_epsilon_nfa(cls, nfa):
        """
        Initialize from epsilon-NFA.

        Initialize this NFA as one equivalent to the given epsilon-NFA,
        deleting all epsilon transitions.
        """
        return nfa.nfa_no_null

    @classmethod
    def from_regex(cls, re):
        """Initialize this NFA as one equivalent to the given regular expression."""
        return re.nfa

    @classmethod
    def union(cls, nfa1, nfa2):
        """
        Initialize this NFA as one accepting the language union of those accepted
        by the given nfa's.
        """
        return nfa1.unite(nfa2)

    @classmethod
    def intersection(cls, nfa1, nfa2):
        """
        Initialize this NFA as one accepting the language intersection of those accepted
        by the given nfa's.
        """
        return nfa1.intersect(nfa2)

    @classmethod
    def concat(cls, nfa1, nfa2):
        """
        Initialize this NFA as one accepting the language concatenation of those accepted
        by the given nfa's.
        """
        return nfa1.concatenate(nfa2)

    @classmethod
    def compl(cls, nfa):
        """
        Initialize this NFA as one accepting the complement language of the one accepted
        by the given nfa.
        """
        return nfa.complement

    @classmethod
    def kleene(cls, nfa):
        """
        Initialize this NFA as one accepting the kleene-closure of the language accepted
        by the given nfa.
        """
        return nfa.kleene_closure

    @staticmethod
    def _transitions_from_delta(delta):
        """Derive internal representation of transition function."""
        transitions = copy.deepcopy(delta)
        for state, state_transitions in delta.items():
            for input_symbol, is_transitions in state_transitions.items():
                transitions[state][input_symbol] = set()
                for is_transition in is_transitions:
                    transitions[state][input_symbol].add(fa.FATransition(is_transition))
        return transitions

    @property
    def _all_input_symbols(self):
        """Return the set of input symbols plus the epsilon char ''."""
        return self.input_symbols.union({''})

# -----------------------------------------------------------------------------
# Derivation

    @property
    def dfa(self):
        """Return a DFA equivalent to this NFA."""
        # TO DO
        dfa = None
        return dfa

    @property
    def nfa_no_null(self):
        """Return NFA equivalent to this one, with no null transition."""
        # TO DO
        new_nfa = None
        return new_nfa

    def unite(self, nfa):
        """
        Return a NFA accepting the language union of those accepted
        by this nfa and the one given as parameter.
        """
        # To DO
        nfa1 = None
        return nfa1

    def intersect(self, nfa):
        """
        Return a NFA accepting the language intersection of those accepted
        by this nfa and the one given as parameter.
        """
        # To DO
        nfa1 = None
        return nfa1

    def concatenate(self, nfa):
        """
        Return a NFA accepting the language concatenation of those accepted
        by this nfa and the one given as parameter.
        """
        # TO DO
        nfa1 = None
        return nfa1

    @property
    def complement(self):
        """
        Return a NFA accepting the complement language of the one accepted
        by this nfa.
        """
        # TO DO
        nfa = None
        return nfa

    @property
    def kleene_closure(self):
        """
        Return a NFA accepting the Kleene-closure of the language accepted
        by this nfa.
        """
        # TO DO
        nfa = None
        return nfa

# -----------------------------------------------------------------------------
# Predicates

    @property
    def infinite(self):
        """Return True iff the language accepted by this NFA is infinite."""
        # TO DO
        is_infinite = True
        return is_infinite

    @property
    def empty(self):
        """Return True iff the language accepted by this NFA is empty."""
        return self.dfa.empty

# -----------------------------------------------------------------------------
# Validation

    def _validate_transition_is(self, start_state, input_symbol):
        """
        Check that the input symbol of a transition is valid.

        Verifies that the input symbol of the transition either belongs to the
        input alphabet or is empty (in the case of epsilon transition).
        """
        if input_symbol not in self._all_input_symbols:
            raise fae.InvalidFATransitionError(
                'transition ({},{}) has invalid transition symbol'
                .format(start_state, input_symbol))

    def _validate_transitions_from_state_and_is(self, start_state,
                                                input_symbol,
                                                input_symbol_transitions):
        """
        Check that the transition from a state and symbol is valid.

        Verifies that all resulting states belong to the set of states.
        """
        for transition in input_symbol_transitions:
            new_state = transition.state
            if new_state not in self.states and new_state is not None:
                raise fae.InvalidFATransitionError(
                    'transition ({},{}) has invalid final state {}'
                    .format(start_state, input_symbol, new_state))

# -----------------------------------------------------------------------------
# Completion

    def _complete_transition_missing_symbols(self, state_transitions):
        """Complete transitions from a same state with all symbols."""
        for input_symbol in self.input_symbols:
            if input_symbol not in state_transitions:
                state_transitions[input_symbol] = set()

# -----------------------------------------------------------------------------
# Transformation





# -----------------------------------------------------------------------------
# Computation

    def _initial_configuration(self, list_of_tokens):
        """Define the initial configuration of the nfa for the given string."""
        initial_config = nfac.NFAConfiguration.initial_configuration(
                        list_of_tokens=list_of_tokens,
                        automaton=self)
        return self._epsilon_closure(initial_config)

    def _next_configuration(self, current_config):
        """Define the next configuration of the nfa."""
        new_states = set()
        for state in current_config.states_iterator:
            transitions = self._transition(state, current_config.next_token)
            if transitions is not None:
                new_states = new_states.union(
                    {transition.state for transition in transitions})
        if not new_states:
            raise fae.UndefinedNFATransitionException(
                    'no transition defined from ({},{})'.format(
                        current_config.next_token,
                        current_config.states))
        next_config = current_config.next_configuration(new_states)
        return self._epsilon_closure(next_config)

    def _epsilon_closure(self, config):
        """
        Return the epsilon closure for the given configuration.

        The epsilon closure of a configuration c is the set containing c,
        along with every configuration that can be reached from c by following
        only epsilon transitions.
        """
        new_states = set()
        n_states = config.number_of_configurations
        for state in config.states_iterator:
            new_states.add(state)
            try:
                transitions = self.delta[state]['']
            except KeyError:
                transitions = set()
        for transition in transitions:
            new_states.add(transition.state)
        config = config.next_epsilon_configuration(new_states)
        if n_states == len(new_states):
            return config
        else:
            return self._epsilon_closure(config)

# -----------------------------------------------------------------------------
# Deterministic paths

    def _deterministic_transition(self, state, input_symbol):
        """
        Follow the transition for the given input symbol on the given state.

        Raise an error if either the state, or the symbol, or the transition
        do not exist.
        """
        if state not in self.states:
            raise ae.InvalidInputError(
                '{} is not a valid state'.format(state))
        if input_symbol not in self.input_symbols and len(input_symbol) > 0:
            raise ae.InvalidInputError(
                '{} is not a valid input symbol'.format(input_symbol))
        try:
            res = self.delta[state][input_symbol]
        except KeyError:
            res = None
        return res

    def _initial_deterministic_configuration(self, list_of_tokens):
        """
        Define the initial configuration of the nfa for the given string.

        The configuration is considered a deterministic one.
        """
        initial_config = dnfac.DFAConfiguration_in_NFA.initial_configuration(
                        list_of_tokens=list_of_tokens,
                        automaton=self)
        return initial_config

    def _next_random_deterministic_configuration(self, current_config):
        """Define the next configuration in a deterministic path of the nfa."""
        new_states = set()
        epsilon_transition_exists = True
        epsilon_transition_applied = True
        next_token = ''
        transitions = self._deterministic_transition(
                current_config.state,
                next_token)
        if transitions is None:
            epsilon_transition_exists = False
        if not epsilon_transition_exists or random.choice([0, 1]) == 0:
            epsilon_transition_applied = False
            next_token = current_config.next_token
            transitions = self._deterministic_transition(
                    current_config.state,
                    next_token)
            if transitions is not None:
                for transition in transitions:
                    new_states.add(transition.state)
        if len(new_states) == 0:
            raise fae.UndefinedNFATransitionException(
                'no transition defined from ({},{})'.format(
                    next_token,
                    current_config.state))
        next_state = random.choice(list(new_states))
        if epsilon_transition_applied:
            next_config = current_config.next_epsilon_configuration(next_state)
        else:
            next_config = current_config.next_configuration(next_state)
        return next_config

# -----------------------------------------------------------------------------
# Other

    def save(self, file):
        """Save a copy of the definition of this DFA in a json file."""
        d = vars(self).copy()
        with open(file+'.json', "w") as f:
            json.dump(d, f)

    def __str__(self):
        """Return a string representation of the object."""
        s = 'symbols: {}\n'.format(','.join(sorted(self.input_symbols)))
        s += 'states: {}\n'.format(','.join(sorted(self.states)))
        s += 'start state: {}\n'.format(self.initial_state)
        s += 'final states: {}\n'.format(','.join(sorted(self.final_states)))
        s += 'transitions\n'
        for start_state, state_transitions in sorted(self.delta.items()):
            for input_symbol, transitions in sorted(state_transitions.items()):
                if transitions:
                    st = '{'
                    for transition in transitions:
                        st += '{}, '.format(transition)
                    st = st[:-2]
                else:
                    st = '{'
                st += '}'
                s += '\t ({},{}) -> {}\n'.format(start_state, input_symbol, st)
        return s[:-1]
