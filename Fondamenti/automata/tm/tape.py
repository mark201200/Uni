#!/usr/bin/env python3
"""Classes and methods for working with Turing machine tapes."""

import base.base as base
import tools.tools as tools


class TMTape(base.Base):
    """
    A Turing machine tape.

    It is hashable and immutable.

        Created by:
        TMTape()
        TMTape.init()
        TMTape.update_tape()


    A TMTape is coded as a possibly empty Python tuple of strings, an integer,
    denoting head position, and a string corresponding to the tape blank symbol

    """

    def __init__(self, *, list_of_tokens, blank_symbol=None, head=None):
        """
        Initialize tape.

        list_of_tokens is a tuple
        """
        if not head:
            self.head = 0
        else:
            self.head = head
        if not blank_symbol:
            self.blank_symbol = '|'
        else:
            self.blank_symbol = blank_symbol
        list_of_tokens = tools.Tools.tuple_from_sequence(list_of_tokens)
        if self.head < 0:
            tape = [self.blank_symbol]*(-head)+list(list_of_tokens)
            self.head = 0
            self.tape = tuple(tape)
        elif self.head >= len(list_of_tokens):
            tape = list(list_of_tokens)+[self.blank_symbol]*(self.head -
                                                             len(list_of_tokens)+1)
            self.tape = tuple(tape)
        else:
            self.tape = list_of_tokens

    @classmethod
    def init(cls, *, input_str, head=None, blank_symbol=None):
        """
        Initialize tape.

        input_str is a string with tokens delimited by config.token_separator
        """
        return cls(list_of_tokens=tools.Tools.tokens(input_str, separator=''),
                   head=head,
                   blank_symbol=blank_symbol)

    @property
    def tape_symbols(self):
        """Return the tape content as a string."""
        return ' '.join(self.tape)

    @property
    def current_symbol(self):
        """Read the symbol at the current position in the tape."""
        return self.tape[self.head]

    def update_tape(self, new_symbol, direction):
        """
        Update tape according to transition.

        Update tape contents modifying the current cell and moving the head.
        A new tape is returned with the resulting contents
        """
        lst = list(self.tape)
        head = self.head
        lst[head] = new_symbol
        if direction == 'R':
            if head == len(lst)-1:
                lst.append(self.blank_symbol)
                head += 1
            elif head == 0 and \
                    lst[head] == self.blank_symbol and len(lst) > 1:
                lst = lst[1:]
            else:
                head += 1
        else:
            if head == 0:
                lst.insert(0, self.blank_symbol)
            elif head == len(lst)-1 and lst[head] == self.blank_symbol and len(lst) > 1:
                lst = lst[:-1]
                head -= 1
            else:
                head -= 1
        return TMTape(list_of_tokens=tuple(lst),
                      blank_symbol=self.blank_symbol,
                      head=head)

    @property
    def items(self):
        """Return tape content as string."""
        return tools.Tools.string_from_tokens(self.list_of_tokens)

    def __len__(self):
        """Return the number of symbols on the tape."""
        return len(self.tape)

    def __iter__(self):
        """Return an interator for the tape."""
        return iter(self.tape)

    def __eq__(self, other):
        """Equality test between stacks."""
        if isinstance(other, self.__class__):
            return self.tape_symbols == other.tape_symbols and self.head == other.head
        else:
            return False

    def __str__(self):
        """Return a string representation of the tape."""
        s = '({}, {})'.format(tools.Tools.print_tuple(self.tape), self.head)
        return s

