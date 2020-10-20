#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classes and methods for working with syntax trees."""

import base.base as base

import tools.tools as tools


class Tree_node(base.Base):
    """A generic tree node."""

    def __init__(self, symbol):
        """Initialize node."""
        self.symbol = symbol
        self._father = None

    @property
    def father(self):
        """Return the node father."""
        return self._father

    @father.setter
    def father(self, father):
        """Set the node father."""
        self._father = father

    def __str__(self):
        """Print the node content."""
        return ' '+self.symbol


class Terminal_node(Tree_node):
    """A leaf of the syntax tree, containing a terminal symbol."""

    def __init__(self, symbol):
        """Initialize node."""
        super().__init__(symbol)

    def pretty_print(self, il):
        """Pretty print the content of the node."""
        s = '\n'+'\t'*il+self.symbol
        return s

    def __repr__(self):
        """Associate a description of the object to its identifier."""
        return '{}(symbol: "{}")'.format(
                self.__class__.__name__,
                self.symbol
                )


class Nonterminal_node(Tree_node):
    """An internal of the syntax tree, containing a nonterminal symbol."""

    def __init__(self, symbol):
        """Initialize node."""
        super().__init__(symbol)
        self.children = []

    def add_child(self, node):
        """Add a children to the node."""
        self.children.append(node)

    def pretty_print(self, il):
        """Pretty print the content of subtree rooted at the given node."""
        s = '\n'+'\t'*il+self.symbol+'->'
        s += self.children[0].pretty_print(il+1)
        for child in self.children[1:]:
            s += child.pretty_print(il+1)
        return s

    def __repr__(self):
        """Associate a description of the object to its identifier."""
        return '{}(symbol: "{}")'.format(
                self.__class__.__name__,
                self.symbol
                )


class Syntax_tree(base.Base):
    """
    A syntax tree.

    Internal nodes, corresponding to nonterminals, are instances of Nonterminal_node
    Leaves, corresponding to terminals, are instances of Terminal_node
    """

    def __init__(self, grammar):
        """Initialize tree."""
        self.grammar = grammar
        self.root = None

    @classmethod
    def null_st(cls, grammar):
        """Return syntax tree of the null string."""
        tree = cls(grammar)
        tree.root = Nonterminal_node(grammar.axiom)
        leaf = Terminal_node('_')
        tree.root.add_child(leaf)
        leaf.father = tree.root
        return tree

    @property
    def left_derivation(self):
        """Derive a leftmost derivation from the syntax tree."""
        from grammar.base.derivation import Left_derivation, Step

        def ld_subtree(root, d, nonterminals):
            if isinstance(root, Terminal_node):
                return d
            else:
                if len(d.steps) == 0:
                    right = []
                    for c in root.children:
                        right.append(c.symbol)
                    left = root.symbol
                    step = Step(left=left,
                                right=tuple(right),
                                phrase=left,
                                next_phrase=tuple(right),
                                start_index=0,
                                grammar=self.grammar)
                    d.append_step(step)
                else:
                    right = []
                    for c in root.children:
                        right.append(c.symbol)
                    left = root.symbol
                    phrase = d.steps[-1].next_phrase
                    ind = tools.Tools.first_nt(phrase, nonterminals)
                    next_phrase = tools.Tools.insert_in_tuple(phrase, ind, right)
                    step = Step(left=left,
                                right=right,
                                phrase=phrase,
                                next_phrase=next_phrase,
                                start_index=ind,
                                grammar=self.grammar)
                    d.append_step(step)
                for child in root.children:
                    d = ld_subtree(child, d, nonterminals)
                return d

        d = Left_derivation.empty(self.grammar)
        return ld_subtree(self.root, d, self.grammar.non_terminals)

    @property
    def right_derivation(self):
        """Derive a rightmost derivation from the syntax tree."""
        from grammar.base.derivation import Right_derivation, Step

        def rd_subtree(root, d, nonterminals):
            if isinstance(root, Terminal_node):
                return d
            else:
                if len(d.steps) == 0:
                    right = []
                    for c in root.children:
                        right.append(c.symbol)
                    left = root.symbol
                    step = Step(left=left,
                                right=tuple(right),
                                phrase=left,
                                next_phrase=tuple(right),
                                start_index=0,
                                grammar=self.grammar)
                    d.append_step(step)
                else:
                    right = []
                    for c in root.children:
                        right.append(c.symbol)
                    left = root.symbol
                    phrase = d.steps[-1].next_phrase
                    ind = tools.Tools.last_nt(phrase, nonterminals)
                    next_phrase = tools.Tools.insert_in_tuple(phrase, ind, right)
                    step = Step(left=left,
                                right=right,
                                phrase=phrase,
                                next_phrase=next_phrase,
                                start_index=ind,
                                grammar=self.grammar)
                    d.append_step(step)
                for child in root.children[::-1]:
                    d = rd_subtree(child, d, nonterminals)
                return d

        d = Right_derivation.empty(self.grammar)
        return rd_subtree(self.root, d, self.grammar.non_terminals)

    def __str__(self):
        """Pretty print the tree content."""
        s = ''
        il = 0
        if self.root is not None:
            s += self.root.pretty_print(il)
        s += ''
        return s

    def __repr__(self):
        """Associate a description of the object to its identifier."""
        def repr_node(node):
            s = '{}: {}'.format(node.__class__.__name__, node.symbol)
            if node.__class__.__name__ == 'Nonterminal_node':
                s += '\n ['
                for c in node.children:
                    s += repr_node(c)
                s += ']\n'
            return s
        return repr_node(self.root)
