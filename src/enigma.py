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

from abc import abstractmethod, ABC
from string import ascii_lowercase
from typing import Dict, Optional, Tuple, Union


class Layer(ABC):
    """Abstract Base Class for Enigma layers.
    """

    @abstractmethod
    def __call__(self,
                 value: str,
                 reverse: Optional[bool] = None) -> Optional[str]:
        """Implements propagation through the layer.

        Args: 
            value (str): The input character.
            reverse (bool): For layers that support it, whether to feed the 
                            layer with the value as if it was an output in order
                            to get the corresponding input.

        Returns:
            str: The output character.
        """


class Plugboard(Layer):
    """Enigma's plugboard.

    Args:
        plugboad (dict, str, optional): The plugboard to be applied, uses `_std`
                                        as default.
    """

    _std_front: str = 'zphnmswciytqedoblrfkuvgxja'

    def __init__(
            self,
            plugboard: Optional[Union[Dict[str, str], str]] = None) -> None:
        """Builds a plugboard.
        """

        self._front = None
        self._back = None
        self.front = plugboard

    @property
    def front(self) -> Dict[str, str]:
        """Returns current plugboard.
        Returns:
            dict: A dictionary representing the current plugboard.  The 
                  dictionary is supposed to have 26 keys, one for each letter of
                  the alphabet, and should associate to each key another letter.
        """

        return self._front

    @front.setter
    def front(self,
              value: Optional[Union[Dict[str, str], str]] = None) -> None:
        """Sets the plugboard to the specified value.

        Args:
            value (dict, str, optional): The new value for the plugboard.  If 
                                         `None` defaults to 
                                         `Enigma._std_front`.  If `value` is a  
                                         string it is supposed to have a length 
                                         of 26 characters, interpreted as a  
                                         plugboard in alphabetical order. 

        Raises:
            ValueError: If either the passed string value is not 26 characters 
                        or the passed dictionary hasn't 26 entries.
            TypeError: If an value of an invalid type is passed.
        """

        if value is None:
            value = self._std_front

        if isinstance(value, str):
            if len(value) != len(ascii_lowercase):
                raise ValueError('Expected {} characters, found {}'.format(
                    len(ascii_lowercase), len(value)))

            value = dict(zip(ascii_lowercase, value))

        if isinstance(value, dict):
            if len(value.keys()) != len(ascii_lowercase):
                raise ValueError('Expected {} keys, found {}'.format(
                    len(ascii_lowercase), len(value)))

            if set(value.keys()) != set(ascii_lowercase) or set(
                    value.values()) != set(ascii_lowercase):
                raise ValueError(
                    'Invalid characters found, expected to be a lowercase ascii'
                )

        if not isinstance(value, dict):
            raise TypeError(
                'Expected dictionary or string, but found {}'.format(
                    type(value)))

        self._front = value

        self._back = dict(zip(value.values(), value.keys()))

    @property
    def back(self) -> Dict[str, str]:
        """A reversed dictionary plugboard.

        Returns:
            dict: The key-value swapped `self.plugboard`.
        """

        return self._back

    def __call__(self,
                 value: str,
                 reverse: Optional[bool] = False) -> Optional[str]:
        """Performs a letter encryption.

        Args:
            value (str): The ascii character to encrypt.
            reverse (bool): Whether or not to input the letter in reverse.

        Returns:
            str: The encrypted letter.
        """

        if reverse is None:
            reverse = False

        return self.back.get(value) if reverse else self.front.get(value)


class Enigma:
    """Code-implementation of the Enigma Machine.

    Args:
        layers (tuple, optional): A tuple of enigma layers.
        order (tuple, optional): A tuple of tuples of two entries representing
                                 the order and direction in which the character
                                 to be enctypted is supposed to be passed to the
                                 layers.
    """

    _std_layers: Tuple[Layer] = (Plugboard(), )
    _std_order: Tuple[Tuple[int, bool]] = ((0, True), )

    def __init__(self,
                 layers: Optional[Tuple[Layer]] = None,
                 order: Optional[Tuple[Tuple[int, bool]]] = None):
        """German blacksmiths and engineers are going to build a new Enigma 
        machine.
        """

        self._layers = layers or self._std_layers
        self._order = order or self._std_order

    @property
    def layers(self) -> Tuple[Layer]:
        """The layers in which the Enigma machine should pass the letters.

        Returns:
            tuple: A tuple containing the layers of the Enigma machine.
        """

        return self._layers

    @property
    def order(self) -> Tuple[Tuple[int, bool]]:
        """The order in which the layers should be used.

        Returns:
            tuple: A tuple containing the order of the layers.
        """

        return self._order

    def __call__(self, value: str) -> str:
        """Forwards the input throught the layers of the Enigma machine.

        Args:
            value (str): The input character ot feed to the Enigma machine.
        
        Return:
            str: The output character.
        """

        for i, r in self.order:
            value = self.layers[i](value, r)

        return value
