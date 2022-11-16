import random
from enum import Enum
from typing import Type


def rand_hex(start: int, stop: int, seed: int) -> hex:
    random.seed(seed)

    return hex(random.randint(start, stop))


def rand_bool() -> bool:
    return bool(random.getrandbits(1))


def rand_enum_value(enum: Type[Enum]) -> Enum:
    return enum(random.randint(1, len(enum) - 1))
