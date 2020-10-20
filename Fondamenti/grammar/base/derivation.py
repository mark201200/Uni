#!/usr/bin/env python3
"""Derivation."""

import random
import itertools

import base.base as base
import tools.tools as tools
from grammar.cf.syntax_tree import Syntax_tree, Terminal_node, Nonterminal_node


class Step(base.Base):
    """
    A representation of a derivation step.

    Encapsulates:
        - the left part of the production applied (as a tuple of strings)
        - the right part of the production applied (as a tuple of strings)
        - the phrase onto which the production is applied (as a tuple of strings)
        - the initial index of the subphrase corresponding to the left part of
            the derivation applied
        - the phrase obtained after the production is applied (as a tuple of strings)
        - the associated grammar
    """

    def __init__(self, *, left, right, phrase, next_phrase,
                 start_index, grammar):
        """Initialize derivation step."""
        self.left = left
        self.right = right
        self.phrase = phrase
        self.start_index = start_index
        self.next_phrase = next_phrase
        self.grammar = grammar

    @classmethod
    def init(cls, *, left, right):
        """Initialize a step from left and tight parts of production."""
        return cls(left=left,
                   right=right,
                   phrase=None,
                   next_phrase=None,
                   start_index=None,
                   grammar=None)

    @staticmethod
    def _left_part_occurrences(phrase, grammar):
        """Return all occurrences in phrase of production left parts."""
        left_part_indices = []
        if type(grammar).__name__ in {'RG', 'CFG'}:
            for i in range(len(phrase)):
                if phrase[i] in grammar.non_terminals:
                    left_part_indices.append((i, 1))
            if len(left_part_indices) == 0:
                return None
        else:
            for i in range(len(phrase)):
                for lp in grammar.productions.keys():
                    if phrase[i:i+len(lp)] == lp:
                        left_part_indices.append((i, len(lp)))
        return left_part_indices

    def __repr__(self):
        """Derive a string representation of the derivation step."""
        return '{} (({} {}) ({} {}))'.format(
            self.__class__.__name__,
            self.left,
            self.right,
            self.phrase,
            self.next_phrase)

    def __str__(self):
        """Derive a string representation of the derivation step."""
        if self.grammar.all_chars:
            s = '{} -> {}\t\t\t{} => {}'.format(
                tools.Tools.print(self.left), tools.Tools.print(self.right),
                tools.Tools.print(self.phrase), tools.Tools.print(self.next_phrase)
                )
        else:
            s = '{} -> {}\t\t\t{} => {}'.format(
                                                tools.Tools.print_tuple(self.left),
                                                tools.Tools.print_tuple(self.right),
                                                tools.Tools.print_tuple(self.phrase),
                                                tools.Tools.print_tuple(self.next_phrase)
                                                )
        return s


