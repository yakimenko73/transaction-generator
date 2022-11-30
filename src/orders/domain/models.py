import dataclasses
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Any

from .enums import *


class Order(ABC):
    pass


@dataclass
class FiatOrder(Order):
    id: hex = 0
    side: OrderSide = OrderSide.UNSPECIFIED
    instrument: OrderInstrument = OrderInstrument.UNSPECIFIED
    status: OrderStatus = OrderStatus.UNSPECIFIED
    px_init: float = 0.0
    px_fill: float = 0.0
    volume_init: int = 0
    volume_fill: int = 0
    note: OrderNote = OrderNote.UNSPECIFIED
    tags: List[OrderTag] = field(default_factory=list)
    date: datetime = None

    def replace(self, status: OrderStatus) -> Any:
        return dataclasses.replace(self, status=status, date=self.date + timedelta(milliseconds=self.date.second))
