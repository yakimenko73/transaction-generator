from abc import abstractmethod, ABC
from pathlib import Path
from typing import List, Optional

from dataclass_csv import DataclassWriter
from typing.io import IO

from .domain.domain import Order


class InMemoryStorage(ABC):
    @abstractmethod
    def add(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_all(self) -> List[Order]:
        pass

    @abstractmethod
    def find_by_id(self, id_: hex) -> Order:
        pass


class FileStorage(ABC):
    @abstractmethod
    def write(self, orders: List[Order]) -> None:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @staticmethod
    def create_path(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)


class ArrayStorage(InMemoryStorage):
    def __init__(self):
        self._orders = []

    def add(self, order: Order) -> Order:
        self._orders.append(order)

        return order

    def find_all(self) -> List[Order]:
        return self._orders

    def find_by_id(self, id_: hex) -> Optional[Order]:
        return next(filter(lambda order: order.id == id_, self._orders), None)


class CsvFileStorage(FileStorage):
    def __init__(self, path: str):
        self._path = Path(path)
        self.create_path(self._path.parent)
        self._file: IO

    def __enter__(self):
        self._file = open(self._path, 'w')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    def write(self, orders: List[Order]) -> None:
        writer = DataclassWriter(self._file, orders, type(next(iter(orders), None)))
        writer.write()

    def size(self) -> int:
        return self._path.stat().st_size
