#!/usr/bin/env python3
"""Classes for working with all automata, including Turing machines."""

import abc

import base.base as base
import tools.tools as tools
import automata.base.automaton_exceptions as ae
import automata.base.computation as comp


class Automaton(base.Base, metaclass=abc.ABCMeta):
    """An abstract base class for all automata, including Turing machines."""

    def __init__(self, states, input_symbols, initial_state, final_states):
        """Initialize a complete automaton."""
        self.states = states.copy()
        self.input_symbols = input_symbols.copy()
        self.initial_state = initial_state
        self.final_states = final_states.copy()
        self.all_chars_input = tools.Tools.all_chars(self.input_symbols)

    def validate(self):
        """Return True if this PDA is internally consistent."""
        self._validate_states()
        self._validate_input_symbols()
        self._validate_initial_state()
        self._validate_final_states()
        self._validate_transitions()
        return True

    def _validate_states(self):
        """
        Raise an error if set of states is invalid.

        Checks that there exists at least one state symbol, all states
        are denoted as strings and no state is denoted by the empty string
        """
        if len(self.states) == 0:
            raise ae.InvalidStatesError(
                'no state defined in automaton')
        for s in self.states:
            if type(s) is not str:
                raise ae.InvalidStatesError(
                     'state {} in automaton is not a string'.format(s))
            if len(s) == 0:
                raise ae.InvalidStackSymbolsError(
                     'state denoted by the empty string')

    def _validate_input_symbols(self):
        """
        Raise an error if set of input symbols is invalid.

        Checks that there exists at least one input symbol and all symbols
        are chars
        """
        if len(self.input_symbols) == 0:
            raise ae.InvalidInputSymbolsError(
                'no stack symbol defined in PDA')
        for s in self.input_symbols:
            if type(s) is not str:
                raise ae.InvalidInputSymbolsError(
                     'input symbol {} in automaton is not a char'.format(s))

    def _validate_initial_state(self):
        """
        Raise an error if the initial state is invalid.

        Checks that an initial state is defined and it belongs to the
        set of states.
        """
        if self.initial_state is None:
            raise ae.InvalidStateError(
                'no initial state defined')
        if self.initial_state not in self.states:
            raise ae.InvalidStateError(
                '{} is not a valid initial state'.format(self.initial_state))

    def _validate_transitions(self):
        """Check that all transitions are valid."""
        for start_state, state_transitions in self.delta.items():
            self._validate_transition_initial_state(start_state)
            self._validate_transitions_from_state(
                start_state, state_transitions)

    def _validate_transition_initial_state(self, start_state):
        """
        Raise an error if the start state of a transition is invalid.

        Checks that the start state of a transition is defined and belongs to
        the set of states.
        """
        if start_state is None:
            raise ae.MissingStateError(
                'no start state defined')
        if start_state not in self.states:
            raise ae.InitialStateError(
                'start state {} is not valid'.format(start_state))

    def _validate_transitions_from_state(self, start_state, state_transitions):
        """Check that all transitions from a given state are valid."""
        for input_symbol, input_symbol_transitions in \
                state_transitions.items():
            self._validate_transition_is(start_state, input_symbol)
            self._validate_transitions_from_state_and_is(
                start_state, input_symbol, input_symbol_transitions)

    def copy(self) -> object:
        """Create a deep copy of the automaton."""
        d = vars(self).copy()
        return self.__class__(**d)

    @abc.abstractmethod
    def _initial_configuration(self):
        """Return the initial configuration wrt the given input string."""
        raise NotImplementedError

    @abc.abstractmethod
    def _transition(self):
        """Check delta for values to be included in the new configuration."""
        raise NotImplementedError

    @abc.abstractmethod
    def _next_configuration(self):
        """Return next configuration."""
        raise NotImplementedError

    def computation(self, list_of_tokens):
        """
        Return iterator for computation.

        Define a computation from list_of_tokens as an iterator of the
        corresponding configurations
        """
        current_config = self._initial_configuration(list_of_tokens)
        yield current_config
        while not current_config.is_final:
            current_config = self._next_configuration(current_config)
            yield current_config

    def step(self, comp):
        """
        Apply the computation on list_of_tokens in a step-by-step manner.

        Yield the current configuration of the DFA at each step.
        """
        try:
            config = next(comp)
            print(config)
        except StopIteration:
            print(config.is_accepting)

    def compute(self, list_of_tokens):
        """
        Perform the computation on the input string.

        Returns the sequence of configurations traversed and the result
        """
        c = comp.Computation.empty(self)
        completed = True
        try:
            for config in self.computation(list_of_tokens):
                c.add_configuration(config)
        except ae.UndefinedTransitionException:
            completed = False
        if completed:
            accepted = config.is_accepting
        else:
            accepted = False
        return (c, completed, accepted)

    def report_computation(self, list_of_tokens):
        """
        Report sequence of configurations in computation.

        Returns the sequence of configurations traversed and the final result.
        """
        c, completed, accepted = self.compute(list_of_tokens)
        for conf in c.generator:
            print(conf)
        if completed:
            if accepted:
                print('Completed computation: string accepted')
            else:
                print('Completed computation: string rejected')
        else:
            print('Incomplete computation: string rejected')
        return

    def random_deterministic_path(self, list_of_tokens):
        """
        Return iterator for a deterministic computation path.

        Define a computation path from list_of_tokens as an iterator of the
        corresponding deterministic configurations
        """
        current_config = self._initial_deterministic_configuration(list_of_tokens)
        yield current_config
        while not current_config.is_final:
            current_config = self._next_random_deterministic_configuration(
                current_config)
            yield current_config

    def derive_random_deterministic_path(self, list_of_tokens):
        """
        Perform a deterministic computation path on the input string.

        Returns the sequence of configurations traversed and the result
        """
        c = comp.Computation.empty(self)
        completed = True
        try:
            for config in self.random_deterministic_path(list_of_tokens):
                c.add_configuration(config)
        except ae.UndefinedTransitionException:
            completed = False
        if completed:
            accepted = config.is_accepting
        else:
            accepted = False
        return (c, completed, accepted)

    def report_random_deterministic_path(self, list_of_tokens):
        """
        Report sequence of configurations in computation.

        Returns the sequence of configurations traversed and the final result.
        """
        c, completed, accepted = \
            self.derive_random_deterministic_path(list_of_tokens)
        for conf in c.generator:
            print(conf)
        if completed:
            if accepted:
                print('Completed path: string accepted')
            else:
                print('Completed path: string rejected')
        else:
            print('Incomplete path: string rejected')
        return
