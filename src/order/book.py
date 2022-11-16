from abc import ABC, abstractmethod

from .builder import OrderBuilder, PseudoRandomFiatOrderBuilder
from .domain.domain import Order, FiatOrder
from src.config import Config


class OrderBook(ABC):
    @abstractmethod
    def get_last_order(self) -> Order:
        pass


class FiatOrderBook(OrderBook):
    def __init__(self, config: Config):
        self._builder = PseudoRandomFiatOrderBuilder(config)

    @property
    def builder(self) -> OrderBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: OrderBuilder):
        self._builder = builder

    def get_last_order(self) -> FiatOrder:
        self._builder.produce_id()
        side = self._builder.produce_side()
        instrument = self._builder.produce_instrument()
        status = self._builder.produce_status()
        px_init = self._builder.produce_px_init(side, instrument)
        self._builder.produce_px_fill(px_init)
        volume_init = self._builder.produce_volume_init()
        self._builder.produce_volume_fill(volume_init, status)
        self._builder.produce_note()
        self._builder.produce_tags()
        self._builder.produce_date()

        return self._builder.order
