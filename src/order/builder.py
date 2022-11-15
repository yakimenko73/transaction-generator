from abc import abstractmethod, ABC

from .domain.domain import Order, FiatOrder
from ..config.config import Config


class OrderBuilder(ABC):
    @abstractmethod
    def build_order(self) -> Order:
        pass

    @abstractmethod
    def produce_id(self) -> hex:
        pass

    @abstractmethod
    def produce_side(self) -> str:
        pass

    @abstractmethod
    def produce_instrument(self) -> str:
        pass

    @abstractmethod
    def produce_status(self) -> str:
        pass

    @abstractmethod
    def produce_px_init(self) -> float:
        pass

    @abstractmethod
    def produce_px_fill(self) -> float:
        pass

    @abstractmethod
    def produce_volume_init(self) -> int:
        pass

    @abstractmethod
    def produce_volume_fill(self) -> int:
        pass

    @abstractmethod
    def produce_date(self) -> str:
        pass

    @abstractmethod
    def produce_note(self) -> str:
        pass

    @abstractmethod
    def produce_tags(self) -> str:
        pass


class PseudoRandomFiatOrderBuilder(OrderBuilder):
    def __init__(self, config: Config):
        self.id_obj = IdGenerator(*config["IDSettings"].values())
        self.side_obj = SideGenerator(*config["SideSettings"].values())
        self.instrument_obj = InstrumentGenerator(*config["InstrumentSettings"].values())
        self.status_obj = StatusGenerator(*config["StatusSettings"].values())
        self.pxinit_obj = PXInitGenerator()
        self.pxfill_obj = PXFillGenerator(*config["PXFillSettings"].values())
        self.volume_init_obj = VolumeInitGenerator(*config["VolumeInitSettings"].values())
        self.volume_fill_obj = VolumeFillGenerator(*config["VolumeFillSettings"].values())
        self.date_obj = DateGenerator(*config["DateSettings"].values())
        self.note_obj = NoteGenerator(*config["NoteSettings"].values())
        self.tag_obj = TagGenerator(*config["TagSettings"].values())

    def build_order(self) -> FiatOrder:
        pass

    def produce_id(self) -> hex:
        pass

    def produce_side(self) -> str:
        pass

    def produce_instrument(self) -> str:
        pass

    def produce_status(self) -> str:
        pass

    def produce_px_init(self) -> float:
        pass

    def produce_px_fill(self) -> float:
        pass

    def produce_volume_init(self) -> int:
        pass

    def produce_volume_fill(self) -> int:
        pass

    def produce_date(self) -> str:
        pass

    def produce_note(self) -> str:
        pass

    def produce_tags(self) -> str:
        pass
