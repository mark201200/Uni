#!/usr/bin/env python3
"""Classes and methods for working with regular expressions."""

import json
import random

import base.base as base
import tools.tools as tools
import regexpr.regex_exceptions as re

import automata.fa.nfa as nf
import grammar.cf.cf_grammar as cfg
import grammar.regular.regular_grammar as rg
import parse.rd.recursive_descent as rdp
import grammar.cf.syntax_tree as syt


class RegEx(base.Base):
    """
    A regular expression.

        Created by:
        RegEx(): definition provided as call parameters

    """

    def __init__(self, *, alphabet, expression):
        """Initialize a complete Turing machine."""
        self.alphabet = alphabet.copy()
        self.input_expression = expression
        self.expression = self.make_canonical()
        self.grammar = self._set_grammar()
        self.all_chars = tools.Tools.all_chars(self.alphabet)
        self.validate()
        self._syntax_tree = self.syntax_tree
        self.includes_null = self._includes_null()

    @property
    def canonical(self):
        """
        Derive a canonical regular expression from the one in input.

        An equivalent regular expression is derived where operators are always
        explicit and that does not assume operator precedence or left
        associativity. The structure of the expression is only based on
        parenthesization.
        """
        terminals = self.alphabet
        tokens = self.input_expression
        if len(tokens) == 0:
            return []
        l1 = []
        # add dots
        for i, v in enumerate(tokens):
            if i > 0:
                if v in terminals.union({'('}) and tokens[i-1] in terminals.union({'*'}):
                    l1.append('.')
                if v in terminals and tokens[i-1] == ')':
                    l1.append('.')
                if v == '(' and tokens[i-1] in terminals:
                    l1.append('.')
            l1.append(v)
        lst = l1
        l1 = []
        # insert parentheses around +, double parentheses, add initial and
        # final parentheses
        for i, v in enumerate(lst):
            if v == '+':
                l1.extend([')', v, '('])
            elif v in {'(', ')'}:
                l1.extend([v, v])
            else:
                l1.append(v)
        l1.insert(0, '(')
        l1.insert(0, '(')
        l1.append(')')
        l1.append(')')
        lst = l1
        # insert parenthesis to model left associativity
        plus_stack = []
        dot_stack = []
        stack = []
        l1 = []
        for i, v in enumerate(lst):
            if v == '+':
                if len(plus_stack) == 0 or plus_stack[-1] != len(stack):
                    plus_stack.append(len(stack))
                else:
                    l1.insert(stack[-1], '(')
                    l1.append(')')
            elif v == '.':
                if len(dot_stack) == 0 or dot_stack[-1] != len(stack):
                    dot_stack.append(len(stack))
                else:
                    l1.insert(stack[-1], '(')
                    l1.append(')')
            elif v == '(':
                stack.append(len(l1))
            elif v == ')':
                if len(plus_stack) > 0 and plus_stack[-1] == len(stack):
                    plus_stack.pop()
                if len(dot_stack) > 0 and dot_stack[-1] == len(stack):
                    dot_stack.pop()
                stack.pop()
            l1.append(v)
        lst = l1
        # reduce the number of parentheses wherever possible, to
        # simplify expression
        stack = []
        l1 = []
        cp_counter = 0
        for i, v in enumerate(lst):
            if v == '(':
                stack.append(len(l1))
                l1.append('(')
            elif v == ')':
                if l1[-1] in terminals and l1[-2] == '(':
                    # simplify (a) to a
                    l1.pop(stack[-1])
                    stack.pop()
                elif l1[-2] in terminals and l1[-1] == '*' and l1[-3] == '(':
                    # simplify (a*) to a*
                    l1.pop(stack[-1])
                    stack.pop()
                else:
                    # ) closes an expression of more than one terminals
                    # increase counter of the length of ) sequence
                    cp_counter += 1
            else:
                if cp_counter > 0:
                    # this character immediately follows a sequence of )
                    # of length cp_counter
                    k = 1
                    while k < cp_counter and stack[-1] == stack[-2] + k:
                        # delete a ( from the list to be returned and
                        # increase the number of ) not considered
                        l1.pop(stack[-2])
                        stack.pop(-2)
                        k += 1
                    # there are still cp_counter-k+1 ) to insert
                    for j in range(cp_counter-k+1):
                        l1.append(')')
                        stack.pop()
                    cp_counter = 0
                l1.append(v)
        while cp_counter > 0:
            if len(stack) == 1 or stack[-1] > stack[-2] + 1:
                l1.append(')')
            else:
                l1.pop(stack[-1])
            stack.pop()
            cp_counter -= 1
        return l1

    def _set_grammar(self):
        """Return CFG associated to RE definition."""
        grammar = cfg.CFG(
            terminals=self.alphabet.union({'(', ')', '+', '*', '.'}),
            non_terminals={'S', 'A', 'B'},
            axiom='S',
            productions={
                'S': {'A'},
                'A': self.alphabet.union({('(', 'A', ')'),
                                          ('(', 'A', '+', 'A', ')'),
                                          ('(', 'A', '.', 'A', ')'),
                                          ('B', '*')}),
                'B': self.alphabet.union({('(', 'A', '.', 'A', ')'),
                                          ('(', 'A', '+', 'A', ')'),
                                          ('(', 'A', ')')}),
                },
            no_null_production=True,
            null_string_produced=True
            )
        return grammar

    def validate(self):
        """Return True if this RG is internally consistent."""
        if not self._check_syntax():
            raise re.InvalidREStructure('Syntactically incorrect RE')
        return True

    def _check_syntax(self):
        """Return True if this RG is syntactically correct."""
        d = rdp.RD_parser(self.grammar).get_derivations(self.expression)
        if len(d) == 1:
            self._syntax_tree = d[0].syntax_tree
        return len(d) == 1

    @property
    def syntax_tree(self):
        """Return the syntax tree associated to the RE structure."""
        if self._syntax_tree is None:
            self._syntax_tree = rdp.RD_parser(self.grammar).parse(self.expression)
        return self._syntax_tree

    def _includes_null(self):
        """Return true if the null string belongs to the associated language."""
        def check_null(node):
            if isinstance(node, syt.Terminal_node):
                return False
            else:
                if len(node.children) == 1:
                    # S->A
                    return check_null(node.children[0])
                elif len(node.children) == 2:
                    # A->B*
                    return True
                elif len(node.children) == 3:
                    # A-> (A), B->(A)
                    return check_null(node.children[1])
                elif node.children[2].symbol == '+':
                    # A->(A+A), B->(A+A)
                    return check_null(node.children[1]) or check_null(node.children[3])
                else:
                    # A->(A.A), B->(A.A)
                    return check_null(node.children[1]) and check_null(node.children[3])

        if not self.expression:
            return True
        else:
            st = self.syntax_tree
            return check_null(st.root)

