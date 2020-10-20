#!/usr/bin/env python3
"""Classes and methods for working with left regular grammars."""

import grammar.base.grammar_exceptions as ge

import grammar.cf.cf_grammar as cfg
# import grammar.regular.right_regular_grammar as rrg
# import automata.fa.dfa as dfa
# import regexpr.regex_exceptions as rex


class RG(cfg.CFG):
    """
    A (left) regular grammar.

    Created by:
        RG(): definition provided as call parameters
        RG.load(file): definition provided in json file
        *RG.from_rrg(): derived from given right regular grammar
        *RG.from_dfa(): derived from given DFA
        *RG.from_regex(): derived from given regular expression

    A RG is coded as follows:
        - terminals are defined as strings
        - the set of terminals is a Python set of strings
        - nonterminals are defined as strings
        - the set of nonterminals is a Python set of strings
        - axiom is a string
        - productions is a Python dictionary where
            - keys are Python tuples of strings of length one
            - values are Python dicts where
                - keys are input symbols, including the empty string ''
                - values are sets of possibly empty Python tuples of strings
                A->a | aA | '' is coded as productions[('A',)]={('a',), ('a', 'A'), ()}
    """

    @classmethod
    def from_rrg(cls, right_rg):
        """Initialize this RG as one equivalent to the given right regular grammar."""
        return right_rg.rg

    @classmethod
    def from_dfa(cls, dfa):
        """Initialize this RG as one equivalent to the given DFA."""
        return dfa.rg

    @classmethod
    def from_regex(cls, regex):
        """Initialize this RG as one equivalent to the given regular expression."""
        return regex.rg


# -----------------------------------------------------------------------------
# Derivation

    @property
    def dfa(self):
        """Return DFA equivalent to this grammar."""
        # TO DO
        dfa = None
        return dfa

    @property
    def rrg(self):
        """Return right regular grammar equivalent to this grammar."""
        # TO DO
        rrg = None
        return rrg

# -----------------------------------------------------------------------------
# Validation

    def _validate_right_part(self, left_part, right_part):
        """
        Raise an error if the right part of a production is invalid.

        Checks that the right part is a (possibly empty) sequence composed by a
        terminal followed by a non terminal, or by a single terminal
        """
        super()._validate_right_part(left_part, right_part)
        if len(right_part) > 2:
            raise ge.InvalidRightPartError(
                      'right part of production {} -> {} is too long'.
                      format(left_part, right_part))
        if len(right_part) == 1:
            if right_part[0] not in self.terminals and left_part[0] != "S'":
                raise ge.InvalidRightPartError(
                     'right part of production {} -> {} is invalid'.
                     format(left_part, right_part))
        if len(right_part) == 2:
            if right_part[1] not in self.non_terminals:
                raise ge.InvalidRightPartError(
                     'right part of production {} -> {} is invalid'.
                     format(left_part, right_part))
