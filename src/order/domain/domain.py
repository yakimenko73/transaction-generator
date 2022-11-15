from abc import ABC
from dataclasses import dataclass

from src.order.domain.enums import *


class Order(ABC):
    pass


@dataclass
class FiatOrder(Order):
    side: OrderSide
    instrument: OrderInstrument
    status: OrderStatus
    id: hex = 0
    px_init: float = 0.0
    px_fill: float = 0.0
    volume_init: int = 0
    volume_fill: int = 0
    note: str = None
    tags: str = None
    date: str = None
