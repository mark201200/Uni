#!/usr/bin/env python3
"""Code for testing."""

# %cd ..

from tools.tools import Tools
from grammar.regular.regular_grammar import RG
from grammar.cf.cf_grammar import CFG
from grammar.cs.cs_grammar import CSG
from grammar.general.general_grammar import GG

# Descrizione di una grammatica:
# - tipo di grammatica (GG generale, CSG context-sensitive, CFG context-free, RG regolare sinistra, RRG regolare destra)
# - insieme dei terminali: insieme di stringhe 
# - insieme dei nonterminali: insieme di stringhe disgiunto
# - assioma: un nonterminale
# - produzioni: dizionario con chiavi ed elementi rappresentati da tuple di terminali e non terminali, inclusa la tupla () relativa alla stringa nulla

# Regular grammar
rg = RG(
    terminals={'a', 'b', 'c'},
    non_terminals={'S', 'A', 'B'},
    axiom='S',
    productions={
        ('S',): {('a', 'S'), ('a', 'A'), ('b', 'A'), ()},
        ('A',): {('b', 'A'), ('b',), ('b', 'B')},
        ('B',): {('c', 'A'), ('c',)}
    }
)

# Stampa della struttura della grammatica

print(rg)

# Generazione di una derivazione casuale

d = rg.random_derivation(n=3)


# Stampa della derivazione: nella colonna a sx la sequenza di forme di frasi; nella colonna a dx la sequenza di produzioni applicate

print(d)

# CF grammar
cfg = GG(
    terminals={'a', 'b', 'c'},
    non_terminals={'S', 'A', 'B', 'C'},
    axiom='S',
    productions={
        ('S', 'A'): {('a', 'S', 'a', 'S'), ('a', 'A'), ('A', 'B')},
        ('A',): {('b', 'b', 'A', 'B'), ('b', 'b'), ('b', 'A', 'a', 'B'), ('B',)},
        ('B',): {('c', 'A', 'A'), ('c', 'c'), ('C',), ()},
        ('C',): {('c', 'C'), ('c',), ('S',)}
    }
)


print(cfg)

cfg0 = CFG(
    terminals={'a'},
    non_terminals={'S', 'A', 'B'},
    axiom='S',
    productions={
        ('S',): {('A', 'B'), ('a',)},
        ('A',): {('a',)}
    }
)

# +
# cfg1 = cfg0.remove_nulls()
# cfg2 = cfg0.remove_unit_prods()
# cfg3 = cfg0.reduce()
# -

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


print(csg)

d = csg.random_derivation()

print(d)

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


print(csg0)

d = csg0.random_derivation()

# Il generatore g consente, attraverso l'iterazione dell'istruzione next(g), di ottenere la sequenza dei passi di derivazione

g = d.generator

# Stampa del prossimo passo di derivazione: a sinistra la produzione applicata, a destra la derivazione diretta conseguente

print(next(g))

# La funzione Tools.simple_productions() applicata all'insieme dell produzioni permette di specificarle, nel caso in cui terminali e nonterminali siano singoli caratteri, utilizzando stringhe al posto di tuple

gg0 = GG(
    terminals={'0', '1'},
    non_terminals={'A', 'B', 'C'},
    axiom='A',
    productions=Tools.simple_productions({
        'A': {'0', '01', 'B1', 'BA0'},
        'BA': {'', 'AB', '01'},
        'A01': {'0', 'A0', 'C', '001'},
        'AA': {'0A0', '0B1', ''}
        })
    )

print(gg0)

# La funzione Tools.simple_sequence() permette di definire una sequenza di simboli terminali o nonterminali mediante una stringa, nel caso in cui siano singoli caratteri

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


print(cfg1)

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

print(csg1)

# Il parametro n indica la lunghezza massima della derivazione riportata (default n=100)

d = csg1.random_derivation(n=20)

print(d)

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

cfg4 = CFG(
    terminals={'i', '+', '*', '(', ')'},
    non_terminals={'E', 'T', 'F'},
    axiom='E',
    productions=Tools.simple_productions({
        'E': {'E+T', 'T'},
        'T': {'T*F', 'F'},
        'F': {'i', '(E)'}
        })
    )

print(cfg4)

cfg5 = CFG(
    terminals={'a', 'b'},
    non_terminals={'S'},
    axiom='S',
    productions=Tools.simple_productions({
        'S': {'aSb', 'ab'}
        })
    )

cfg6 = CFG(
    terminals={'(', ')'},
    non_terminals={'S'},
    axiom='S',
    productions=Tools.simple_productions({
        'S': {'()', 'SS', '(S)'}
        })
    )

cfg7 = CFG(
    terminals={'a', 'b'},
    non_terminals={'S', 'U'},
    axiom='S',
    productions=Tools.simple_productions({
        'S': {'Ub'},
        'U': {'ab', 'S'}
        })
    )


cfg8 = CFG(
    terminals={'a', 'b'},
    non_terminals={'S', 'U'},
    axiom='S',
    productions=Tools.simple_productions({
        'S': {'Ub', ''},
        'U': {'ab', 'S'}
        })
    )

gg2 = GG(
    terminals={'a', 'b', 'c'},
    non_terminals={'S', 'B', 'C', 'F', 'G'},
    axiom='S',
    productions={
        Tools.simple_sequence('S'): {Tools.simple_sequence('aSBC')},
        Tools.simple_sequence('CB'): {Tools.simple_sequence('BC')},
        Tools.simple_sequence('SB'): {Tools.simple_sequence('bF')},
        Tools.simple_sequence('FB'): {Tools.simple_sequence('bF')},
        Tools.simple_sequence('FC'): {Tools.simple_sequence('cG')},
        Tools.simple_sequence('GC'): {Tools.simple_sequence('cG')},
        Tools.simple_sequence('G'): {Tools.simple_sequence('')}
        }
    )


print(gg2)

# Salva definizione di una grammatica in un file .yaml nella cartella 'store'

gg2.save('gg2')

# File yaml derivato

# %less store/gg2.yaml

# La funzione Tools.load carica la definizione di una grammatica dal file specificato, nella cartella 'store'

gg20 = Tools.load('gg2')

print(gg20)


