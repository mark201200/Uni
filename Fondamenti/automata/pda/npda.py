#!/usr/bin/env python3
"""Classes and methods for working with nondeterministic pushdown automata."""

import copy
import random

import tools.tools as tools
import automata.base.automaton_exceptions as ae
import automata.pda.pda_exceptions as pae
import automata.pda.pda as pd

import automata.pda.npda_configuration as npc
import automata.pda.dpda_in_npda_configuration as dnpc


class NPDA(pd.PDA):
    """
    A nondeterministic pushdown automaton.

    Created by:
    NPDA(): definition provided as call parameters
    NPDA.load(file): definition provided in yaml file
    *NPDA.from_dpda(nda): derived from given DPDA
    *NPDA.from_cfg(cfg) derived from given context free grammar
    *NPDA.accept_final_state(npda): accepting by final state derived from given npda
    *NPDA.accept_empty_stack(npda): accepting by empty stack derived from given npda

    A NPDA is coded as follows:
        - states are defined as strings
        - the set of states is a Python set of strings
        - initial state is a string
        - final states is a Python set of strings
        - input symbols are strings
        - input alphabet is a Python set of strings
        - stack items are strings
        - the set of stack items is a Python set of strings
        - transition function is a Python dictionary where
            - keys are strings
            - values are Python dicts where
                - keys are input symbols or the empty string ''
                - values are Python dicts where
                    - keys are stack symbols
                    - values are possibly empty sets of pairs (tuples of two items),
                        each composed of a state and a possible empty Python tuple of
                        stack symbols: the internal representation of this pair is as an
                        instance of StateStackPair
                delta(q1,a,'X')={(q2,ZY), (q3,_), (q1, Y)} is coded as
                                 delta['q1']['a']={('q2', ('Z', 'Y')), ('q3', ()),
                                                   ('q1', ('Y',))}
        - acceptance_mode ('E' or 'F') specifies whether the NPDA accepts by empty stack
            or final state
    """

    def __init__(self, *, states, input_symbols, stack_symbols,
                 delta, initial_state,
                 initial_stack_symbol, final_states, acceptance_mode):
        """Initialize a complete NPDA."""
        super().__init__(states, input_symbols, stack_symbols, initial_state,
                         initial_stack_symbol, final_states, acceptance_mode)
        self.delta = NPDA.transitions_from_delta(delta)
        # 'E': empty stack, 'F': final state
        self.validate()

    @classmethod
    def from_dpda(cls, dpda):
        """Initialize this NPDA as one equivalent to the given DPDA."""
        return dpda.npda

    @classmethod
    def from_cfg(cls, cfg):
        """Initialize this NPDA as one equivalent to the given CFG."""
        return cfg.npda

    @classmethod
    def accept_final_state(cls, npda):
        """Initialize a NPDA equivalent to the given one, accepting by final state."""
        return npda.final_state

    @classmethod
    def accept_empty_stack(cls, npda):
        """Initialize a NPDA equivalent to the given one, accepting by empty stack."""
        return npda.empty_stack

    @staticmethod
    def transitions_from_delta(delta):
        """Derive internal representation of transition function."""
        transitions = copy.deepcopy(delta)
        for state, state_transitions in delta.items():
            for input_symbol, is_transitions in state_transitions.items():
                for stack_symbol, ss_transitions in is_transitions.items():
                    transitions[state][input_symbol][stack_symbol] = set()
                    for ss_transition in ss_transitions:
                        transitions[state][input_symbol][stack_symbol].add(
                                pd.PDATransition(ss_transition))
        return transitions

    def _validate_transition_is(self, start_state, input_symbol):
        """
        Raise an error if the input symbol of a transition is invalid.

        Checks that the input symbol of a transition either belongs to the
        input alphabet or is empty (in the case of epsilon transitions).
        """
        if input_symbol not in self.input_symbols and len(input_symbol) > 0:
            raise pae.InvalidPDATransitionError(
                    'state {} has invalid transition symbol {}'.format(
                        start_state, input_symbol))

    def _validate_transitions_from_state_and_is_and_ss(self,
                                                       start_state,
                                                       input_symbol,
                                                       stack_symbol,
                                                       stack_symbol_transitions
                                                       ):
        """Check that the transition is valid."""
        for transition in stack_symbol_transitions:
            new_state, to_push = transition.state, transition.stack_symbols
            if new_state is None:
                raise pae.InvalidPDATransitionError(
                    'next state for transition ({},{},{}) is missing'
                    .format(start_state, input_symbol, stack_symbol))
            if new_state not in self.states:
                raise pae.InvalidPDATransitionError(
                    'next state for transition ({},{},{}) is not valid'
                    .format(start_state, input_symbol, stack_symbol))
            if not set(to_push).issubset(self.stack_symbols):
                raise pae.InvalidPDATransitionError(
                    'stack symbol string for ({},{},{}) is not valid'
                    .format(start_state, input_symbol, stack_symbol))

