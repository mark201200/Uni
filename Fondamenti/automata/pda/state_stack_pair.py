#!/#!/usr/bin/env python3
"""Classes and methods for working with state-stack pairs."""

import base.base as base

import tools.tools as tools
import automata.pda.stack as stk


class StateStackPair(base.Base):
    """
    A (state, stack) pair.

    It is hashable and immutable.

        Created by:
        StateStackPair()
        StateStackPair.init()
        StateStackPair.new()
        StateStackPair.initial_configuration()


     A StateStackPair is coded as:
         - a string corresponding to a state
         - a PDAStack instance

    """

    def __init__(self, *, state, stack):
        """
        Create a pair from state and PDAStack instance.
        
        Parameters are a state, given as a string, and a PDAStack instance
        """
        self.state = state
        self.stack = stack

    @classmethod
    def init(cls, *, state, stack_str, separator=None):
        """
        Create a pair from state and stack items as string.
        
        Parameters are a state, given as a string, and the sequence of stack items,
        given as string (assuming items have lenght 1)
        """
        return cls(state=state,
                   stack=stk.PDAStack.init(stack_str=stack_str))

    @classmethod
    def new(cls, state, list_of_stack_items):
        """Create a pair from state and stack items as tuple.
        
        Parameters are a state, given as a string, and the the sequence of stack items,
        given as Python tuple
        """
        if isinstance(list_of_stack_items, str):
            return cls(state=state,
                   stack=stk.PDAStack(list_of_stack_items=(list_of_stack_items)))
        else:
            return cls(state=state,
                   stack=stk.PDAStack(list_of_stack_items=list_of_stack_items))

    @classmethod
    def initial_configuration(cls, dpda):
        """Create a DPDA initial pair."""
        return cls(state=dpda.initial_state,
                   stack=stk.PDAStack.initial_stack(dpda.initial_stack_symbol))

# ---------------------------------------------------------------------------

    @property
    def stack_items(self):
        """Return the items in the stack in the pair."""
        return self.stack.items

    @property
    def has_empty_stack(self):
        """Return True if the stack in the pair is empty."""
        return self.stack.is_empty

    @property
    def top_of_stack(self):
        """Return the top stack symbol in the pair."""
        return self.stack.top

    @property
    def rest_of_stack(self):
        """Return the rest of the stack apart the top symbol."""
        return StateStackPair(state=self.state, stack=self.stack.rest)

    def update(self, new_state, to_push):
        """Return pair with new state and updated stack."""
        return StateStackPair(state=new_state,
                              stack=self.stack.update_stack(to_push))

    def __str__(self):
        """Return a string representation of the pair."""
        s = '({}, {})'.format(self.state, self.stack)
        return s

    def __eq__(self, other):
        """Check if two pairs are equal."""
        if isinstance(other, self.__class__):
            return (self.state == other.state) and \
                (self.stack_items == other.stack_items)
        else:
            return False

    def __hash__(self):
        """Return hash value of pair."""
        return hash((tools.Tools.string_from_tokens(self.stack_items), self.state))

    def __repr__(self):
        """Return a string representation of the pair."""
        s = '{} ({}, {} '.format(self.__class__.__name__, 
                                  self.state, 
                                  self.stack.__class__.__name__)
        if isinstance(self.stack.items, str):
            s += "('{}'))".format(self.stack.items)
        else:
            s += '{})'.format(self.stack.items)
        return s
