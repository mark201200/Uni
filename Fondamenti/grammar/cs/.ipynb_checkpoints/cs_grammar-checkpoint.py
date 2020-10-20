#!/usr/bin/env python3
"""Classes and methods for working with context free grammars."""

import grammar.base.grammar_exceptions as ge

import grammar.general.general_grammar as gg


class CSG(gg.GG):
    """
    A context sensitive grammar.

    Created by:
        CSG(): definition provided as call parameters
        CSG.load(file): definition provided in json file

    A CSG is encoded as follows:
        - terminals are defined as strings
        - the set of terminals is a Python set of strings
        - nonterminals are defined as strings
        - the set of nonterminals is a Python set of strings
        - axiom is a string
        - productions is a Python dictionary where
            - keys are Python tuples of strings of length at least one
            - values are Python dicts where
                - keys are input symbols
                - values are sets of possibly empty Python tuples of strings
                Ab->a | AaA | bb is encoded as
                    productions[('A', 'b')]={('a',), ('A', 'a', 'A'), ('b', 'b')}
    """

    def __init__(self, *, terminals, non_terminals, axiom, productions):
        """Initialize grammar."""
        super().__init__(terminals=terminals, non_terminals=non_terminals, axiom=axiom, 
                         productions=productions)

    # def _validate_left_part(self, left_part, right_parts):
    #     """
    #     Raise an error if the left part of a production is invalid.

    #     Checks that the left part contains at least one non terminal.
    #     """
    #     super()._validate_left_part(left_part, right_parts)
    #     if set(left_part).isdisjoint(self.non_terminals):
    #         raise ge.InvalidLeftPartError(
    #              'left part {} of productions has no nonterminal'.format(left_part))

    def _validate_right_part(self, left_part, right_part):
        """
        Raise an error if the right part of a production is invalid.

        Checks that the right part is a (possibly empty) sequence of terminals
        and non terminals
        """
        super()._validate_right_part(left_part, right_part)
        if not set(right_part).issubset(self.terminals.union(self.non_terminals)):
            raise ge.InvalidRightPartError('production {} -> {} is not valid'
                                           .format(left_part, right_part))
        if len(right_part) < len(left_part):
            raise ge.InvalidRightPartError('production {} -> {} is not context sensitive'
                                           .format(left_part, right_part))