# -----------------------------------------------------------------------------
# Completion

    def _complete_transition_missing_stack_symbols(self, input_transitions):
        """Complete transitions from a same state and symbol."""
        for stack_symbol in self.stack_symbols:
            if stack_symbol not in input_transitions:
                input_transitions[stack_symbol] = set()

    @property
    def final_state(self):
        """Return NPDA equivalent to this one, accepting by final state."""
        if self.acceptance_mode == 'F':
            return self
        else:
            npda = None
            # TO DO
            return npda

    @property
    def empty_stack(self):
        """Return NPDA equivalent to this one, accepting by empty_stack."""
        if self.acceptance_mode == 'E':
            return self
        else:
            npda = None
            # TO DO
            return npda

    @property
    def cfg(self):
        """Return CFG equivalent to this NPDA."""
        cfg = None
        # TO DO
        return cfg
# -----------------------------------------------------------------------------
# Computation

    def _initial_configuration(self, list_of_tokens):
        """
        Define initial configuration.

        Defines the initial configuration of the npda for the given
        input string
        """
        initial_config = npc.NPDAConfiguration.initial_configuration(
            list_of_tokens, self)
        return self._epsilon_closure(initial_config)

    def _next_configuration(self, current_config):
        """
        Compute next configuration.

        Defines the next configuration of the npda for the current
        configuration
        """
        new_pairs = set()
        for pair in current_config.pairs_iterator:
            if pair.has_empty_stack:
                break
            transitions = self._transition(
               pair.state,
               current_config.next_token,
               pair.top_of_stack)
            if transitions is None:
                transitions = set()
            for transition in transitions:
                new_pairs.add(pair.update(transition.state,
                                          transition.stack_symbols))
        if not new_pairs:
            raise pae.UndefinedNPDATransitionException(
                'no transition defined from ({},{})'.format(
                    current_config.next_token,
                    current_config.state_stack_pairs))
        next_config = current_config.next_configuration(new_pairs)
        return self._epsilon_closure(next_config)

    def _epsilon_closure(self, config):
        """
        Return the epsilon closure for the given configuration.

        The epsilon closure of a configuration c is the set containing c,
        along with every configuration that can be reached from c by following
        only epsilon transitions.
        """
        new_pairs = set()
        n_pairs = config.number_of_pairs
        for pair in config.pairs_iterator:
            new_pairs.add(pair)
            if pair.has_empty_stack:
                break
            try:
                transitions = self.delta[pair.state]['']['pair.top_of_stack']
            except KeyError:
                transitions = set()
            for transition in transitions:
                new_pairs.add(pair.update(transition.state,
                                          transition.stack_symbols))
        config = config.next_epsilon_configuration(new_pairs)
        if n_pairs == len(new_pairs):
            return config
        else:
            return self._epsilon_closure(config)

