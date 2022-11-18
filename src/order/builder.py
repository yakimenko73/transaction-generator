from src.config import Config
from .domain.domain import FiatOrder
from .generators import *


class OrderBuilder(ABC):
    @abstractmethod
    def produce_id(self) -> hex:
        pass

    @abstractmethod
    def produce_side(self) -> OrderSide:
        pass

    @abstractmethod
    def produce_instrument(self) -> OrderInstrument:
        pass

    @abstractmethod
    def produce_status(self) -> OrderStatus:
        pass

    @abstractmethod
    def produce_px_init(self, side: OrderSide, instrument: OrderInstrument) -> float:
        pass

    @abstractmethod
    def produce_px_fill(self, px_init: float) -> float:
        pass

    @abstractmethod
    def produce_volume_init(self) -> int:
        pass

    @abstractmethod
    def produce_volume_fill(self, volume_init: int, status: OrderStatus) -> int:
        pass

    @abstractmethod
    def produce_date(self) -> datetime:
        pass

    @abstractmethod
    def produce_note(self) -> OrderNote:
        pass

    @abstractmethod
    def produce_tags(self) -> List[OrderTag]:
        pass


class PseudoRandomFiatOrderBuilder(OrderBuilder):
    def __init__(self, config: Config):
        self._order = FiatOrder()
        self._id_gen = IdGenerator(config.generators.id_generator)
        self._side_gen = SideGenerator()
        self._instrument_gen = InstrumentGenerator()
        self._status_gen = StatusGenerator()
        self._px_init_gen = PXInitGenerator()
        self._px_fill_gen = PXFillGenerator(config.generators.px_fill_generator)
        self._volume_init_gen = VolumeInitGenerator(config.generators.volume_init_generator)
        self._volume_fill_gen = VolumeFillGenerator(config.generators.volume_init_generator)
        self._date_gen = DateGenerator(config.generators.date_generator)
        self._note_gen = NoteGenerator()
        self._tags_gen = TagsGenerator()

    @property
    def order(self) -> FiatOrder:
        return self._order

    def produce_id(self) -> hex:
        id_ = self._id_gen.generate()
        self._order.id = id_

        return id_

    def produce_side(self) -> OrderSide:
        side = self._side_gen.generate()
        self._order.side = side

        return side

    def produce_instrument(self) -> OrderInstrument:
        instrument = self._instrument_gen.generate()
        self._order.instrument = instrument

        return instrument

    def produce_status(self) -> OrderStatus:
        status = self._status_gen.generate()
        self._order.status = status

        return status

    def produce_px_init(self, side: OrderSide, instrument: OrderInstrument) -> float:
        px = self._px_init_gen.generate(side, instrument)
        self._order.px_init = px

        return px

    def produce_px_fill(self, px_init: float) -> float:
        px = self._px_fill_gen.generate(px_init)
        self._order.px_fill = px

        return px

    def produce_volume_init(self) -> int:
        volume = self._volume_init_gen.generate()
        self._order.volume_init = volume

        return volume

    def produce_volume_fill(self, volume_init: int, status: OrderStatus) -> int:
        volume = self._volume_fill_gen.generate(volume_init, status)
        self._order.volume_fill = volume

        return volume

    def produce_date(self) -> datetime:
        date = self._date_gen.generate()
        self._order.date = date

        return date

    def produce_note(self) -> OrderNote:
        note = self._note_gen.generate()
        self._order.note = note

        return note

    def produce_tags(self) -> List[OrderTag]:
        tags = self._tags_gen.generate()
        self._order.tags = tags

        return tags
