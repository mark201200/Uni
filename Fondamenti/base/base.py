#!/usr/bin/env python3
"""Base classes and methods."""

import abc
import yaml

import base.config as config


class Base(metaclass=abc.ABCMeta):
    """Methods common to all objects."""

    @abc.abstractmethod
    def __init__(self):
        """Initialize an object."""
        raise NotImplementedError

    def _instance_of(self):
        """Print the class instantiated by the object."""
        print(self.__class__.__name__)

    def __eq__(self, other):
        """Check if two objects are equal."""
        return vars(self) == vars(other)

    def save(self, file):
        """Save a copy of the definition of this re in a json file."""
        with open(config.store_folder+file+'.yaml', 'w') as f:
            yaml.dump(self, f)

    def __repr__(self):
        """Associate a description of the object to its identifier."""
        return self.__class__.__name__ + repr(self.__dict__)

