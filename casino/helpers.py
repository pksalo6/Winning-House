import secrets
import random
from typing import Tuple


def generate_random_key() -> str:
    """
    Generate cryptographically secure random
    pseudo numbers
    """
    return secrets.token_urlsafe()


def generate_roll_values(block: int, choices: Tuple) -> Tuple:
    """
    A function to generate random values from 1 to 3
    which will be used to pick blocks value i.e. cherry,
    lemon etc.
    """
    return tuple(random.choice(choices) for _ in range(block))


def re_roll_probability_by_30() -> int:
    """
    A function to compute re-roll probability by 30%
    """
    return random.choice([1, 1, 1, 0, 0, 0, 0, 0, 0, 0])


def re_roll_probability_by_60() -> int:
    """
    A function to compute re-roll probability by 60%
    """
    return random.choice([1, 1, 1, 1, 1, 1, 0, 0, 0, 0])


SYMBOL_DICT = {
    1: {"name": "Cherry", "reward": 10},
    2: {"name": "lemon", "reward": 20},
    3: {"name": "orange", "reward": 30},
    4: {"name": "watermelon", "reward": 40},
}
