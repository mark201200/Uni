#!/usr/bin/env python3
"""Implementation of parsing through the CYK algorithm."""

import base.base as base
import parse.base.parser_exceptions as pre

import grammar.cf.cf_grammar as cfg
import parse.cyk.cyk_table as ct
import grammar.cf.syntax_tree as st
import tools.tools as tools


class CYK_parser(base.Base):
    """A parser based on the CYK algorithm."""

    def __init__(self, grammar):
        """Initialize."""
        self.grammar_rules = tools.Dict_of_sets()
        if not isinstance(grammar, cfg.CFG):
            raise Exception('Grammar is not CF')
        if grammar.cnf:
            self.grammar = grammar
        else:
            self.grammar = grammar.to_cnf()
        for left_part, right_parts in grammar.productions.items():
            for right_part in right_parts:
                self.grammar_rules[right_part] = left_part

    def parse(self, list_of_tokens):
        """Parse a sentence (string) with the CYK algorithm ."""
        # case of null string production
        if len(list_of_tokens) > 0:
            pt = self.derive_cyk_table(list_of_tokens)
            if not pt.successful:
                raise pre.StringNotAccepted('String not accepted')
            elif pt.ambiguous:
                raise pre.AmbiguousDerivation('Ambiguous grammar: multiple derivations')
            else:
                print('String accepted')
                return pt.syntax_tree
        else:
            if self.grammar.null_string_produced:
                print('String accepted')
                return st.Syntax_tree.null_st(self.grammar)
            else:
                raise pre.StringNotAccepted('String not accepted')

    def derive_cyk_table(self, list_of_tokens):
        """Derive a CYK parse table for the given list_of_tokens."""
        grammar = self.grammar
        grammar_rules = grammar.grammar_rules
        self.number_of_trees = 0
        number_of_tokens = len(list_of_tokens)
        if number_of_tokens < 1:
            raise pre.InvalidStringException(
                'string to be parsed is empty: cyk table cannot be built')
        if not set(list_of_tokens).issubset(grammar.terminals):
            raise pre.InvalidStringException(
                'string include symbol non terminals for the grammar.')
        cyk_table = ct.CYK_table(number_of_tokens, list_of_tokens, grammar)
        for start_index, terminal in enumerate(list_of_tokens):
            # select all terminal production producing the symbol
            tt = terminal
            left_parts = grammar_rules.get((tt,))
            if left_parts is None:
                raise pre.ParsingError("Terminal " + terminal +
                                       " is not produced in the grammar")
            else:
                # for each non terminal producing the symbol
                for left_part in left_parts:
                    # insert the terminal production in the corresponding cell
                    cyk_table.terminal_cell(1, start_index, left_part[0], tt)
        list_of_rules = []
        # for each row in the table (length os substrings considered)
        for substring_length in range(2, number_of_tokens+1):
            # for each column in the table
            # (starting index of a substring in the string)
            for starting_index in range(0, number_of_tokens-substring_length+1):
                # for each possible right part of a non terminal production
                # (splitting index in the substring)
                cyk_table.empty_nonterminal_cell(substring_length, starting_index)
                for splitting_index in range(1, substring_length):
                    # select possible productions for the first part and
                    # the second part of the splitted substring
                    first_cell = cyk_table.cell(splitting_index, starting_index)
                    first_part_productions = first_cell.productions
                    second_cell = cyk_table.cell(substring_length-splitting_index,
                                                 starting_index+splitting_index)
                    second_part_productions = second_cell.productions
                    # loop over all pairs of non terminals producing the first
                    # and the second part of the splitted substring
                    for first_part_production in first_part_productions:
                        for second_part_production in second_part_productions:
                            # select all non terminals producing the sequence
                            # of the two non terminals considered in the loop
                            lot = (first_part_production.left,
                                   second_part_production.left)
                            set_of_nt = grammar_rules.get(lot)
                            if set_of_nt:
                                for nt in set_of_nt:
                                    rule = (
                                            (starting_index, substring_length),
                                            nt[0],
                                            (starting_index, splitting_index),
                                            (starting_index+splitting_index,
                                             substring_length-splitting_index
                                             )
                                            )
                                    list_of_rules.append(rule)
                                    cyk_table.cell(
                                        substring_length,
                                        starting_index).\
                                        add_nonterminal_production(nt[0],
                                                                   first_cell,
                                                                   second_cell)
        cyk_table.filled = True
        return cyk_table

    def __str__(self):
        """Return a string representation of the parser."""
        s = 'grammar:\n'+str(self.grammar)+'\n'
        s += 'inverse rules:\n'
        for left, right in self.grammar_rules.items():
            s += tools.Tools.output_string_from_tokens(left)+' -> {'
            for r in right:
                s += tools.Tools.output_string_from_tokens(r)+' ,'
            s = s[:-2]
            s += '}\n'
        return s

    def __repr__(self):
        """Associate a description of the object to its identifier."""
        return '{}[\ngrammar: {}\ninverse rules:{}\n)'.format(
                self.__class__.__name__,
                self.grammar,
                self.grammar_rules
                )
