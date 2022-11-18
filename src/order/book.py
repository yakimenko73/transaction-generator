from abc import ABC, abstractmethod

from loguru import logger

from src.config import GeneratorsConfig
from src.order.storage import Storage
from src.utils import percentage_off
from .domain.domain import Order, FiatOrder
from .domain.enums import OrderStatus


class OrderBook(ABC):
    @abstractmethod
    def add(self, order: Order) -> None:
        pass


class OrderHistoryLog(ABC):
    @abstractmethod
    def write(self, order: FiatOrder) -> None:
        pass

    @abstractmethod
    def write_after_created(self, order: FiatOrder) -> None:
        pass

    @abstractmethod
    def write_before_completed(self, order: FiatOrder) -> None:
        pass


class FiatOrderBook(OrderBook):
    def __init__(self, config: GeneratorsConfig, storage: Storage):
        self._orders_log = FiatOrderHistoryLog(storage)
        self._config = config
        self._size = 0

    @property
    def size(self):
        return self._size

    def add(self, order: FiatOrder) -> None:
        if self._size < self._first_segment_size():
            self._orders_log.write_after_created(order)
        elif self._size < self._first_segment_size() + self._second_segment_size():
            self._orders_log.write(order)
        else:
            self._orders_log.write_before_completed(order)

        self._size += 1

        logger.info(f'{order.id} order successfully added to storage')

    def _first_segment_size(self) -> int:
        return self._segment_size(self._config.percent_completed_orders)

    def _second_segment_size(self) -> int:
        return self._segment_size(self._config.percent_created_and_completed_orders)

    def _segment_size(self, segment_percent: int) -> int:
        return int(percentage_off(self._config.max_orders, segment_percent))


class FiatOrderHistoryLog(OrderHistoryLog):
    def __init__(self, storage: Storage):
        self._storage = storage

    def write(self, order: FiatOrder) -> None:
        processing_status = order.status
        self._save(order, OrderStatus.NEW)
        self._save(order, OrderStatus.IN_PROCESS)
        self._save(order, processing_status)
        self._save(order, OrderStatus.DONE)

    def write_after_created(self, order: FiatOrder) -> None:
        processing_status = order.status
        self._save(order, OrderStatus.IN_PROCESS)
        self._save(order, processing_status)
        self._save(order, OrderStatus.DONE)

    def write_before_completed(self, order: FiatOrder) -> None:
        processing_status = order.status
        self._save(order, OrderStatus.NEW)
        self._save(order, OrderStatus.IN_PROCESS)
        self._save(order, processing_status)

    def _save(self, order: FiatOrder, status: OrderStatus) -> None:
        order.update_status(status)
        self._storage.add(order)
