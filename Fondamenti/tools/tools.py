#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility classes."""

import itertools
import yaml

import re
import base.config as config

class States_pairs_table():
    """Implementation of a table of pairs of states."""
    def __init__(self, dfa):
        self.table = {
            frozenset(c): [False, set()]
            for c in itertools.combinations(dfa.states, 2)
        }
        self.keys = sorted([tuple(k) for k in self.table.keys()], key=lambda x: x[0])

    def set_flag_true(self, key):
        self.table[frozenset(key)][0] = True
        
    def flag(self, key):
        return self.table[frozenset(key)][0]
    
    def pairs(self, key):
        return self.table[frozenset(key)][1]
    
    def no_pairs(self, key):
        self.table[frozenset(key)][1] = set()
        
    def add_pair(self, key, pair):
        self.table[frozenset(key)][1].add(pair)
        
    @property
    def unmarked_pairs(self):
        return set(filter(lambda s: not self.table[s][0], self.table.keys()))
        
    def __str__(self):
        s = ''
        for k1 in sorted(self.keys):
            k = frozenset(k1)
            s += '({}, {}): '.format(k1[0], k1[1])
            s += '{}\t'.format(self.table[k][0])
            s += '{}'.format(self.table[k][1])
            s += '\n'
        return s


class Dict_of_sets(dict):
    """Implementation of a dictionary of sets of items."""

    def __setitem__(self, key, value):
        """Setter method for dictionary."""
        try:
            self[key]
        except KeyError:
            super().__setitem__(key, set())
        self[key].add(value)


