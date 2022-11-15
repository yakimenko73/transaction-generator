from enum import Enum
from typing import Tuple


class OrderSide(Enum):
    SELL: int = 1
    BUY: int = 2


class OrderInstrument(Enum):
    EURGBP: Tuple = (0.88491, 0.88473)
    EURCHF: Tuple = (1.08052, 1.02197),
    EURCAD: Tuple = (1.55111, 1.41313),
    AUDEUR: Tuple = (0.629698, 0.62963),
    EURNZD: Tuple = (1.68618, 1.68501),
    EURJPY: Tuple = (127.09323, 124.88801),
    GBPJPY: Tuple = (143.51412, 143.23002),
    CHFJPY: Tuple = (117.5189, 116.89021),
    AUDJPY: Tuple = (80.03001, 80.00315),
    GBPCAD: Tuple = (1.75086, 1.44401),
    EURRUB: Tuple = (91.99600, 91.31132),


class OrderStatus(Enum):
    NEW: int = 1
    INPROCESS: int = 2
    FILL: int = 3
    PARTIALFILL: int = 4
    CANCEL: int = 5
    DONE: int = 6
