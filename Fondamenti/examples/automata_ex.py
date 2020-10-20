#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Code for testing automata."""

# %cd ..

from tools.tools import Tools
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.fa.dfa_configuration import DFAConfiguration
from automata.fa.nfa_configuration import NFAConfiguration
from automata.pda.dpda import DPDA
from automata.pda.npda import NPDA
from automata.pda.stack import PDAStack
from automata.pda.state_stack_pair import StateStackPair
from automata.pda.dpda_configuration import DPDAConfiguration
from automata.pda.npda_configuration import NPDAConfiguration
from automata.tm.dtm import DTM
from automata.tm.ntm import NTM
from automata.tm.tape import TMTape
from automata.tm.state_tape_pair import StateTapePair
from automata.tm.dtm_configuration import DTMConfiguration
from automata.tm.ntm_configuration import NTMConfiguration


# Descrizione di un automa a stati finiti deterministico:
# - tipo di automa: DFA
# - insieme degli stati: insieme di stringhe 
# - alfabeto di input: insieme di stringhe
# - stato iniziale: un simbolo dell'alfabeto
# - stati finali: un sottoinsieme dell'insieme degli stati
# - funzione di transizione: dizionario con 
#     - stati come chiavi 
#     - elementi rappresentati da dizionari con chiavi = simboli dell'alfabeto ed elementi = stati

dfa = DFA(
    states={'q0', 'q1'},
    input_symbols={'id', 'expr'},
    delta={
        'q0': {'id': 'q0', 'expr': 'q1'},
        'q1': {'id': 'q0', 'expr': 'q0'}
    },
    initial_state='q0',
    final_states={'q1'}
)

dfa1 = DFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4'},
    input_symbols={'0', '1'},
    delta={
        'q0': {'0': 'q3', '1': 'q4'},
        'q1': {'0': 'q3', '1': 'q0'},
        'q2': {'0': 'q2', '1': 'q1'},
        'q3': {'0': 'q0'},
        'q4': {'0': 'q0'}
    },
    initial_state='q0',
    final_states={'q1'}
)

dfa2 = DFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
    input_symbols={'0', '1'},
    delta={
        'q0': {'0': 'q2', '1': 'q4'},
        'q1': {'0': 'q3', '1': 'q0'},
        'q2': {'0': 'q2', '1': 'q1'},
        'q3': {'0': 'q0'},
        'q4': {'0': 'q0'},
        'q5': {'0': 'q1'}
    },
    initial_state='q0',
    final_states={'q5'}
)

# Restituzione della computazione effettuata dall'automa sull'input specificato come tupla di simboli dell'alfabeto. Le righe rappresentano le configurazione attraversate: a sx lo stato, a dx la stringa da leggere. In fondo, esito della computazione.

dfa.report_computation(('expr', 'expr', 'id'))

# La funzione Tools.tokens() permette di specificare una tupla di simboli come stringa composta dalla concatenazione dei simboli stessi, separati dal simbolo specificato come separator

dfa.report_computation(Tools.tokens('expr:expr:id', separator=':'))

# Non specificare un valore per separator in Tools.tokens() corrisponde ad assumere nessun separatore, e quindi che i simboli siano singoli caratteri

dfa2.report_computation(Tools.tokens('0010'))

# Descrizione di un automa a stati finiti nondeterministico:
# - tipo di automa: NFA
# - insieme degli stati: insieme di stringhe 
# - alfabeto di input: insieme di stringhe
# - stato iniziale: un simbolo dell'alfabeto
# - stati finali: un sottoinsieme dell'insieme degli stati
# - funzione di transizione: dizionario con 
#     - stati come chiavi 
#     - elementi rappresentati da dizionari con chiavi = simboli dell'alfabeto (o la stringa vuota '') ed elementi = insiemi di stati

nfa = NFA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'digit', 'operator'},
    delta={
        'q0': {'digit': {'q0', 'q1'}, 'operator': {'q0'}, '': {'q1'}},
        'q1': {'digit': {'q2'}},
        'q2': {'digit': {'q3'}}
    },
    initial_state='q0',
    final_states={'q3'}
)


