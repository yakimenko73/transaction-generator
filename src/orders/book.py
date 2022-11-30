from abc import ABC, abstractmethod

from loguru import logger

from config import GeneratorConfig
from .domain.models import Order, FiatOrder
from .domain.enums import OrderStatus
from .storage import InMemoryStorage


class OrderBook(ABC):
    @abstractmethod
    def add(self, order: Order) -> None:
        pass


class FiatOrderBook(OrderBook):
    def __init__(self, config: GeneratorConfig, storage: InMemoryStorage):
        self._config = config
        self._storage = storage
        self._size = 0

    @property
    def size(self):
        return self._size

    def add(self, order: FiatOrder) -> None:
        self._save_with_statuses(order)
        self._size += 1

        logger.info(f'{order.id} order successfully added to storage')

    def _save_with_statuses(self, order: FiatOrder) -> None:
        if self._size < self._config.segment_size(self._config.percent_completed_orders):
            self._save(order, OrderStatus.IN_PROCESS, order.status, OrderStatus.DONE)
        elif self._size < self._config.first_two_segments_size():
            self._save(order, OrderStatus.NEW, OrderStatus.IN_PROCESS, order.status, OrderStatus.DONE)
        else:
            self._save(order, OrderStatus.NEW, OrderStatus.IN_PROCESS, order.status)

    def _save(self, order: Order, *statuses: OrderStatus) -> None:
        for status in statuses:
            order = order.replace(status)
            self._storage.add(order)
