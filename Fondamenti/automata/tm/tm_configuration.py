#!/usr/bin/env python3
"""Classes and methods for working with TM configurations."""


import abc

import automata.base.configuration as co


class TMConfiguration(co.Configuration, metaclass=abc.ABCMeta):
    """
    Representation of the complete runtime state of a Turing mmachine.

    It is hashable and immutable.
    """

    pass