nfa1 = NFA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'0', '1'},
    delta={
        'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
        'q1': {'0': {'q2'}},
        'q2': {'0': {'q3'}}
    },
    initial_state='q0',
    final_states={'q3'}
)


# Configurazione di un DFA: stato attuale, lista di simboli da leggere, fornita come tupla. In aggiunta, riferimento all'automa relativo.

dfac = DFAConfiguration(state='q0', list_of_tokens=('id', 'expr'), automaton=dfa)

dfac1 = DFAConfiguration(state='q0', list_of_tokens=('id'), automaton=dfa)

# Lista dei simboli fornita come stringa, nel caso in cui i simboli dell'alfabeto siano caratteri

dfac0 = DFAConfiguration.init(state='q0', input_str='0110', automaton=dfa1)

dfac00 = DFAConfiguration(state='q0', list_of_tokens=(), automaton=dfa)


# Configurazione di un NFA: insieme degli stati attuale, lista di simboli da leggere, fornita come tupla. In aggiunta, riferimento all'automa relativo.

nfac = NFAConfiguration(states={'q0'},
                        list_of_tokens=('digit', 'operator', 'operator'),
                        automaton=nfa)

nfac1 = NFAConfiguration(states={'q0'}, list_of_tokens=('0', '0', '1'), automaton=nfa1)

# Lista dei simboli fornita come stringa, nel caso in cui i simboli dell'alfabeto siano caratteri

nfac2 = NFAConfiguration.init(states={'q0'}, input_str='111001', automaton=nfa1)

nfac0 = NFAConfiguration(states={'q0'}, list_of_tokens=(), automaton=nfa)

# Restituzione della computazione effettuata dall'automa sull'input specificato. Le righe rappresentano le configurazione attraversate: a dx la sequenza dei simboli da leggere, a sx l'insieme degli stati. In fondo, esito della computazione.

nfa.report_computation(('operator', 'operator', 'digit'))


nfa1.report_computation(Tools.tokens('0100'))

# Restituzione di una sequenza (casuale) di configurazioni deterministiche, derivate dalla computazione nondeterministica eseguita dal NFA sull'input dato.

nfa.report_random_deterministic_path(Tools.tokens('operator:operator:digit', separator=':'))

# Descrizione di un automa a stati a pila deterministico:
# - tipo di automa: DPDA
# - insieme degli stati: insieme di stringhe 
# - alfabeto di input: insieme di stringhe
# - alfabeto di pila: insieme di stringhe
# - stato iniziale: un simbolo dell'alfabeto
# - simbolo inziale nella pila: un simbolo dell'alfabeto di pila
# - stati finali: un sottoinsieme dell'insieme degli stati
# - condizione di accettazione: 'F' (stato finale) o 'E' (pila vuota)
# - funzione di transizione: dizionario con 
#     - stati come chiavi 
#     - elementi rappresentati da dizionari con 
#         - simboli dell'alfabeto come chiavi
#         - elementi rappresentati da dizionari con
#             - simboli di pila come chiavi
#             - elementi rappresentati da coppie (tuple) con:
#                 - stato come prima componente
#                 - sequenza di simboli di pila come tupla

dpda = DPDA(
    states={'q0', 'q1'},
    input_symbols={'id1', 'id2', 'id3'},
    stack_symbols={'SYM1', 'SYM2', 'SYM3'},
    delta={
        'q0': {
                'id1': {'SYM1': ('q0', Tools.tokens('SYM1:SYM1', separator=':')),
                        'SYM2': ('q0', Tools.tokens('SYM2:SYM1', separator=':')),
                        'SYM3': ('q0', ('SYM1',))
                        },
                'id2': {'SYM1': ('q0', Tools.tokens('SYM1:SYM2', separator=':')),
                        'SYM3': ('q0', ('SYM1',))
                        },
                'id3': {'SYM1': ('q1',  ('SYM1',)),
                        'SYM2': ('q1', ('SYM1',)),
                        'SYM3': ('q1', ())
                        }
              },
        'q1': {'id1': {'SYM1': ('q1', ())},
               'id2': {'SYM3': ('q1', ())}}
        },
    initial_state='q0',
    initial_stack_symbol='SYM3',
    final_states={},
    acceptance_mode='E'
)


