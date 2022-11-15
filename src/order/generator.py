from __future__ import annotations

import datetime as dt
import math
from abc import ABC, abstractmethod

import numpy as np

from src.config.generator_config import *


class Generator(ABC):
    @abstractmethod
    def generate(self):
        pass


class IdGenerator(Generator):
    def __init__(self, config: IdGeneratorConfig):
        self._modulus = config.modulus
        self._multiplier = config.multiplier
        self._increment = config.increment
        self._seed = config.seed

    def generate(self) -> int:
        self._seed = (self._multiplier * self._seed + self._increment) % self._modulus

        return self._seed


class SideGenerator(Generator):
    def __init__(self, config: SideGeneratorConfig):
        self._modulus = config.modulus
        self._multiplier = config.multiplier
        self._increment = config.increment

    def generate(self, seed: int) -> str:
        self._seed = (self._multiplier * self._seed + self._increment) % self._modulus

        return SIDES[0] if seed <= 50 else SIDES[1]


class InstrumentGenerator(Generator):
    def __init__(self, m: int, a: int, c: int) -> None:
        self._id_generator = IdGenerator(*CONFIG["IDSettings"].values())

        self._modulus = config.modulus
        self._multiplier = config.multiplier
        self._increment = config.increment

    def generate_value(self, seed: IdGenerator = None) -> str:
        self._seed = seed if seed else self._id_generator.generate_value()

        self._seed = (self._multiplier * self._seed + self._increment) % self._modulus
        try:
            value = INSTRUMENTS[self._seed - 1][0]
        except IndexError as ex:
            value = INSTRUMENTS[10][0]

        return value


class StatusGenerator(Generator):
    def __init__(self, m: int, a: int, c: int) -> None:
        self._id_generator = IdGenerator(*CONFIG["IDSettings"].values())

        self._modulus = config.modulus
        self._multiplier = config.multiplier
        self._increment = config.increment

    def generate_value(self, seed: IdGenerator = None) -> str:
        self._seed = seed if seed else self._id_generator.generate_value()

        self._seed = (self._multiplier * self._seed + self._increment) % self._modulus
        if self._seed <= 100:
            value = STATUSES[2][0]
        elif self._seed >= 101 and self._seed <= 200:
            value = STATUSES[2][1]
        else:
            value = STATUSES[2][2]

        return value


class PXInitGenerator(Generator):
    def __init__(self) -> None:
        self._side_generator = SideGenerator(*CONFIG["SideSettings"].values())
        self._instrument_generator = InstrumentGenerator(*CONFIG["InstrumentSettings"].values())

        self._side_sell = SIDES[0]
        self._side_buy = SIDES[1]

    def generate_value(self, side: SideGenerator = None, instrument: InstrumentGenerator = None) -> float:
        self.side = side if side else self._side_generator.generate_value()
        self.instrument = instrument if instrument else self._instrument_generator.generate_value()

        for index, instrument in enumerate(INSTRUMENTS):
            if self.instrument == instrument[0]:
                price_buy = instrument[1]
                price_sell = instrument[2]
                return price_buy if self.side == self._side_buy else price_sell


class PXFillGenerator(Generator):
    def __init__(self, m: float, a: float, c: float) -> None:
        self._id_generator = IdGenerator(*CONFIG["IDSettings"].values())
        self._price_generator = PXInitGenerator()
        self._status_generator = StatusGenerator(*CONFIG["StatusSettings"].values())

        self._status_cancel = STATUSES[2][2]
        self._modulus = config.modulus
        self._multiplier = config.multiplier
        self._increment = config.increment

    def generate_value(self, seed: IdGenerator = None, price: PXInitGenerator = None,
                       status: StatusGenerator = None) -> float:
        self._seed = seed if seed else self._id_generator.generate_value()
        self.price = price if price else self._price_generator.generate_value()
        self.status = status if status else self._status_generator.generate_value()

        self._seed = round((self._multiplier * self._seed + self._increment) % self._modulus, 5)

        if self.status == self._status_cancel:
            return 0
        else:
            return round(self.price + self._seed if self._seed < 0.0005 else self.price - self._seed, 5)


