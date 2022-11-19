import random
from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from typing import List, Any

from config import IdGeneratorConfig, DateGeneratorConfig, PxFillConfig, VolumeInitConfig
from utils import rand_hex, rand_bool, rand_enum_value
from .domain.enums import *


class Generator(ABC):
    @abstractmethod
    def generate(self, *args, **kwargs) -> Any:
        pass


class IdGenerator(Generator):
    def __init__(self, config: IdGeneratorConfig):
        self._id = config.seed
        self._config = config

    def generate(self) -> hex:
        self._id = rand_hex(self._config.start, self._config.stop, self._id)

        return self._id


class SideGenerator(Generator):
    def generate(self) -> OrderSide:
        return OrderSide.SELL if rand_bool() else OrderSide.BUY


class InstrumentGenerator(Generator):
    def generate(self) -> OrderInstrument:
        return rand_enum_value(OrderInstrument)


class StatusGenerator(Generator):
    def generate(self) -> OrderStatus:
        return OrderStatus(random.randint(OrderStatus.FILL.value, OrderStatus.CANCEL.value))


class PXInitGenerator(Generator):
    def generate(self, side: OrderSide, instrument: OrderInstrument) -> float:
        sell, buy = OrderInstrumentSellPrice[instrument.name], OrderInstrumentBuyPrice[instrument.name]

        return sell.value if side == OrderSide.SELL else buy.value


class PXFillGenerator(Generator):
    def __init__(self, config: PxFillConfig):
        self._config = config

    def generate(self, px_init: float) -> float:
        diff = random.uniform(self._config.start, self._config.stop)
        px_fill = px_init + diff if rand_bool() else px_init

        return round(px_fill, self._config.rounding)


class VolumeInitGenerator(Generator):
    def __init__(self, config: VolumeInitConfig):
        self._config = config

    def generate(self) -> int:
        volume = random.randint(self._config.start, self._config.stop)

        return round(volume, self._config.rounding)


class VolumeFillGenerator(Generator):
    def __init__(self, config: VolumeInitConfig):
        self._config = config

    def generate(self, volume_init: int, status: OrderStatus) -> int:
        unfulfilled = random.randint(self._config.start, volume_init)

        return volume_init - unfulfilled if status == OrderStatus.PARTIAL_FILL else volume_init


class DateGenerator(Generator):
    def __init__(self, config: DateGeneratorConfig):
        self._date = config.start_date
        self._config = config

    def generate(self) -> datetime:
        increment = random.randint(self._config.start, self._config.stop)
        self._date = self._date + timedelta(milliseconds=increment)

        return self._date


class NoteGenerator(Generator):
    def generate(self) -> OrderNote:
        return rand_enum_value(OrderNote)


class TagsGenerator(Generator):
    def generate(self) -> List[OrderTag]:
        tags_count = random.randint(1, len(OrderTag) - 1)
        tags = list(filter(lambda tag: tag != OrderTag.UNSPECIFIED, OrderTag))

        return random.choices(tags, k=tags_count)