dpda1 = DPDA(
    states={'q0', 'q1'},
    input_symbols={'a', 'b', 'c'},
    stack_symbols={'X', 'Y', 'Z'},
    delta={
        'q0': {
                'a': {'X': ('q0', Tools.tokens('X:X', separator=':')),
                      'Y': ('q0', Tools.tokens('Y:Y', separator=':')),
                      'Z': ('q0', ('X',))
                      },
                'b': {'X': ('q0', Tools.tokens('X:Y', separator=':')),
                      'Z': ('q0', ('X',))
                      },
                'c': {'X': ('q1',  ('X',)),
                      'Y': ('q1', ('Y',)),
                      'Z': ('q1', ())
                      }
              },
        'q1': {'a': {'X': ('q1', ())},
               'b': {'Y': ('q1', ())}}
        },
    initial_state='q0',
    initial_stack_symbol='X',
    final_states={},
    acceptance_mode='E'
)

# Descrizione di un automa a stati a pila nondeterministico:
# - tipo di automa: NPDA
# - insieme degli stati: insieme di stringhe 
# - alfabeto di input: insieme di stringhe
# - alfabeto di pila: insieme di stringhe
# - stato iniziale: un simbolo dell'alfabeto
# - simbolo inziale nella pila: un simbolo dell'alfabeto di pila
# - stati finali: un sottoinsieme dell'insieme degli stati
# - condizione di accettazione: 'F' (stato finale) o 'E' (pila vuota)
# - funzione di transizione: dizionario con 
#     - stati come chiavi 
#     - elementi rappresentati da dizionari con 
#         - simboli dell'alfabeto come chiavi
#         - elementi rappresentati da dizionari con
#             - simboli di pila (o la stringa vuota '') come chiavi
#             - elementi rappresentati da insiemi di coppie (tuple) con:
#                 - stato come prima componente
#                 - sequenza di simboli di pila come tupla

npda1 = NPDA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'aa', 'b'},
    stack_symbols={'A', 'BB', '#'},
    delta={
        'q0': {
            '': {
                '#': {('q0', ())}
                },
            'aa': {
                '#': {('q0', ('A',))},
                'A': {
                        ('q0', ('A', 'A')),
                        ('q1', ()),
                     },
                'BB': {('q0', ('BB', 'A'))}
                 },
            'b': {
                '#': {('q0', ('BB',))},
                'A': {('q0', ('A', 'BB'))},
                'BB': {
                       ('q0', ('BB', 'BB')),
                       ('q1', ()),
                     }
                 }
        },
        'q1': {
            '': {'#': {('q2', ())}},
            'aa': {'A': {('q1', ())}},
            'b': {'BB': {('q1', ())}}
        }
    },
    initial_state='q0',
    initial_stack_symbol='#',
    final_states={'q2'},
    acceptance_mode='F'
)

# Restituzione della computazione effettuata dal DPDA sull'input specificato. Le righe rappresentano le configurazione attraversate: a dx l'insieme di simboli da leggere, a sx le coppie, comprendenti stato e contenuto della pila attuali. In fondo, esito della computazione.

dpda.report_computation(Tools.tokens('id1:id1:id2', separator=':'))

# Definizione del contenuto di una pila, come tupla di simboli

stack00 = PDAStack(list_of_stack_items=('AS'))
stack001 = PDAStack(list_of_stack_items=(('AS', 'V')))
stack000 = PDAStack(list_of_stack_items=())

print(stack001)

# Definizione del contenuto di una pila, come stringa di caratteri

stack0000 = PDAStack.init(stack_str='')
stack01 = PDAStack.init(stack_str='ab')

print(stack01)

# Definizione del contenuto di una pila, come lista di simboli

stack03 = PDAStack.new(stack_items=[])

print(stack03)

# Definizione del contenuto iniziale di una pila, contenente il singolo carattere specificato

stack02 = PDAStack.initial_stack(token='N')

print(stack02)

