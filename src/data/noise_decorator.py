import functools
from typing import Dict, Iterable, Union
from numpy.random import choice, random

def anadir_ruido(noise_probability : float, noise_distribution : Dict[str, float]):
    def inner_decorator(func):
        possible_noise_values = list(noise_distribution.keys())
        noise_value_probabilities = list(noise_distribution.values())
        @functools.wraps(func)
        def wrapper(*args):
            true_value = func(*args)
            if random() <= noise_probability: #ie con prob `noise_probability`
                vals, probs = exclude_true_value(possible_noise_values, noise_value_probabilities, true_value)
                return choice(vals, p=probs)
            else:
                return true_value
        return wrapper
    return inner_decorator


def exclude_true_value(possible_noise_values, noise_value_probabilities, true_value):
    try:
        i = possible_noise_values.index(true_value)
        possible_noise_values = possible_noise_values[:i] + possible_noise_values[i+1:]
        noise_value_probabilities = noise_value_probabilities[:i] + noise_value_probabilities[i+1:]
        z = sum(noise_value_probabilities)
        noise_value_probabilities = [x/z for x in noise_value_probabilities]
    except ValueError:
        pass
    return possible_noise_values, noise_value_probabilities

if __name__ == "__main__":
    @anadir_ruido(0.5, {'ups!':0.7, 'UPS!':0.3})
    def funcion_de_ejemplo(x):
        return 2*x
    for x in range(10):
        print(funcion_de_ejemplo(x))