class Derivation(base.Base):
    """
    A representation of a derivation as a sequence of derivation steps.

    Encapsulates:
        - a list of Steps
        - the associated grammar
    """

    def __init__(self, sequence_of_steps, grammar):
        """Initialize derivation."""
        self.steps = sequence_of_steps
        self.grammar = grammar

    @classmethod
    def empty(cls, grammar):
        """Create empty derivation."""
        return cls([], grammar)

    @property
    def generator(self):
        """Return a generator to loop over the sequence of steps."""
        return (step for step in self.steps)

    def _select_choices(self, left_part_indices):
        """Select the set of possible next steps."""
        return left_part_indices

    def next_step(self):
        """Return a random step from current phrase."""
        grammar = self.grammar
        if self.steps:
            phrase_tokens = self.steps[-1].next_phrase
        else:
            phrase_tokens = tuple(grammar.axiom)
        left_part_indices = Step._left_part_occurrences(phrase_tokens, grammar)
        if not left_part_indices:
            return None
        left_choices = self._select_choices(left_part_indices)
        start_index, length = random.choice(left_choices)
        lpart_tokens = phrase_tokens[start_index:start_index+length]
        choices = self.grammar.get_right_parts(lpart_tokens)
        if choices is None or len(choices) == 0:
            return None
        rpart_tokens = random.choice(list(choices))
        sub_phrases = [phrase_tokens[:start_index],
                       rpart_tokens,
                       phrase_tokens[start_index+length:]]
        next_phrase_tokens = tuple(itertools.chain.from_iterable(sub_phrases))
        return Step(left=lpart_tokens,
                    right=rpart_tokens,
                    phrase=phrase_tokens,
                    start_index=start_index,
                    next_phrase=next_phrase_tokens,
                    grammar=grammar)

    def append_step(self, step):
        """
        Extend this derivation by adding a new step at its end.

        It is assumed that the step is applied on the subsequence of the right
        part of the last step in the derivation, starting from symbol at
        start_index
        """
        self.steps.append(step)

    def prepend_step(self, step):
        """
        Extend this derivation by adding a new step at its start.

        It is assumed that the first step in the rest of the derivation
        is applied on the subsequence of the right part of step starting from
        symbol at start_index
        """
        self.steps.insert(0, step)

    def _syntax_tree(self, f):
        """Derive/return syntax tree for the string from the derivation."""
        st = Syntax_tree(self.grammar)
        st.root = Nonterminal_node(self.grammar.axiom)
        leaves = [st.root]
        for step in self.generator:
            ind = f(step.phrase, self.grammar.non_terminals)
            father = leaves[ind]
            new_leaves = []
            new_leaves.extend(leaves[:ind])
            if len(step.right) == 0:
                l_symbols = tuple()
            else:
                l_symbols = tuple(step.right)
            for symbol in l_symbols:
                if symbol in self.grammar.terminals.union({''}):
                    node = Terminal_node(symbol)
                else:
                    node = Nonterminal_node(symbol)
                node.father = father
                father.add_child(node)
                new_leaves.append(node)
            new_leaves.extend(leaves[ind+1:])
            leaves = new_leaves
        return st

    def __repr__(self):
        """Derive a string representation of the derivation."""
        return '{} ({})'.format(self.__class__.__name__, self.steps)

    def __str__(self):
        """Pretty print the derivation."""
        from tabulate import tabulate
        lstlst = []
        if self.grammar.all_chars:
            if self.steps:
                for step in self.steps:
                    lst = [tools.Tools.print(step.phrase),
                           tools.Tools.print(step.left)+' -> ' +
                           tools.Tools.print(step.right)]
                    lstlst.append(lst)
                lstlst.append([tools.Tools.print(self.steps[-1].next_phrase), ''])
            else:
                lstlst.append([tools.Tools.print(self.grammar.axiom), ''])
        else:
            if self.steps:
                for step in self.steps:
                    lst = [tools.Tools.print_tuple(step.phrase),
                           tools.Tools.print_tuple(step.left)+' -> ' +
                           tools.Tools.print_tuple(step.right)]
                    lstlst.append(lst)
                lstlst.append([tools.Tools.print_tuple(self.steps[-1].next_phrase), ''])
            else:
                lstlst.append([tools.Tools.print_tuple(self.grammar.axiom), ''])
        return tabulate(lstlst, tablefmt='plain')


class Left_derivation(Derivation):
    """A leftmost derivation."""

    def __init__(self, sequence_of_steps, grammar):
        """Initialize derivation."""
        super().__init__(sequence_of_steps, grammar)

    @classmethod
    def empty(cls, grammar):
        """Create empty left derivation."""
        return cls([], grammar)

    @property
    def syntax_tree(self):
        """Derive/return syntax tree for the string from the derivation."""
        return super()._syntax_tree(tools.Tools.first_nt)

    def _select_choices(self, left_part_indices):
        """Select the set of possible next steps."""
        start_index = min([x[0] for x in left_part_indices])
        left_choices = [x for x in left_part_indices if x[0] == start_index]
        return left_choices


class Right_derivation(Derivation):
    """A right derivation."""

    def __init__(self, sequence_of_steps, grammar):
        """Initialize derivation."""
        super().__init__(sequence_of_steps, grammar)

    @classmethod
    def empty(cls, grammar):
        """Create empty left derivation."""
        return cls([], grammar)

    @property
    def syntax_tree(self):
        """Derive/return syntax tree for the string from the derivation."""
        return super()._syntax_tree(tools.Tools.last_nt)

    def _select_choices(self, left_part_indices):
        """Select the set of possible next steps."""
        start_index = max([x[0] for x in left_part_indices])
        left_choices = [x for x in left_part_indices if x[0] == start_index]
        return left_choices