# Definizione di coppie stato-pila

# Specificando una pila già definita

stack4 = StateStackPair(state='q1', stack=stack00)
print(stack4)

# Inizializzando lo stack

stack0 = StateStackPair(state='q0', stack=PDAStack.init(stack_str=''))
print(stack0)

# Specificando il contenuto dello stack come stringa

stack1 = StateStackPair.init(state='q1', stack_str='#BA')
print(stack1)

# Specificando il contenuto dello stack come tupla

stack2 = StateStackPair.new(state='q1', list_of_stack_items=('#', 'B', 'A'))
print(stack2)

stack21 = StateStackPair.new(state='q1', list_of_stack_items=('#'))
stack200 = StateStackPair.new(state='q1', list_of_stack_items=())
stack201 = StateStackPair.new(state='q1', list_of_stack_items=('A', 'BB'))

# Definizione di una configurazione completa di DPDA, specificando stato attuale, lista di simboli da leggere (come tupla), contenuto della pila (come tupla), automa relativo

dpdac = DPDAConfiguration.new(state='q0',
                              list_of_tokens=('id1', 'id1', 'id2'),
                              list_of_stack_items=('SYM3', 'SYM3'),
                              automaton=dpda)

print(dpdac)

dpdac0 = DPDAConfiguration.init(state='q0',
                                input_str=('abcab'),
                                stack_str=('XYX'),
                                automaton=dpda1)


# Definizione di una configurazione completa di NPDA, specificando insieme di coppie stato-pila, lista di simboli da leggere (come tupla), automa relativo

npdac = NPDAConfiguration(state_stack_pairs={stack201},
                          list_of_tokens=('aa', 'b', 'aa'),
                          automaton=npda1)

print(npdac)

# Restituzione della computazione effettuata dal NPDA sull'input specificato. Le righe rappresentano le configurazioni attraversate: a dx l'insieme di simboli da leggere, a sx l'insieme di coppie, comprendenti stato e contenuto della pila attuali. In fondo, esito della computazione.

npda1.report_computation(Tools.tokens('aa:b', separator=':'))

# Restituzione di una sequenza (casuale) di configurazioni deterministiche, derivate dalla computazione nondeterministica eseguita dal NPDA sull'input dato.

npda1.report_random_deterministic_path(Tools.tokens('aa:b', separator=':'))


# Descrizione di una macchina di Turing deterministica:
# - tipo di automa: DTM
# - insieme degli stati: insieme di stringhe 
# - alfabeto di input: insieme di stringhe
# - alfabeto di nastro: insieme di stringhe, comprendente i simboli di input e il simbolo blank
# - simbolo blank: simbolo non appartenente all'alfabeto di input
# - stato iniziale: un simbolo dell'alfabeto
# - stati finali: un sottoinsieme dell'insieme degli stati
# - funzione di transizione: dizionario con 
#     - stati come chiavi 
#     - elementi rappresentati da dizionari con 
#         - simboli dell'alfabeto di nastro come chiavi
#         - elementi rappresentati da tuple di tre elementi
#             - stato
#             - simbolo di nastro
#             - carattere in {'R', 'L', 'N'}

