"""This package provides a Python-code implementation of the Enigma machine 
encryption algorithm and of Alan Turing's British Bombe decryption machine.
"""
__all__ = ['Enigma']

from .enigma import __doc__ as _enigma_doc, Enigma

__doc__ += '\n\n' + _enigma_doc
del _enigma_doc