class Tools():
    """Just a container of static methods."""

    @classmethod
    def set_token_separator(cls, separator):
        """Set string used as token separator in internal phrase coding."""
        config.token_separator = separator

    @classmethod
    def get_token_separator(cls):
        """Get string used as token separator in internal phrase coding."""
        return config.token_separator

    @classmethod
    def set_str_token_separator(cls, separator):
        """Set string used as token separator in phrase printing."""
        config.str_token_separator = separator

    @classmethod
    def get_str_token_separator(cls):
        """Get string used as token separator in phrase printing."""
        return config.str_token_separator

    @staticmethod
    def first_nt(phrase, nonterminals):
        """
        Return the index of the first nonterminal in a phrase.

        None if the phrase contains only terminals
        """
        try:
            ind = next((i for i, ch in enumerate(phrase) if
                        ch in nonterminals), None)
        except StopIteration:
            ind = None
        return ind

    @staticmethod
    def first_left(phrase, left_parts):
        """Return the list of indices of the first left parts in a phrase."""
        matching_lefts = []
        for left_part in left_parts:
            for i in range(len(phrase)-len(left_part)+1):
                for j in range(len(left_part)):
                    if phrase[i+j] != left_part[j]:
                        break
                else:
                    matching_lefts.append((i, left_part))
        min_index = min([x[0] for x in matching_lefts])
        return [x for x in matching_lefts if x[0] == min_index]

    @staticmethod
    def last_nt(phrase, nonterminals):
        """
        Return the index of the last nonterminal in a phrase.

        None if the phrase contains only terminals
        """
        try:
            ind = next((i for i, ch in enumerate(phrase[::-1]) if
                        ch in nonterminals), None)
            ind = len(phrase)-ind-1
        except StopIteration:
            ind = None
        return ind

    @staticmethod
    def list_of_tokens(input_str=None, separator=None):
        """Return the list of tokens from an input string, under the form of a tuple."""
        if input_str == '':
            lst = ('',)
        elif not input_str:
            lst = tuple()
        elif not separator:
            lst = tuple(input_str)
        else:
            lst = tuple([x for x in re.split('[\s,' + separator + ']+', input_str) if x != ''])
        return lst
    
    @staticmethod
    def tuple_from_sequence(t):
        if t == ():
            return tuple()
        elif isinstance(t, str):
            return (t,)
        else:
            return t

    @staticmethod
    def string_from_tokens(lst):
        """Return a string from the given list of tokens."""
        separator = config.token_separator
        s = separator.join(lst)
        return s
    
    @staticmethod
    def output_string_from_tokens(lst, separator=' '):
        """Return a string from the given list of tokens."""
        if len(lst)==1 and lst[0]=='':
            s = " "
        else:
            s = separator.join(lst)
        return s

    @staticmethod
    def phrase(list_of_tokens):
        """Return a string to be printed from the given list of tokens."""
        separator = config.str_token_separator
        s = separator.join(list_of_tokens)
        return s
    
    @staticmethod
    def merge_tuples(t_pair):
        """Return tuple from merging the ones in the given pair."""
        lst = list(t_pair[0])
        lst.extend(t_pair[1])
        return tuple(lst)
    
    @staticmethod
    def insert_in_tuple(t, i, t1):
        """Insert item t1 in tuple t at given position i."""
        lst = list(t[:i])
        lst.extend(t1)
        lst.extend(t[i+1:])
        return tuple(lst)
    
    @staticmethod
    def simple_productions(productions):
        prods = {}
        for left_part, right_parts in productions.items():
            prods[Tools.list_of_tokens(left_part, separator='')] = set()
            for right_part in right_parts:
                prods[Tools.list_of_tokens(left_part, separator='')].add(Tools.list_of_tokens(right_part, separator=''))
        return prods
    
    @staticmethod
    def simple_sequence(input_str=None):
        if not input_str:
            return tuple()
        elif input_str=='_':
            return tuple()
        else:
            return Tools.list_of_tokens(input_str, separator='')

    @staticmethod
    def print(input_str, separator=''):
        """Return a string from the given list of tokens."""
        if not input_str:
            return '_'
        else:
            return  separator.join(input_str)

    @staticmethod
    def print_tuple(lst, separator=' '):
        """Return a string from the given list of tokens."""
        if not lst:
            return '()'
        elif isinstance(lst, str):
            return '('+lst+')'
        elif len(lst) == 1:
            return '('+lst[0]+')'
        else:
            return  '('+separator.join(lst)+')'

    @staticmethod
    def tokens(input_str=None, separator=None):
        """Return the list of tokens from an input string, under the form of a tuple."""
        if not input_str:
            return tuple()
        else:
            return Tools.list_of_tokens(input_str, separator)
        
    @staticmethod
    def all_chars(alphabet, allow="S'"):
        """Return true if all input symbols have length 1."""
        lst = [x for x in alphabet if len(x) > 1 and x != allow]
        return not lst
    
    @staticmethod
    def new_nt_symbol(nonterminals):
        """
        Return a new nonterminal symbol, not included in nonterminals.

        Symbol is an uppercase char, if possible. Otherwise a string.
        """
        def nt_substring(k):
            if k==1:
                generator = (chr(x) for x in range(65, 90))
                for c in generator:
                    yield c
            else:
                for c in (chr(x) for x in range(65, 90)):
                    generator = nt_substring(k-1)
                    for s in generator:
                        yield c+s

        k = 1
        while True:
            for s in nt_substring(k):
                if s not in nonterminals:
                    return s
            k += 1

# --------------------------------------------------------------------------------

    @staticmethod
    def car(t):
        """Return first item in tuple."""
        if not t:
            raise Exception('empty tuple')
        else:
            return t[0]
        
    @staticmethod
    def cdr(t):
        """Return new tuple containing all items in tuple except first one."""
        if not t:
            raise Exception('empty tuple')
        else:
            return t[1:]

    @staticmethod
    def cons(item, t):
        """Return new tuple containing all items in tuple except first one."""
        lst = list(t)
        lst.insert(0, item)
        return tuple(lst)
    
    @staticmethod
    def tuple(item):
        if isinstance(item, tuple):
            return item
        elif isinstance(item, list):
            return tuple(item)
        else:
            return (item,)
        
    @staticmethod
    def load(file):
        """Save a copy of the definition of this re in a json file."""
        with open(config.store_folder+file+'.yaml') as f:
            o = yaml.load(f, Loader=yaml.FullLoader)
            o.validate()
            return o
