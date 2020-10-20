#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classes and methods for working with CYK parse table."""

import base.base as base
import grammar.cf.syntax_tree as sy
import parse.base.parser_exceptions as pre


class terminal_production(base.Base):
    """Representation of a terminal production in the CYK table."""

    def __init__(self, left, right):
        """Initialize."""
        self.left = left
        self.right = right

    def __str__(self):
        """Associate a description of the object to its identifier."""
        s = '{}->{}'.format(self.left, self.right)
        return s


class nonterminal_production(base.Base):
    """Representation of a non terminal production in the CYK table."""

    def __init__(self, left, first_table_cell, second_table_cell):
        """Initialize."""
        self.left = left
        self.first_table_cell = first_table_cell
        self.second_table_cell = second_table_cell

    def __str__(self):
        """Associate a description of the object to its identifier."""
        s = '{}->({},{})({},{})'.format(
                                self.left,
                                self.first_table_cell.substring_length,
                                self.first_table_cell.start_index,
                                self.second_table_cell.substring_length,
                                self.second_table_cell.start_index)
        return s


class Table_cell(base.Base):
    """Content of a cell in the CYK table."""

    def __init__(self, substring_length, start_index):
        """Initialize cell row, column, type, and set of CNF productions."""
        self.substring_length = substring_length
        self.start_index = start_index

    def productions(self):
        """Return list of productions in cell."""
        if type(self).__name__ == 'Table_cell_terminal':
            return [self.production]
        elif type(self).__name__ == 'Table_cell_nonterminal':
            return self.productions
        else:
            pass

    def __str__(self):
        """Associate a description of the object to its identifier."""
        s = '({},{}): '.format(self.substring_length, self.start_index)
        s += '{'
        sp = ''
        for production in self.productions:
            sp += str(production)
            sp += ', '
        if len(sp) > 1:
            s += sp[:-2]
        s += '}'
        return s


class Table_cell_terminal(Table_cell):
    """Content of a table cell containing terminal CNF productions."""

    def __init__(self, substring_length, start_index):
        """Initialize cell."""
        super(Table_cell_terminal, self).__init__(substring_length, start_index)
        self.production = None

    def set_terminal_production(self, left, right):
        """Set the terminal production of the cell."""
        self.production = terminal_production(left, right)

    @property
    def productions(self):
        """Return a list containing the single terminal production."""
        return [self.production]

    def cell_visit(self):
        """Return description tuple of the cell."""
        result = ['t']
        production = self.production
        left_side = production.left
        right_side = production.right
        result.append((left_side, right_side))
        return result


class Table_cell_nonterminal(Table_cell):
    """Content of a table cell containing nonterminal CNF productions."""

    def __init__(self, substring_length, start_index):
        """Initialize cell."""
        super(Table_cell_nonterminal, self).__init__(substring_length, start_index)
        self.productions = []

    def add_nonterminal_production(self, left, first_cell, second_cell):
        """Add a non terminal production to the cell."""
        self.productions.append(nonterminal_production(left, first_cell, second_cell))

    def cell_visit(self):
        """Return description tuple of the cell."""
        result = ['nt']
        productions = self.productions
        for production in productions:
            left_side = production.left
            right_side_1 = production.first_table_cell
            right_side_2 = production.second_table_cell
            result.append((left_side, right_side_1, right_side_2))
        return result


