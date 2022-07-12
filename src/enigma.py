"""Implementation of an Enigma machine.

The Enigma machine is a cipher device developed and used in the early - to 
mid-20th century to protect commercial, diplomatic, and military communication. 
It was employed extensively by Nazi Germany during World War II, in all branches 
of the German military. The Enigma machine was considered so secure that it was 
used to encipher the most top-secret messages.

The Enigma has an electromechanical rotor mechanism that scrambles the 26 
letters of the alphabet. In typical use, one person enters text on the Enigma's 
keyboard and another person writes down which of the 26 lights above the 
keyboard illuminated at each key press. If plain text is entered, the 
illuminated letters are the ciphertext. Entering ciphertext transforms it back 
into readable plaintext. The rotor mechanism changes the electrical connections 
between the keys and the lights with each keypress.
"""
__all__ = ['Enigma']

from string import ascii_lowercase
from typing import Dict, Optional, Union


class Enigma:
    """Code-implementation of the Enigma Machine.
    """

    _std_plugboard: str = 'zphnmswciytqedoblrfkuvgxja'

    def __init__(self, plugboard: Optional[Union[Dict[str, str], str]] = None) -> None:
        """Builds a new Enigma machine.
        """

        self.plugboard = plugboard

    @property
    def plugboard(self) -> Dict[str, str]:
        """Returns current plugboard.

        Returns:
            dict: A dictionary representing the current plugboard.  The 
                  dictionary is supposed to have 26 keys, one for each letter of
                  the alphabet, and should associate to each key another letter.
        """

        return self._plugboard

    @plugboard.setter
    def plugboard(self, value: Optional[Union[Dict[str, str], str]] = None) -> None:
        """Sets the plugboard to the specified value.

        Args:
            value (dict, str, optional): The new value for the plugboard.  If 
                                         `None` defaults to 
                                         `Enigma._std_plugboard`.  If `value` is 
                                         a string it is supposed to have a 
                                         length of 26 characters, interpreted as 
                                         a plugboard in alphabetical order. 

        Raises:
            ValueError: If either the passed string value is not 26 characters 
                        or the passed dictionary hasn't 26 entries.
        """

        if value is None:
            value = self._std_plugboard

        if isinstance(value, str):
            if len(value) != len(ascii_lowercase):
                raise ValueError('Expected {} characters, found {}'.format(len(ascii_lowercase), len(value)))

            value = dict(zip(ascii_lowercase, value))
        
        if isinstance(value, dict):
            if len(value.keys()) != len(ascii_lowercase):
                raise ValueError('Expected {} keys, found {}'.format(len(ascii_lowercase), len(value)))

            if set(value.keys()) != set(ascii_lowercase) or set(value.values()) != set(ascii_lowercase):
                raise ValueError('Invalid characters found, expected to be a lowercase ascii')

        if not isinstance(value, dict):
            raise TypeError('Expected dictionary or string, but found {}'.format(type(value)))

        self._plugboard = value