# -----------------------------------------------------------------------------
# Derivation

    @property
    def nfa(self):
        """Return DFA equivalent to this regular expression."""
        # stub: to be completed
        nfa = None
        return nfa

    @property
    def reg_grammar(self):
        """Return RG equivalent to this regular expression."""
        # stub: to be completed
        grammar = None
        return grammar

    @property
    def lr_grammar(self):
        """Return left regular grammar equivalent to this regular expression."""
            # TO DO
        lrg = None
        return lrg

# -----------------------------------------------------------------------------
# Other

    def equivalent(self, regex):
        """Return true if this regex is equivalent to the one given in input."""
        # nfa accepting language L1 described by this regex
        nfa1 = self.nfa
        # nfa accepting language L2 described by given regex
        nfa2 = regex.nfa
        # nfa accepting L1-L2
        nfa12 = nf.NFA.intersection(nfa1, nf.NFA.compl(nfa2))
        # nfa accepting L2-L1
        nfa21 = nf.NFA.intersection(nfa2, nf.NFA.compl(nfa1))
        return nfa12.empty and nfa21.empty

    def random_string(self, iteration_probability=.8,
                      iteration_probability_decrease=.65):
        """Return a random string described by the regular expression."""
        rs = self._random_string_from_subtree(self.syntax_tree.root,
                                              iteration_probability,
                                              iteration_probability_decrease)
        return tools.Tools.phrase(rs)

    def _random_string_from_subtree(self, current, iteration_probability,
                                    iteration_probability_decrease):
        if isinstance(current, syt.Terminal_node):
            rs = [current.symbol]
        else:
            nt = current.symbol
            if nt == 'S':
                # S->A
                rs = self._random_string_from_subtree(current.children[0],
                                                      iteration_probability,
                                                      iteration_probability_decrease)
            elif nt == 'A':
                if current.children[0].symbol == 'B':
                    # A->B*
                    rs = []
                    check_value = random.random()
                    check_probability = iteration_probability
                    while check_value < check_probability:
                        rs.extend(self._random_string_from_subtree(
                            current.children[0],
                            iteration_probability,
                            iteration_probability_decrease))
                        check_probability *= iteration_probability_decrease
                        check_value = random.random()
                elif len(current.children) == 3:
                    # A->(A)
                    rs = self._random_string_from_subtree(
                        current.children[1],
                        iteration_probability,
                        iteration_probability_decrease)
                elif len(current.children) == 5:
                    if current.children[2].symbol == '+':
                        # A->(A+A)
                        check_value = random.random()
                        if check_value < .5:
                            rs = self._random_string_from_subtree(
                                current.children[1],
                                iteration_probability,
                                iteration_probability_decrease)
                        else:
                            rs = self._random_string_from_subtree(
                                current.children[3],
                                iteration_probability,
                                iteration_probability_decrease)
                    else:
                        # A->(A.A)
                        rs = self._random_string_from_subtree(
                            current.children[1],
                            iteration_probability,
                            iteration_probability_decrease)
                        l1 = self._random_string_from_subtree(
                            current.children[3],
                            iteration_probability,
                            iteration_probability_decrease)
                        rs.extend(l1)
                else:
                    # A-> terminal
                    rs = self._random_string_from_subtree(
                        current.children[0],
                        iteration_probability,
                        iteration_probability_decrease)
            else:
                if len(current.children) == 3:
                    # B->(A)
                    rs = self._random_string_from_subtree(
                        current.children[1],
                        iteration_probability,
                        iteration_probability_decrease)
                elif len(current.children) == 5:
                    if current.children[2].symbol == '+':
                        # B->(A+A)
                        check_value = random.random()
                        if check_value < .5:
                            rs = self._random_string_from_subtree(
                                current.children[1],
                                iteration_probability,
                                iteration_probability_decrease)
                        else:
                            rs = self._random_string_from_subtree(
                                current.children[3],
                                iteration_probability,
                                iteration_probability_decrease)
                    else:
                        # B->(A.A)
                        rs = self._random_string_from_subtree(
                            current.children[1],
                            iteration_probability,
                            iteration_probability_decrease)
                        l1 = self._random_string_from_subtree(
                            current.children[3],
                            iteration_probability,
                            iteration_probability_decrease)
                        rs.extend(l1)
                else:
                    # B->terminal
                    rs = self._random_string_from_subtree(
                        current.children[0],
                        iteration_probability,
                        iteration_probability_decrease)
        return rs

    def save(self, file):
        """Save a copy of the definition of this re in a json file."""
        d = vars(self).copy()
        with open(file+'.json', "w") as f:
            json.dump(d, f)

    def __str__(self):
        """Return a string representation of the re."""
        s = 'alphabet: {}\n'.format(', '.join(sorted(self.alphabet)))
        if self.all_chars:
            s += 'expression: {}\n'.format(tools.Tools.print(self.expression))
        else:
            s += 'expression: {}\n'.format(tools.Tools.print_tuple(self.expression))
        return s
