#!/usr/bin/env python3
"""Code for testing."""

# %cd ..

from tools.tools import Tools
from grammar.regular.regular_grammar import RG
from grammar.cf.cf_grammar import CFG
from grammar.cs.cs_grammar import CSG
from grammar.general.general_grammar import GG
from parse.cyk.cyk_parser import CYK_parser
from parse.rd.recursive_descent import RD_parser
from regexpr.reg_expression import RegEx

# Definizione di grammatica context free in CNF che genera le espressioni regolari sull'alfabeto {a,b,c}

er_terminals = {'(', ')', '+', '*', '.'}
string_alphabet = {'a', 'b', 'c'}
regex = CFG(
    terminals=er_terminals.union(string_alphabet),
    non_terminals={"E", 'A', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z', 'X'},
    axiom="E",
    productions={
        'A': {('a'), ('b'), ('c'), ('A', 'R'), ('Y', 'X'), ('Z', 'X', 'E')},
        'R': {('*')},
        'S': {('(')},
        'T': {(')')},
        'U': {('+')},
        'V': {('.')},
        'W': {('S', 'A')},
        'Y': {('W', 'U')},
        'X': {('A', 'T')},
        'Z': {('W', 'V')},
        "E": {('A',), ()}
    }
)


print(regex)

# Definizione di un parser CYK sulla grammatica precedente

cyk = CYK_parser(regex)

simple_prods = {
                'A': {'b', 'a', 'c', 'AR', 'YX', 'ZX'},
                'R': {'*'},
                'S': {'('},
                'T': {')'},
                'U': {'+'},
                'V': {'.'},
                'W': {'SA'},
                'Y': {'WU'},
                'X': {'AT'},
                'Z': {'WV'},
                }

er_terminals = {'(', ')', '+', '*', '.'}
string_alphabet = {'a', 'b', 'c'}
regex_simple = CFG(
    terminals=er_terminals.union(string_alphabet),
    non_terminals={'A', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z', 'X'},
    axiom='A',
    productions=Tools.simple_productions(simple_prods)
)

Tools.simple_productions(simple_prods)

Tools.simple_sequence('aXbZ')

er_terminals = {'(', ')', '+', '*', '.'}
string_alphabet = {'a', 'b', 'c'}
regex = CFG(
    terminals=er_terminals.union(string_alphabet),
    non_terminals={'A', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z', 'X'},
    axiom='A',
    productions={
                'A': {('a'), ('b'), ('c'), ('A', 'R'), ('Y', 'X'), ('Z', 'X')},
                'R': {('*')},
                'S': {('(')},
                'T': {(')')},
                'U': {('+')},
                'V': {('.')},
                'W': {('S', 'A')},
                'Y': {('W', 'U')},
                'X': {('A', 'T')},
                'Z': {('W', 'V')},
                }
        )

re = RegEx(alphabet={'a', 'b'}, expression=('(', '(', 'a', '.', 'b', ')', '*', ')'))

print(re)

print(re.syntax_tree)

print(re.random_string())

re1 = RegEx(alphabet={'a', 'b'}, expression=(Tools.simple_sequence('(a+b*)*.(a.b)')))
re2 = RegEx(alphabet={'a', 'b'}, expression=(Tools.simple_sequence('(a+b*)*+(a.b)')))
re3 = RegEx(alphabet={'a', 'b'}, expression=(Tools.simple_sequence('(a.b)')))


for i in range(20):
    print(re2.random_string())

terminals = {'(', ')', '+', '*', '.', 'a', 'b', 'c'}
regex1 = CFG(
    terminals=terminals,
    non_terminals={'A'},
    axiom='A',
    productions={
        ('A',): {('a',), ('b',), ('c',), ('(', 'A', '+', 'A', ')'),
                 ('(', 'A', '+', 'A', ')', '*'),
                 ('(', 'A', '.', 'A', ')'),
                 ('(', 'A', '.', 'A', ')', '*'), ('a', '*'), ('b', '*'), ('c', '*')}
                }
        )

alphabet = {'io', 'tu', 'lui'}
regex2 = CFG(
            terminals=alphabet.union({'(', ')', '+', '*', '.'}),
            non_terminals={'S', 'A', 'B'},
            axiom='S',
            productions={
                'S': {'A', ''},
                'A': alphabet.union({('(', 'A', ')'),
                                     ('(', 'A', '+', 'A', ')'),
                                     ('(', 'A', '.', 'A', ')'),
                                     ('B', '*')}),
                'B': alphabet.union({('(', 'A', '.', 'A', ')'),
                                     ('(', 'A', '+', 'A', ')'),
                                     ('(', 'A', ')')}),
                }
            )

rd = RD_parser(regex1)

vars(rd)