class CYK_table:
    """The parse table filled by the CYK algorithm."""

    def __init__(self, length, tokens, grammar):
        """Initialize cell."""
        self.table = [[None for row in range(length - column)]
                      for column in range(length)]
        self.length = length
        self.tokens = tokens
        self.grammar = grammar
        self.list_of_rules = None
        self._syntax_tree = None
        self.filled = False

    def terminal_cell(self, substring_length, start_index, left_part, terminal):
        """Set a terminal table cell at the given location."""
        if self.table[substring_length-1][start_index] is None:
            self.table[substring_length-1][start_index] = \
                Table_cell_terminal(substring_length, start_index)
        self.table[substring_length-1][start_index].set_terminal_production(
                                                        left_part, terminal)

    def nonterminal_cell(self, substring_length, start_index, left_part,
                         first_cell, second_cell):
        """Set a nonterminal table cell at the given location."""
        if self.table[substring_length-1][start_index] is None:
            self.table[substring_length-1][start_index] = \
                Table_cell_nonterminal(substring_length, start_index)
        self.table[substring_length-1][start_index].add_nonterminal_production(
                                            left_part,
                                            first_cell,
                                            second_cell)

    def empty_nonterminal_cell(self, substring_length, start_index):
        """Set an empty nonterminal table cell at the given location."""
        if self.table[substring_length-1][start_index] is None:
            self.table[substring_length-1][start_index] = \
                Table_cell_nonterminal(substring_length, start_index)

    def number_of_productions(self, substring_length, start_index):
        """Return number of productions in the cell at the given location."""
        return len(self.table[substring_length-1][start_index].productions)

    def cell_productions(self, substring_length, start_index):
        """Return list of productions in the cell at the given location."""
        if type(self.table[substring_length-1][start_index]).__name__ \
                == 'Table_cell_terminal':
            return [self.table[substring_length-1][start_index].production]
        elif type(self.table[substring_length-1][start_index]).__name__ \
                == 'Table_cell_nonterminal':
            return self.table[substring_length-1][start_index].productions
        else:
            pass

    def cell(self, substring_length, start_index):
        """Return cell at the given location."""
        return self.table[substring_length-1][start_index]

    @property
    def root(self):
        """Return root cell of the table."""
        return self.table[-1][0]

    @property
    def number_of_trees(self):
        """Return number of syntax trees associated to the parsed string."""
        root_productions = self.cell_productions(self.length, 0)
        string_syntax_trees = []
        for production in root_productions:
            if production.left == tuple(self.grammar.axiom):
                string_syntax_trees.append(production)
        return len(string_syntax_trees)

    @property
    def successful(self):
        """Return true if the string belongs to the language."""
        return self.number_of_trees > 0

    @property
    def ambiguous(self):
        """Return true if there exist more that 1 syntax tree."""
        return self.number_of_trees > 1

    @property
    def syntax_tree(self):
        """Derive/return syntax tree for the string from the parsing table."""

        def nt(current_cell):
            """Derive a node of the syntax tree from a table cell."""
            current_cell_description = current_cell.cell_visit()
            if current_cell_description[0] == 't':
                node = sy.Nonterminal_node(current_cell_description[1][0])
                node1 = sy.Terminal_node(current_cell_description[1][1])
                node.add_child(node1)
                node1.father = node
            else:
                node = sy.Nonterminal_node(current_cell_description[1][0])
                node1 = nt(current_cell_description[1][1])
                node2 = nt(current_cell_description[1][2])
                node.add_child(node1)
                node.add_child(node2)
                node1.father = node
                node2.father = node
            return node

        if not self.filled:
            raise pre.NoParseTable('CYK table not filled')
        if self._syntax_tree is None:
            root_cell = self.root
            root_description = root_cell.cell_visit()
            tree = sy.Syntax_tree(self.grammar)
            if root_description[0] == 't':
                tree.root = sy.Nonterminal_node(root_description[1][0])
                node1 = sy.Terminal_node(root_description[1][1])
                tree.root.add_child(node1)
                node1.father = tree.root
            else:
                tree.root = nt(root_cell)
            self._syntax_tree = tree
        return self._syntax_tree

    @property
    def left_derivation(self):
        """Return leftmost derivation from the parse table."""
        if not self.filled:
            raise pre.NoParseTable('CYK table not filled')
        st = self.syntax_tree
        return st.left_derivation

    @property
    def right_derivation(self):
        """Return rightmost derivation from the parse table."""
        if not self.filled:
            raise pre.NoParseTable('CYK table not filled')
        st = self.syntax_tree
        return st.right_derivation

    def __str__(self):
        """Derive a string representation of the table."""
        s = ''
        for row in self.table[::-1]:
            for cell in row:
                s += '{}'.format(cell)
                s += '\n'
            s += '\n'
        return s

    def __repr__(self):
        """Associate a description of the object to its identifier."""
        s = ''
        for row in self.table[::-1]:
            for cell in row:
                s += '{}'.format(repr(cell))
                s += '\n'
            s += '\n'
        return s
