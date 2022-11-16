import random
from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from typing import List

from src.config import IdGeneratorConfig, DateGeneratorConfig
from src.constants import *
from src.utils import rand_hex, rand_bool, rand_enum_value
from .domain.enums import *


class Generator(ABC):
    @abstractmethod
    def generate(self, *args, **kwargs):
        pass


class IdGenerator(Generator):
    def __init__(self, config: IdGeneratorConfig):
        self._id = config.seed

    def generate(self) -> hex:
        self._id = rand_hex(ORDER_ID_MIN_LENGTH, ORDER_ID_MAX_LENGTH, self._id)

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
        enum = OrderInstrumentSellPrice[instrument.name] if side == OrderSide.SELL \
            else OrderInstrumentBuyPrice[instrument.name]

        return enum.value


class PXFillGenerator(Generator):
    def generate(self, px_init: float) -> float:
        diff = random.uniform(ORDER_PX_FILL_START, ORDER_PX_FILL_STOP)
        px_fill = px_init + diff if rand_bool() else px_init

        return round(px_fill, ORDER_PX_ROUNDING)


class VolumeInitGenerator(Generator):
    def generate(self) -> int:
        volume = random.randint(ORDER_VOLUME_INIT_START, ORDER_VOLUME_INIT_STOP)

        return round(volume, ORDER_VOLUME_ROUNDING)


class VolumeFillGenerator(Generator):
    def generate(self, volume_init: int, status: OrderStatus) -> int:
        unfulfilled = random.randint(ORDER_VOLUME_INIT_START, volume_init)

        return volume_init - unfulfilled if status == OrderStatus.PARTIAL_FILL else volume_init


class DateGenerator(Generator):
    def __init__(self, config: DateGeneratorConfig):
        self._date = config.start_date

    def generate(self) -> datetime:
        increment = random.randint(ORDER_DATE_INCREMENT_START, ORDER_DATE_INCREMENT_STOP)
        self._date = self._date + timedelta(milliseconds=increment)

        return self._date


class NoteGenerator(Generator):
    def generate(self) -> OrderNote:
        return rand_enum_value(OrderNote)


class TagsGenerator(Generator):
    def generate(self) -> List[OrderTag]:
        tags_count = random.randint(1, len(OrderTag) - 1)
        tags = list(filter(lambda tag: tag != OrderTag.UNRECOGNIZED, OrderTag))

        return random.choices(tags, k=tags_count)
