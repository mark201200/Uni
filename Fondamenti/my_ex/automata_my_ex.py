
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
