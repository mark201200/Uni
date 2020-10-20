#!/#!/usr/bin/env python3
"""Classes and methods for working with state-tape pairs."""

import base.base as base
import automata.tm.tape as tmt


class StateTapePair(base.Base):
    """
    A (state, tape) pair.

    It is hashable and immutable.

        Created by:
        StateTapePair()
        StateTapePair.init()
        StateTapePair.new()
        StateTapePair.initial_configuration()


     A StateTapePair is encoded as:
         - a string corresponding to a state
         - a TMTape instance

    """

    def __init__(self, *, state, tape):
        """Create a pair from state and Tape instance."""
        self.state = state
        self.tape = tape

    @classmethod
    def init(cls, *, state, input_str, head=None, blank_symbol=None):
        """Create a pair from state, tape content and head position."""
        return cls(state=state,
                   tape=tmt.TMTape.init(input_str=input_str,
                                        head=head,
                                        blank_symbol=blank_symbol))

    @classmethod
    def new(cls, *, state, list_of_tokens, head=None, blank_symbol=None):
        """Create a pair from state and stack items."""
        return cls(state=state,
                   tape=tmt.TMTape(list_of_tokens=list_of_tokens,
                                   head=head,
                                   blank_symbol=blank_symbol))

    @classmethod
    def initial_configuration(cls, list_of_tokens, tm):
        """Create a TM initial pair."""
        return cls(state=tm.initial_state,
                   tape=tmt.TMTape(list_of_tokens=list_of_tokens,
                                   blank_symbol=tm.blank_symbol))

    @property
    def tape_symbols(self):
        """Return the symbols in the tape in the pair as a string."""
        return self.tape.tape_symbols

    @property
    def tape_list_of_tokens(self):
        """Return the symbols in the tape in the pair as a tuple."""
        return self.tape.tape

    @property
    def head(self):
        """Return the position of the tape head in the pair."""
        return self.tape.head

    @property
    def state_tape_head(self):
        """Return the 3-tuple of state, list_of_tokens, and head positions."""
        return (self.state,
                self.tape_list_of_tokens,
                self.head)

    @property
    def current_symbol(self):
        """Return the tape symbol under the head."""
        return self.tape.current_symbol

    def update_pair(self, new_state, symbol, direction):
        """Return pair with new state and updated tape."""
        new_tape = self.tape.update_tape(symbol, direction)
        return StateTapePair(state=new_state, tape=new_tape)

    def __str__(self):
        """Return a string representation of the pair."""
        s = '({}, {})'.format(self.state, str(self.tape))
        return s

    def __eq__(self, other):
        """Check if two pairs are equal."""
        if isinstance(other, self.__class__):
            return (self.state == other.state) and \
                (self.tape_symbols == other.tape_symbols) and \
                (self.head == other.head)
        else:
            return False

    def __hash__(self):
        """Return hash value of pair."""
        return hash((self.tape_symbols, self.state, self.head))

    def __repr__(self):
        """Associate a description of the object to its identifier."""
        return '{}(\'{}, {}\')'.format(
            self.__class__.__name__,
            self.state,
            self.tape
        )