class VolumeInitGenerator(Generator):
    def __init__(self, m: int, a: int, c: int, seed: int) -> None:
        self._modulus = config.modulus
        self._multiplier = config.multiplier
        self._increment = config.increment
        self._seed = seed

    def generate_value(self) -> int:
        rounding_number = 1000
        self._seed = (self._multiplier * int(str(self._seed), 16) + self._increment) % self._modulus
        self._seed = math.ceil(self._seed / rounding_number) * rounding_number - rounding_number

        return self._seed


class VolumeFillGenerator(Generator):
    def __init__(self, a: int, c: int) -> None:
        self._id_generator = IdGenerator(*CONFIG["IDSettings"].values())
        self._status_generator = StatusGenerator(*CONFIG["StatusSettings"].values())
        self._volume_generator = VolumeInitGenerator(*CONFIG["VolumeInitSettings"].values())

        self._status_partialfill = STATUSES[2][1]
        self._status_cancel = STATUSES[2][2]
        self._multiplier = config.multiplier
        self._increment = config.increment

    def generate_value(self, seed: IdGenerator = None, status: StatusGenerator = None,
                       volume: VolumeInitGenerator = None) -> int:
        self._seed = seed if seed else self._id_generator.generate_value()
        self.status = status if status else self._status_generator.generate_value()
        self.volume = volume if volume else self._volume_generator.generate_value()

        rounding_number = 1000
        self._seed = (self._multiplier * self._seed + self._increment) % self.volume
        self._seed = math.ceil(self._seed / rounding_number) * rounding_number - rounding_number

        if self.status == self._status_partialfill:
            return self.volume - self._seed
        else:
            return 0 if self.status == self._status_cancel else self.volume


class DateGenerator(Generator):
    def __init__(self, m: int, a: int, c: int, seed: int, start_date: str) -> None:
        self._modulus = config.modulus
        self._multiplier = config.multiplier
        self._increment = config.increment
        self._seed = seed
        self.start_date = start_date

    def generate_value(self) -> str:
        date = dt.datetime.strptime(self.start_date, DATE_FORMAT_FOR_DATE_ATTRIBUTE)

        self._seed = (self._multiplier * self._seed + self._increment) % self._modulus
        increment_in_seconds = str(self._seed)[0]
        increment_in_milliseconds = f"{int(self._seed)}".zfill(3)

        date += dt.timedelta(seconds=int(increment_in_seconds))
        date = date.strftime(DATE_FORMAT_FOR_DATE_ATTRIBUTE) + f".{increment_in_milliseconds}"

        self.start_date = date[:-4]  # date without milliseconds

        return date


class NoteGenerator(Generator):
    def __init__(self, m: int, a: int, c: int) -> None:
        self._id_generator = IdGenerator(*CONFIG["IDSettings"].values())

        self._modulus = config.modulus
        self._multiplier = config.multiplier
        self._increment = config.increment

    def generate_value(self, seed: IdGenerator = None) -> str:
        self._seed = seed if seed else self._id_generator.generate_value()

        self._seed = (self._multiplier * self._seed + self._increment) % self._modulus
        try:
            value = NOTES[self._seed - 1]
        except IndexError:
            value = NOTES[10]

        return value


class TagGenerator(Generator):
    def __init__(self, n_m: int, n_a: int, n_c: int, t_m: int, t_a: int, t_c: int, seed: int) -> None:
        self.number_m = n_m
        self.number_a = n_a
        self.number_c = n_c
        self.tag_m = t_m
        self.tag_a = t_a
        self.tag_c = t_c
        self._seed = seed
        self.tags_kit = self._generate_tags_matrix(self._seed)

    def generate_value(self) -> str:
        self._seed = (self.number_a * self._seed + self.number_c) % self.number_m

        return ', '.join([tag for tag in self.tags_kit[self._seed] if tag])

    def _generate_tags_matrix(self, seed):
        matrix_tags = np.zeros((NUMBER_OF_DIFFERENT_TAGS_SETS, len(TAGS))).astype("str")

        for row in range(NUMBER_OF_DIFFERENT_TAGS_SETS):
            for column in range(len(TAGS)):
                seed = (self.tag_a * seed + self.tag_c) % self.tag_m

                matrix_tags[row][column] = TAGS[column] if seed % 2 else ''

        return matrix_tags
