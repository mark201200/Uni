#!/usr/bin/env python3
"""Code for testing."""

from tools.tools import Tools
from grammar.regular.regular_grammar import RG
from grammar.cf.cf_grammar import CFG
from grammar.cs.cs_grammar import CSG
from grammar.general.general_grammar import GG
from parse.cyk.cyk_parser import CYK_parser
from parse.rd.recursive_descent import RD_parser
from regexpr.reg_expression import RegEx

# Regular grammar
rg = RG(
    terminals={'a', 'b', 'c'},
    non_terminals={'S', 'A', 'B'},
    axiom='S',
    productions={
        ('S',): {('a', 'S'), ('a', 'A'), ('b', 'A'), ()},
        ('A',): {('b', 'A'), ('b'), ('b', 'B')},
        ('B',): {('c', 'A'), 'c'}
    }
)

d = rg.random_derivation()


# CF grammar
cfg = CFG(
    terminals={'a', 'b', 'c'},
    non_terminals={'S', 'A', 'B', 'C'},
    axiom='S',
    productions={
        ('S',): {('a', 'S', 'a', 'S'), ('a', 'A'), ('A', 'B')},
        ('A',): {('b', 'b', 'A', 'B'), ('b', 'b'), ('b', 'A', 'a', 'B'), ('B',)},
        ('B',): {('c', 'A', 'A'), ('c', 'c'), ('C',), ()},
        ('C',): {('c', 'C'), ('c',), ('S',)}
    }
)


cfg0 = CFG(
    terminals={'a'},
    non_terminals={'S', 'A', 'B'},
    axiom='S',
    productions={
        ('S',): {('A', 'B'), ('a',)},
        ('A',): {('a',)}
    }
)

cfg1 = cfg0.remove_nulls()
cfg2 = cfg0.remove_unit_prods()
cfg3 = cfg0.reduce()

csg = CSG(
    terminals={'io', 'tu', 'lui'},
    non_terminals={'A', 'AX', 'XX'},
    axiom='A',
    productions={
        ('A',): {('io',), ('tu',), ('lui',), ('AX', 'tu'), ('XX', 'A', 'io')},
        ('AX', 'tu', 'io'): {('XX', 'A', 'io'), ('AX', 'io', 'tu')},
        ('A', 'io'): {('XX', 'A', 'io'), ('AX', 'io', 'tu'), ('tu', 'tu')},
        ('XX', 'A'): {('A', 'XX'), ('A', 'io'), ('tu', 'tu')}
        }
    )


csg0 = CSG(
    terminals={'a', 'b', 'c'},
    non_terminals={'X', 'Y', 'Z'},
    axiom='X',
    productions={
        ('X',): {('a',), ('b',), ('c',), ('Y', 'b'), ('Z', 'X', 'a')},
        ('Y', 'b', 'a'): {('Z', 'X', 'a'), ('Y', 'a', 'b')},
        ('X', 'a'): {('Z', 'X', 'a'), ('Y', 'a', 'b'), ('b', 'b')},
        ('Z', 'X'): {('X', 'Z'), ('X', 'a'), ('b', 'b')}
        }
    )


d = csg0.random_derivation()


gg0 = GG(
    terminals={'0', '1'},
    non_terminals={'A', 'B', 'C'},
    axiom='A',
    productions={
        Tools.simple_sequence('A'): {Tools.simple_sequence('0'),
                                     Tools.simple_sequence('01'),
                                     Tools.simple_sequence('B1'),
                                     Tools.simple_sequence('BA0')},
        Tools.simple_sequence('BA'): {Tools.simple_sequence(''),
                                      Tools.simple_sequence('AB'),
                                      Tools.simple_sequence('01')},
        Tools.simple_sequence('A01'): {Tools.simple_sequence('0'),
                                       Tools.simple_sequence('A0'),
                                       Tools.simple_sequence('C'),
                                       Tools.simple_sequence('001')},
        Tools.simple_sequence('AA'): {Tools.simple_sequence('0A0'),
                                      Tools.simple_sequence('0B1'),
                                      Tools.simple_sequence('')}
        }
    )


cfg1 = CFG(
    terminals={'a', 'b', 'c'},
    non_terminals={'A', 'S'},
    axiom='S',
    productions={
        Tools.simple_sequence('S'): {Tools.simple_sequence('aSc'),
                                     Tools.simple_sequence('A')},
        Tools.simple_sequence('A'): {Tools.simple_sequence(''),
                                      Tools.simple_sequence('bAc')}
        }
    )


csg1 = CSG(
    terminals={'a'},
    non_terminals={'I', 'S', 'F', 'M'},
    axiom='S',
    productions={
        Tools.simple_sequence('S'): {Tools.simple_sequence('a'),
                                     Tools.simple_sequence('aa'),
                                     Tools.simple_sequence('IaF')},
        Tools.simple_sequence('aF'): {Tools.simple_sequence('Maa'),
                                      Tools.simple_sequence('MaaF')},
        Tools.simple_sequence('aM'): {Tools.simple_sequence('Maa')},
        Tools.simple_sequence('IM'): {Tools.simple_sequence('Ia'),
                                      Tools.simple_sequence('aa')}
        }
    )

gg1 = GG(
    terminals={'a', 'b'},
    non_terminals={'S', 'A'},
    axiom='S',
    productions={
        Tools.simple_sequence('S'): {Tools.simple_sequence('aAb')},
        Tools.simple_sequence('aA'): {Tools.simple_sequence('aaAb')},
        Tools.simple_sequence('A'): {Tools.simple_sequence('')}
        }
    )

csg2 = CSG(
    terminals={'a', 'b'},
    non_terminals={'S', 'A'},
    axiom='S',
    productions={
        Tools.simple_sequence('S'): {Tools.simple_sequence('aSa'),
                                     Tools.simple_sequence('aAb'),
                                     Tools.simple_sequence('aAa')},
        Tools.simple_sequence('aA'): {Tools.simple_sequence('aa')},
        Tools.simple_sequence('Ab'): {Tools.simple_sequence('aab')}
        }
    )

csg3 = CSG(
    terminals={'a', 'b'},
    non_terminals={'S', 'B'},
    axiom='S',
    productions={
        Tools.simple_sequence('S'): {Tools.simple_sequence('aBS'),
                                     Tools.simple_sequence('ab')},
        Tools.simple_sequence('Ba'): {Tools.simple_sequence('aB')},
        Tools.simple_sequence('Bb'): {Tools.simple_sequence('bb')}
        }
    )

