"""
HUMAI 2023

This is a module that has a functions related to noise in data
"""
import functools
from typing import Dict

from numpy.random import choice, random


def anadir_ruido(noise_probability : float, noise_distribution : Dict[str, float]):
    """Adds noise as a result of some function

    Args:
        noise_probability (float): probability of adding noise
        noise_distribution (Dict[str, float]): Dictionary where the key is the
            noise result and the value is the probability chance of each
            ex: {'ups!':0.7, 'UPS!':0.3}
    """

    def inner_decorator(func):
        possible_noise_values = list(noise_distribution.keys())
        noise_value_probabilities = list(noise_distribution.values())
        @functools.wraps(func)
        def wrapper(*args):
            true_value = func(*args)
            if random() <= noise_probability: #ie con prob `noise_probability`
                vals, probs = exclude_true_value(possible_noise_values,
                                                noise_value_probabilities,
                                                true_value)
                return choice(vals, p=probs)

            return true_value
        return wrapper
    return inner_decorator


def exclude_true_value(possible_noise_values, noise_value_probabilities, true_value):
    """Excludes the true value from the noise possibble values, so it is noise

    Args:
        possible_noise_values (list): possible noise values
        noise_value_probabilities (list): possible noise values
        true_value (any): True value that the function return 

    Returns:
        list, list: list of possible noise values and list of their probabilities
    """

    try:
        i = possible_noise_values.index(true_value)
        del possible_noise_values[i]
        del noise_value_probabilities[i]
        sumatoria_de_probabilidad = sum(noise_value_probabilities)
        noise_value_probabilities = \
            [probabilidad/sumatoria_de_probabilidad for \
                 probabilidad in noise_value_probabilities]
    except ValueError:
        return 
    return possible_noise_values, noise_value_probabilities

if __name__ == "__main__":
    @anadir_ruido(0.5, {'ups!':0.7, 'UPS!':0.3})
    def funcion_de_ejemplo(number):
        """ejemplo
        """
        return 2*number
    for aux in range(10):
        print(funcion_de_ejemplo(aux))
