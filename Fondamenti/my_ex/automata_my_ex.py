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
from automata.tm.dtm import DTM
from tools.tools import Tools

# Definire un mtd a 1 nastro che, dato un numero binario, ne calcola il doppio

# Aggiungendo uno 0 a destra (assumendo che il bit più significativo è a sinistra, quindi che si legge da sx verso dx)
dtm_zerofine_sx = DTM(
    states={'q0'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', '.'},
    delta={
        'q0': {
            '0': ('q0', '0', 'R'),
            '1': ('q0', '1', 'R'),
            '.': ('q1', '0', 'N')
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q1'}
)

# Aggiungendo uno 0 a sinistra (assumendo che il bit più significativo è a destra, quindi che si legge da dx verso sx)
dtm_zerofine_dx = DTM(
    states={'q0'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', '.'},
    delta={
        'q0': {
            '0': ('q0', '0', 'L'),
            '1': ('q0', '1', 'L'),
            '.': ('q1', '0', 'N')
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q1'}
)

# shiftando ogni bit a sinistra (assumo che il numero si legge da sx a dx)
dtm_zerofine_shift = DTM(
    states={'q0', 'q1', 'q2', 'q3', 'q4'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', '.'},
    delta={
        'q0': {
            '0': ('q1', '.', 'L'),
            '1': ('q2', '.', 'L'),
            '.': ('q3', '.', 'R')
        },
        'q1': {
            '.': ('q0', '0', 'R')
        },
        'q2': {
            '.': ('q0', '1', 'R')
        },
        'q3': {
            '.': ('q4', '.', 'L'),
            '0': ('q1', '.', 'L'),
            '1': ('q2', '.', 'L')
        },
        'q4': {
            '.': ('q5', '0', 'L')
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q5'}
)

dtm_zerofine_dx.report_computation(Tools.tokens('111'))
dtm_zerofine_sx.report_computation(Tools.tokens('1110101'))
dtm_zerofine_shift.report_computation(Tools.tokens('1110101'))

dtm_esercizio_slide3 = DTM(
    states={'q0', 'q1'},
    input_symbols={'a', 'b'},
    tape_symbols={'a', 'b', '_'},
    delta={
        'q0': {
            'a': ('q0', '_', 'R'),
            'b': ('q1', '_', 'R')
        },
        'q1': {
            'b': ('q1', '_', 'R'),
            '_': ('q2', '_', 'R')
        }
    },
    initial_state='q0',
    blank_symbol='_',
    final_states={'q2'}
)

dtm_esercizio_slide3.report_computation(Tools.tokens('aaaaaaaa'))

dtm_esercizio_slide4 = DTM(
    states={'q0', 'q1'},
    input_symbols={'a', 'b'},
    tape_symbols={'a', 'b', '_'},
    delta={
        'q0': {
            'a': ('q0', '_', 'R'),
            'b': ('q1', '_', 'R')
        },
        'q1': {
            'b': ('q1', '_', 'R'),
            '_': ('q2', '_', 'R'),
            'a': ('q0', '_', 'R')
        }
    },
    initial_state='q0',
    blank_symbol='_',
    final_states={'q2'}
)

dtm_esercizio_slide4.report_computation(Tools.tokens('babbbabbbababbbbabababb'))
