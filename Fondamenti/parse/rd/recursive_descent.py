#!/usr/bin/env python3
"""
Implementation of parsing through recursive descent.

The CFG grammar is assumed
"""

import base.base as base
import tools.tools as tools
import parse.base.parser_exceptions as pre
import grammar.cf.cf_grammar as cfg
import grammar.base.derivation as der
import grammar.cf.syntax_tree as st


class RD_parser(base.Base):
    """A parser based on (leftmost) recursive descent."""

    def __init__(self, grammar):
        """Initialize."""
        self.parse_table = None
        self.length = 0
        if not isinstance(grammar, cfg.CFG):
            raise Exception('Grammar is not CF')
        self.grammar = grammar
        self.validate_not_left_recursive()

    def validate_not_left_recursive(self):
        """Check that the grammar is not left recursive."""
        if len(self.grammar.productions) == 0:
            pre.InvalidGrammarException('no production in grammar')
        for left_part, right_parts in self.grammar.productions.items():
            for right_part in right_parts:
                if len(right_part) > 0:
                    if left_part[0] == right_part[0]:
                        raise pre.InvalidGrammarException(
                            'production {} -> {} is left recursive'
                            .format(left_part, right_part))
                elif left_part[0] != self.grammar.axiom:
                    raise pre.InvalidGrammarException(
                            'production {} -> {} is not allowed:\
                                epsilon production only from axiom'
                            .format(left_part, right_part))

    def parse(self, list_of_tokens):
        """Parse a sentence (string) with the CYK algorithm ."""
        if len(list_of_tokens) > 0:
            d = self.get_derivations(list_of_tokens)
            if len(d) == 0:
                raise pre.StringNotAccepted('String not accepted')
            elif len(d) > 1:
                raise pre.AmbiguousDerivation('Ambiguous grammar: multiple derivations')
            else:
                print('String accepted')
                return d[0].syntax_tree
        else:
            if self.grammar.null_string_produced:
                print('String accepted')
                return st.Syntax_tree.null_st(self.grammar)
            else:
                raise pre.StringNotAccepted('String not accepted')

    def get_derivations(self, tokens):
        """Return left derivations if string is generated in grammar."""
        grammar = self.grammar
        nt = (grammar.axiom,)
        derivations = []
        if not tokens:
            derivation = der.Left_derivation.empty(grammar)
            step = der.Step(left=(nt,),
                            right=tuple(),
                            phrase=(nt,),
                            next_phrase=tuple(),
                            start_index=0,
                            grammar=grammar)
            derivation.append_step(step)
            derivations.append(derivation)
        else:
            generator = self._match_nonterminal(nt, tokens)
            for derivation in generator:
                d = der.Left_derivation.empty(grammar)
                for i, p in enumerate(derivation):
                    if i == 0:
                        step = der.Step(left=p[0],
                                        right=p[1],
                                        phrase=p[0],
                                        next_phrase=p[1],
                                        start_index=0,
                                        grammar=grammar)
                        d.append_step(step)
                    else:
                        phrase = d.steps[i-1].next_phrase
                        ind = tools.Tools.first_nt(phrase, grammar.non_terminals)
                        next_phrase = list(phrase)
                        next_phrase[ind:ind+1] = p[1]
                        step = der.Step(left=p[0],
                                        right=p[1],
                                        phrase=phrase,
                                        next_phrase=tuple(next_phrase),
                                        start_index=ind,
                                        grammar=grammar)
                        d.append_step(step)
                derivations.append(d)
        return derivations

    def _match_nonterminal(self, nt, tokens):
        """
        Generate all ways to derive a string from nonterminal.

        At each step, provides a sequence of productions
        """
        # generate all ways to derive any prefix of the list of tokens
        # from the given nonterminal
        generator = self._match_nonterminal_on_prefix(nt, tokens)
        # check that the remaining suffix, not produced by the derivation,
        # is null: in that case, return the derivation of the whole list
        # of tokens
        for derivation, suffix in generator:
            if derivation is not None:
                if len(suffix) == 0:
                    yield derivation

    def _match_nonterminal_on_prefix(self, nt, tokens):
        """
        Generate all ways to derive a string prefix from nonterminal.

        At each step, provides a sequence of productions and the remaining
        prefix
        """
        # derive the list of rightparts immediately produced by the
        # given nonterminal
        right_parts = self.grammar.get_right_parts(nt)
        for rp in right_parts:
            # consider the production from the nonterminal to any rightpart
            # in list
            production = [(nt, rp)]
            # generate all ways to derive any prefix of the list of
            # tokens from the right part of the production, hence from
            # the given nonterminal, by applying the production nt->rp
            # as first derivation step
            generator = self._match_rightpart_on_prefix(rp, tokens)
            # for each such derivations, insert the production from
            # nonterminal to rightpart as the first step and yield the
            # resulting derivation
            for derivation, suffix in generator:
                if derivation is not None:
                    production.extend(derivation)
                    yield production, suffix

    def _match_rightpart_on_prefix(self, rp, tokens):
        """
        Generate all ways to derive string from phrase.

        At each step, provides a sequence of productions and the remaining
        suffix
        """
        # rightpart has no symbol: return the empty derivation and the whole
        # list of tokens as non derived suffix
        if len(rp) == 0:
            derivation = []
            yield (derivation, tokens)
        # the list of tokens is empty while some suffix of righpart has still
        # to be considered for the derivation: as a consequence, a prefix of
        # the list of tokens is not derived from the rightpart
        elif len(tokens) == 0:
            yield (None, tokens)
        else:
            first = (rp[0],)
            rest = rp[1:]
            first_token = (tokens[0],)
            rest_of_tokens = tokens[1:]
            if first[0] in self.grammar.terminals:
                if first == first_token:
                    generator = self._match_rightpart_on_prefix(rest, rest_of_tokens)
                    for derivation, suffix in generator:
                        if derivation is not None:
                            yield derivation, suffix
            else:
                generator = self._match_nonterminal_on_prefix(first, tokens)
                for derivation, suffix in generator:
                    generator1 = self._match_rightpart_on_prefix(rest, suffix)
                    for derivation1, suffix1 in generator1:
                        if derivation1 is not None:
                            derivation.extend(derivation1)
                            yield derivation, suffix1

    def __str__(self):
        """Return a string representation of the parser."""
        s = 'grammar:\n'+str(self.grammar)
        return s