# DTM which matches all strings beginning with '0's, and followed by
# the same number of '1's
dtm = DTM(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', 'x', 'y', '.'},
    delta={
        'q0': {
            '0': ('q1', 'x', 'R'),
            'y': ('q3', 'y', 'R')
        },
        'q1': {
            '0': ('q1', '0', 'R'),
            '1': ('q2', 'y', 'L'),
            'y': ('q1', 'y', 'R')
        },
        'q2': {
            '0': ('q2', '0', 'L'),
            'x': ('q0', 'x', 'R'),
            'y': ('q2', 'y', 'L')
        },
        'q3': {
            'y': ('q3', 'y', 'R'),
            '.': ('q4', '.', 'R')
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q4'}
)


print(dtm)

dtm1 = DTM(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'00', '11'},
    tape_symbols={'00', '11', 'x', 'y', '.'},
    delta={
        'q0': {
            '00': ('q1', 'x', 'R'),
            'y': ('q3', 'y', 'R')
        },
        'q1': {
            '00': ('q1', '00', 'R'),
            '11': ('q2', 'y', 'L'),
            'y': ('q1', 'y', 'R')
        },
        'q2': {
            '00': ('q2', '00', 'L'),
            'x': ('q0', 'x', 'R'),
            'y': ('q2', 'y', 'L')
        },
        'q3': {
            'y': ('q3', 'y', 'R'),
            '.': ('q4', '.', 'R')
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q4'}
)


print(dtm1)

# Definizione di un nastro con il suo contenuto (come tupla o come stringa), la posizione della testina (default 0) e il carattere blank (default |)

t = TMTape(list_of_tokens=('ad', 'ca', 'a', 'd'), head=3)
print(t)

t = TMTape.init(input_str='00101', head=-3, blank_symbol='^')
print(t)

t = TMTape.init(input_str='00101', head=-3)
print(t)

t = TMTape.init(input_str='00101')
print(t)

# Definizione di coppia nastro+stato

stp = StateTapePair(state='q0', tape=t)
print(stp)

stp1 = StateTapePair.init(state='q0', input_str='001', head=5, blank_symbol='.')
print(stp1)

# Definizione configurazione DTM, comprendente coppia stato+nastro e automa relativo

dtmc = DTMConfiguration(state_tape_pair=stp, automaton=dtm)
print(dtmc)

dtmc1 = DTMConfiguration.init(state='q0', input_str='011110', head=9, automaton=dtm)
print(dtmc1)

dtm.report_computation(Tools.tokens('0011'))


ntm = NTM(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'id1', 'id2'},
    tape_symbols={'id1', 'id2', 'x', 'y', '.'},
    delta={
        'q0': {
            'id1': {('q1', 'x', 'R'), ('q2', 'y', 'N')},
            'y': {('q3', 'y', 'R')}
        },
        'q1': {
            'id1': {('q1', 'id1', 'R'), ('q1', 'id2', 'L')},
            'id2': {('q2', 'y', 'L')},
            'y': {('q1', 'y', 'R')}
        },
        'q2': {
            'id1': {('q2', 'id1', 'L')},
            'x': {('q0', 'x', 'R')},
            'y': {('q2', 'y', 'L')}
        },
        'q3': {
            'y': {('q3', 'y', 'R')},
            '.': {('q4', '.', 'R')}
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q4'}
)


print(ntm)

ntm1 = NTM(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'a', 'b'},
    tape_symbols={'a', 'b', 'x', 'y', '.'},
    delta={
        'q0': {
            'a': {('q1', 'x', 'R'), ('q2', 'y', 'N')},
            'y': {('q3', 'y', 'R')}
        },
        'q1': {
            'a': {('q1', 'a', 'R'), ('q1', 'b', 'L')},
            'b': {('q2', 'y', 'L')},
            'y': {('q1', 'y', 'R')}
        },
        'q2': {
            'a': {('q2', 'a', 'L')},
            'x': {('q0', 'x', 'R')},
            'y': {('q2', 'y', 'L')}
        },
        'q3': {
            'y': {('q3', 'y', 'R')},
            '.': {('q4', '.', 'R')}
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q4'}
)


t1 = TMTape(list_of_tokens=('id1', 'id2', 'x', '.', 'y'), head=4)
t2 = TMTape(list_of_tokens=Tools.tokens('id2:id2:id2:x:id2', separator=':'), head=2)

stp1 = StateTapePair(state='q0', tape=t1)
stp2 = StateTapePair(state='q2', tape=t2)

ntmc = NTMConfiguration(state_tape_pairs={stp1, stp2}, automaton=ntm)
print(ntmc)

t10 = TMTape(list_of_tokens=('a', 'b', 'x', '.', 'y'), head=4)
t20 = TMTape.init(input_str='aabxa', head=2)

stp10 = StateTapePair(state='q0', tape=t10)
stp20 = StateTapePair(state='q2', tape=t20)

ntmc1 = NTMConfiguration(state_tape_pairs={stp10, stp20}, automaton=ntm1)

ntm1.report_computation(Tools.tokens('abaab'))


