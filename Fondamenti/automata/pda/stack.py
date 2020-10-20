#!/usr/bin/env python3
"""Classes and methods for working with PDA stacks."""


import base.base as base
import tools.tools as tools
import automata.pda.pda_exceptions as pae


class PDAStack(base.Base):
    """
    A PDA stack.

    It is hashable and immutable.

        Created by:
        PDAStack()
        PDAStack.init()
        PDAStack.new()
        PDAStack.initial_stack()


    A PDAStack is coded as a possibly empty Python tuple of strings

    """

    def __init__(self, *, list_of_stack_items):
        """
        Create the new PDA stack from a list.

        The parameter is a sequence of input tokens as a Python tuple
        """
        if isinstance(list_of_stack_items, str):
            self.stack_items = (list_of_stack_items,)
        else:
            self.stack_items = list_of_stack_items

    @classmethod
    def init(cls, *, stack_str):
        """
        Create the new PDA stack from a string.

        The parameter is a string of chars (assuming tokens have length 1)
        """
        return cls(list_of_stack_items=tools.Tools.tokens(stack_str, separator=''))

    @classmethod
    def new(cls, stack_items):
        """
        Create the new PDA stack from a list.

        The parameter is a sequence of input tokens as a Python list
        """
        return cls(list_of_stack_items=tuple(stack_items))

    @classmethod
    def initial_stack(cls, token):
        """Create a PDA stack containing the specified symbol."""
        return cls(list_of_stack_items=(token,))

    def update_stack(self, tokens):
        """
        Return a new stack derived from the original one, according to transition.

        Update stack contents popping the top of this stack
        and pushing symbols in symbols
        A new stack is returned with the resulting contents
        """
        lst = list(self.stack_items)
        if lst:
            _ = lst.pop()
            lst1 = list(tools.Tools.tuple_from_sequence(tokens))
            lst.extend(lst1)
            return PDAStack.new(lst)
        else:
            raise pae.EmptyStack('empty stack')

    @property
    def top(self):
        """Return the symbol at the top of the stack."""
        if self.stack_items:
            return self.stack_items[-1]
        else:
            raise pae.EmptyStack('empty stack')

    @property
    def rest(self):
        """Return a new stack with all symbols apart from the top of the stack."""
        if self.stack_items:
            return PDAStack(list_of_stack_items=self.stack_items[:-1])
        else:
            raise pae.EmptyStack('empty stack')

    @property
    def pop(self):
        """Return the top symbol of the stack and a new stack with the other symbols."""
        if self.stack_items:
            lst = list(self.stack_items)
            c = lst.pop()
            return c, PDAStack.new(lst)
        else:
            raise pae.EmptyStack('empty stack')

    def push(self, list_of_tokens):
        """Return a new stack with the top of the original stack by the given symbols."""
        lst = list(self.stack_items)
        lst1 = list(list_of_tokens)
        lst.extend(lst1)
        return PDAStack.new(lst)

    @property
    def items(self):
        """Return stack items."""
        return self.stack_items

    @property
    def is_empty(self):
        """Return True if stack is empty."""
        return not self.stack_items or len(self.stack_items) == 0

    @property
    def size(self):
        """Return the number of symbols on the stack."""
        return len(self.stack_items)

    @property
    def iter(self):
        """Return an interator for the stack."""
        return iter(self.stack_items)

    def __str__(self):
        """Return a string representation of the stack."""
        s = '{}'.format(tools.Tools.print_tuple(self.stack_items))
        return s

    def __hash__(self):
        """Compute hash value of stack."""
        return hash(self.items)

    def __eq__(self, other):
        """Equality test between stacks."""
        if isinstance(other, self.__class__):
            return self.items == other.items
        else:
            return False

    def __repr__(self):
        """Return a string representation of the stack."""
        s = self.__class__.__name__
        if isinstance(self.items, str):
            s += " ('{}')".format(self.items)
        else:
            s += ' {}'.format(self.items)
        return s
