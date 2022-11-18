from abc import abstractmethod, ABC
from typing import List, Optional

from src.order.domain.domain import Order


class Storage(ABC):
    @abstractmethod
    def add(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_all(self) -> List[Order]:
        pass

    @abstractmethod
    def find_by_id(self, id_: hex) -> Order:
        pass


class ArrayStorage(Storage):
    def __init__(self):
        self._orders = []

    def add(self, order: Order) -> Order:
        self._orders.append(order)

        return order

    def find_all(self) -> List[Order]:
        return self._orders

    def find_by_id(self, id_: hex) -> Optional[Order]:
        return next(filter(lambda order: order.id == id_, self._orders), None)
