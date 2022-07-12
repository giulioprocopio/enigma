"""This package provides a Python-code implementation of the Enigma machine 
encryption algorithm and of Alan Turing's British Bombe decryption machine.
"""
__all__ = ['Enigma']

from .enigma import __doc__ as _enigma_doc, Enigma


def _append_doc(doc):
    globals()['__doc__'] += '\n\n{}'.format(_enigma_doc)

_append_doc(_enigma_doc)
del _enigma_doc

del _append_doc
