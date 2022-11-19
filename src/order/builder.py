from loguru import logger

from src.config import GeneratorsConfig
from .domain.domain import FiatOrder, Order
from .generators import *


class OrderBuilder(ABC):
    @abstractmethod
    def add_id(self) -> hex:
        pass

    @abstractmethod
    def add_side(self) -> OrderSide:
        pass

    @abstractmethod
    def add_instrument(self) -> OrderInstrument:
        pass

    @abstractmethod
    def add_status(self) -> OrderStatus:
        pass

    @abstractmethod
    def add_px_init(self, side: OrderSide, instrument: OrderInstrument) -> float:
        pass

    @abstractmethod
    def add_px_fill(self, px_init: float, status: OrderStatus) -> float:
        pass

    @abstractmethod
    def add_volume_init(self) -> int:
        pass

    @abstractmethod
    def add_volume_fill(self, volume_init: int, status: OrderStatus) -> int:
        pass

    @abstractmethod
    def add_date(self) -> datetime:
        pass

    @abstractmethod
    def add_note(self) -> OrderNote:
        pass

    @abstractmethod
    def add_tags(self) -> List[OrderTag]:
        pass

    @abstractmethod
    def build(self) -> Order:
        pass


class PseudoRandomFiatOrderBuilder(OrderBuilder):
    def __init__(self, config: GeneratorsConfig):
        self._order = FiatOrder()
        self._id_gen = IdGenerator(config.id_generator)
        self._side_gen = SideGenerator()
        self._instrument_gen = InstrumentGenerator()
        self._status_gen = StatusGenerator()
        self._px_init_gen = PXInitGenerator()
        self._px_fill_gen = PXFillGenerator(config.px_fill_generator)
        self._volume_init_gen = VolumeInitGenerator(config.volume_init_generator)
        self._volume_fill_gen = VolumeFillGenerator(config.volume_init_generator)
        self._date_gen = DateGenerator(config.date_generator)
        self._note_gen = NoteGenerator()
        self._tags_gen = TagsGenerator()

    @property
    def order(self) -> FiatOrder:
        return self._order

    def add_id(self) -> hex:
        id_ = self._id_gen.generate()
        self._order.id = id_

        return id_

    def add_side(self) -> OrderSide:
        side = self._side_gen.generate()
        self._order.side = side

        return side

    def add_instrument(self) -> OrderInstrument:
        instrument = self._instrument_gen.generate()
        self._order.instrument = instrument

        return instrument

    def add_status(self) -> OrderStatus:
        status = self._status_gen.generate()
        self._order.status = status

        return status

    def add_px_init(self, side: OrderSide, instrument: OrderInstrument) -> float:
        px = self._px_init_gen.generate(side, instrument)
        self._order.px_init = px

        return px

    def add_px_fill(self, px_init: float, status: OrderStatus) -> float:
        px = self._px_fill_gen.generate(px_init) if status != OrderStatus.CANCEL else 0
        self._order.px_fill = px

        return px

    def add_volume_init(self) -> int:
        volume = self._volume_init_gen.generate()
        self._order.volume_init = volume

        return volume

    def add_volume_fill(self, volume_init: int, status: OrderStatus) -> int:
        volume = self._volume_fill_gen.generate(volume_init, status) if status != OrderStatus.CANCEL else 0
        self._order.volume_fill = volume

        return volume

    def add_date(self) -> datetime:
        date = self._date_gen.generate()
        self._order.date = date

        return date

    def add_note(self) -> OrderNote:
        note = self._note_gen.generate()
        self._order.note = note

        return note

    def add_tags(self) -> List[OrderTag]:
        tags = self._tags_gen.generate()
        self._order.tags = tags

        return tags

    def build(self) -> FiatOrder:
        self._order = FiatOrder()

        id_ = self.add_id()
        side = self.add_side()
        instrument = self.add_instrument()
        status = self.add_status()
        px_init = self.add_px_init(side, instrument)
        self.add_px_fill(px_init, status)
        volume_init = self.add_volume_init()
        self.add_volume_fill(volume_init, status)
        self.add_note()
        self.add_tags()
        self.add_date()

        logger.info(f'Build new order with {id_} id')

        return self._order