# -----------------------------------------------------------------------------
# Deterministic paths

    def _deterministic_transition(self, state, input_symbol, stack_symbol):
        """
        Follow transition.

        Follow the transition for the given input symbol and stack symbol on
        the given state.
        Raise an error if either the state, the symbol, the stack symbol or
        the transition do not exist.
        """
        if state not in self.states:
            raise ae.InvalidInputError(
                '{} is not a valid state'.format(state))
        if input_symbol not in self.input_symbols and len(input_symbol) > 0:
            raise ae.InvalidInputError(
                '{} is not a valid input symbol'.format(input_symbol))
        if stack_symbol not in self.stack_symbols:
            raise ae.InvalidInputError(
                '{} is not a valid stack symbol'.format(stack_symbol))
        try:
            res = self.delta[state][input_symbol][stack_symbol]
        except KeyError:
            res = None
        return res

    def _initial_deterministic_configuration(self, list_of_tokens):
        """
        Define the initial configuration of the nfa for the given string.

        The configuration is considered a deterministic one.
        """
        initial_config = dnpc.DPDAConfiguration_in_NPDA.initial_configuration(
                        list_of_tokens=list_of_tokens,
                        automaton=self)
        return initial_config

    def _next_random_deterministic_configuration(self, current_config):
        """Define next configuration in a deterministic path of the npda."""
        new_pairs = set()
        epsilon_transition_exists = True
        epsilon_transition_applied = True
        pair = current_config.state_stack_pair
        if pair.has_empty_stack:
            raise pae.UndefinedNPDATransitionException(
                'no transition defined due to empty stack')
        transitions = self._deterministic_transition(
                pair.state,
                '',
                pair.top_of_stack)
        if transitions is None:
            epsilon_transition_exists = False
        if not epsilon_transition_exists or random.choice([0, 1]) == 0:
            epsilon_transition_applied = False
            transitions = self._deterministic_transition(
                pair.state,
                current_config.next_token,
                pair.top_of_stack)
            if transitions is None:
                transitions = set()
        for transition in transitions:
            new_pairs.add(transition)
        if not new_pairs:
            raise pae.UndefinedNPDATransitionException(
                'no transition defined from ({},{},{})'.format(
                    pair.state,
                    current_config.next_token,
                    pair.top_of_stack
                    ))
        transition = random.choice(list(new_pairs))
        next_state, to_push = transition.state, transition.stack_symbols
        if epsilon_transition_applied:
            next_config = current_config.next_epsilon_configuration(next_state,
                                                                    to_push)
        else:
            next_config = current_config.next_configuration(next_state,
                                                            to_push)
        return next_config
# -----------------------------------------------------------------------------
# Other

    def save(self, file):
        """Save a copy of the definition of this NPDA in a json file."""
        d = vars(self).copy()
        with open(file+'.json', "w") as f:
            json.dump(d, f)

    def __str__(self):
        """Return a string representation of the object."""
        s = 'symbols: {}\n'.format(','.join(sorted(self.input_symbols)))
        s += 'states: {}\n'.format(','.join(sorted(self.states)))
        s += 'stack symbols: {}\n'.format(','.join(sorted(self.stack_symbols)))
        s += 'start state: {}\n'.format(self.initial_state)
        s += 'initial stack symbol: {}\n'.format(self.initial_stack_symbol)
        s += 'final states: {}\n'.format(','.join(sorted(self.final_states)))
        s += 'acceptance condition: {}\n'.format(self.acceptance_mode)
        s += 'transitions'
        for start_state, state_transitions in self.delta.items():
            for input_symbol, state_input_transitions in \
                    state_transitions.items():
                for stack_symbol, transitions in \
                        state_input_transitions.items():
                    st = '{'
                    for transition in transitions:
                        st += '({}, {}), '.format(
                            transition.state,
                            tools.Tools.output_string_from_tokens(
                                transition.stack_symbols))
                    st = st[:-2]
                    st += '}'
                    s += '\t ({},{},{}) -> {}\n'.format(start_state,
                                                        input_symbol,
                                                        stack_symbol, st)
        return s[:-1]
