from __future__ import annotations

import math
import datetime as dt
import numpy as np

from abc import ABC, abstractmethod, abstractproperty

from constants import *


class GeneratorInterface(ABC):
	@abstractmethod
	def generate_value(self):
		pass


class IdGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seed: int) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seed = seed

	def generate_value(self) -> int:
		self.seed = (self.multiplier * self.seed + self.increment) % self.modulus

		return self.seed


class SideGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int) -> None:
		self._id_generator = IdGenerator(4294967296, 65539, 0, 1)

		self.modulus = m
		self.multiplier = a
		self.increment = c

	def generate_value(self, seed: IdGenerator=None) -> str:
		self.seed = seed if seed else self._id_generator.generate_value()

		self.seed = (self.multiplier * self.seed + self.increment) % self.modulus

		return SIDES[0] if self.seed <= 50 else SIDES[1]


class InstrumentGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int) -> None:
		self._id_generator = IdGenerator(4294967296, 65539, 0, 1)

		self.modulus = m
		self.multiplier = a
		self.increment = c

	def generate_value(self, seed: IdGenerator=None)  -> str:
		self.seed = seed if seed else self._id_generator.generate_value()

		self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
		try:
			value = INSTRUMENTS[self.seed-1][0]
		except IndexError as ex:
			value = INSTRUMENTS[10][0]

		return value


class StatusGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int) -> None:
		self._id_generator = IdGenerator(4294967296, 65539, 0, 1)

		self.modulus = m
		self.multiplier = a
		self.increment = c

	def generate_value(self, seed: IdGenerator=None) -> str:
		self.seed = seed if seed else self._id_generator.generate_value()

		self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
		if self.seed <= 100:
			value = STATUSES[2][0]
		elif self.seed >= 101 and self.seed <= 200:
			value = STATUSES[2][1]
		else:
			value = STATUSES[2][2]

		return value 


class PXInitGenerator(GeneratorInterface):
	def __init__(self) -> None:
		self._side_generator = SideGenerator(100, 1, 3)
		self._instrument_generator = InstrumentGenerator(13, 1, 3)

		self._side_sell = SIDES[0]
		self._side_buy = SIDES[1]

	def generate_value(self, side: SideGenerator=None, instrument: InstrumentGenerator=None) -> float:
		self.side = side if side else self._side_generator.generate_value()
		self.instrument = instrument if instrument else self._instrument_generator.generate_value()

		for index, instrument in enumerate(INSTRUMENTS):
			if self.instrument == instrument[0]:
				price_buy = instrument[1]
				price_sell = instrument[2]
				return price_buy if self.side == self._side_buy else price_sell


class PXFillGenerator(GeneratorInterface):
	def __init__(self, m: float, a: float, c: float) -> None:
		self._id_generator = IdGenerator(4294967296, 65539, 0, 1)
		self._price_generator = PXInitGenerator()
		self._status_generator = StatusGenerator(300, 7, 4)

		self._status_cancel = STATUSES[2][2]
		self.modulus = m
		self.multiplier = a
		self.increment = c

	def generate_value(self, seed: IdGenerator=None, price: PXInitGenerator=None, status: StatusGenerator=None) -> float:
		self.seed = seed if seed else self._id_generator.generate_value()
		self.price = price if price else self._price_generator.generate_value()
		self.status = status if status else self._status_generator.generate_value()

		self.seed = round((self.multiplier * self.seed + self.increment) % self.modulus, 5)

		if self.status == self._status_cancel:
			return 0
		else:
			return round(self.price + self.seed if self.seed < 0.0005 else self.price - self.seed, 5)


class VolumeInitGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seed: int) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seed = seed

	def generate_value(self) -> int:
		rounding_number = 1000
		self.seed = (self.multiplier * int(str(self.seed), 16) + self.increment) % self.modulus
		self.seed = math.ceil(self.seed/rounding_number) * rounding_number - rounding_number

		return self.seed


class VolumeFillGenerator(GeneratorInterface):
	def __init__(self, a: int, c: int) -> None:
		self._id_generator = IdGenerator(4294967296, 65539, 0, 1)
		self._status_generator = StatusGenerator(300, 7, 4)
		self._volume_generator = VolumeInitGenerator(1000000, 1000, 4432423, 1)

		self._status_partialfill = STATUSES[2][1]
		self._status_cancel = STATUSES[2][2]
		self.multiplier = a
		self.increment = c

	def generate_value(self, seed: IdGenerator=None, status: StatusGenerator=None, volume: VolumeInitGenerator=None) -> int:
		self.seed = seed if seed else self._id_generator.generate_value()
		self.status = status if status else self._status_generator.generate_value()
		self.volume = volume if volume else self._volume_generator.generate_value()

		rounding_number = 1000
		self.seed = (self.multiplier * self.seed + self.increment) % self.volume
		self.seed = math.ceil(self.seed/rounding_number) * rounding_number - rounding_number

		if self.status == self._status_partialfill:
			return self.volume - self.seed
		else:
			return 0 if self.status == self._status_cancel else self.volume


class DateGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seed: int, start_date: str) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seed = seed
		self.start_date = start_date

	def generate_value(self) -> str:
		date = dt.datetime.strptime(self.start_date, DATE_FORMAT_FOR_DATE_ATTRIBUTE)

		self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
		increment_in_seconds = str(self.seed)[0]
		increment_in_milliseconds = f"{int(self.seed)}".zfill(3)

		date += dt.timedelta(seconds=int(increment_in_seconds))
		date = date.strftime(DATE_FORMAT_FOR_DATE_ATTRIBUTE) + f".{increment_in_milliseconds}"

		self.start_date = date[:-4] # date without milliseconds

		return date


class NoteGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int) -> None:
		self._id_generator = IdGenerator(4294967296, 65539, 0, 1)

		self.modulus = m
		self.multiplier = a
		self.increment = c

	def generate_value(self, seed: IdGenerator=None) -> str:
		self.seed = seed if seed else self._id_generator.generate_value()

		self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
		try:
			value = NOTES[self.seed-1]
		except IndexError:
			value = NOTES[10]

		return value


class TagGenerator(GeneratorInterface):
	def __init__(self, n_m: int, n_a: int, n_c: int, t_m: int, t_a: int, t_c: int, seed: int) -> None:
		self.number_m = n_m
		self.number_a = n_a
		self.number_c = n_c
		self.tag_m = t_m
		self.tag_a = t_a
		self.tag_c = t_c
		self.seed = seed
		self.tags_kit = self._generate_tags_matrix(self.seed)

	def generate_value(self) -> str:
		self.seed = (self.number_a * self.seed + self.number_c) % self.number_m

		return self.seed, ', '.join([tag for tag in self.tags_kit[self.seed] if tag])

	def _generate_tags_matrix(self, seed):
		matrix_tags = np.zeros((NUMBER_OF_DIFFERENT_TAGS_SETS, len(TAGS))).astype("str")

		for row in range(NUMBER_OF_DIFFERENT_TAGS_SETS):
			for column in range(len(TAGS)):
				seed = (self.tag_a * seed + self.tag_c) % self.tag_m

				matrix_tags[row][column] = TAGS[column] if seed % 2 else ''

		return matrix_tags