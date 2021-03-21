from __future__ import annotations

import math
import datetime as dt
import numpy as np

from abc import ABC, abstractmethod, abstractproperty

from constants import *


class GeneratorInterface(ABC):
	@abstractmethod
	def generate_array(self) -> array:
		pass


class IdGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seed: int) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seed = seed

	def generate_array(self):
		list_id = []

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = (self.multiplier * self.seed + self.increment) % self.modulus

			list_id.append(hex(self.seed))

		return list_id


class SideGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seeds: IdGenerator) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seeds = seeds

	def generate_array(self):
		list_sides = []

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = (self.multiplier * int(self.seeds[order_number], 16) + self.increment) % self.modulus
			if self.seed <= 50:
				list_sides.append(SIDES[0])
			else:
				list_sides.append(SIDES[1])

		return list_sides


class InstrumentGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seeds: IdGenerator) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seeds = seeds

	def generate_array(self):
		list_instruments = []

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = (self.multiplier * int(self.seeds[order_number], 16) + self.increment) % self.modulus
			try:
				list_instruments.append(INSTRUMENTS[self.seed-1][0])
			except IndexError:
				list_instruments.append(INSTRUMENTS[10][0])

		return list_instruments


class StatusGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seeds: IdGenerator) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seeds = seeds

	def generate_array(self):
		list_statuses_on_broker = []

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = (self.multiplier * int(self.seeds[order_number], 16) + self.increment) % self.modulus
			if self.seed <= 100:
				list_statuses_on_broker.append(STATUSES[2][0])
			elif self.seed >= 101 and self.seed <= 200:
				list_statuses_on_broker.append(STATUSES[2][1])
			else:
				list_statuses_on_broker.append(STATUSES[2][2])

		return list_statuses_on_broker


class PXInitGenerator(GeneratorInterface):
	def __init__(self, instruments: InstrumentGenerator, sides: SideGenerator) -> None:
		self.instruments = instruments
		self.sides = sides

	def generate_array(self):
		list_prices = []

		for order_number in range(MAX_NUMBER_ORDERS):
			for j in range(len(INSTRUMENTS)):
				if INSTRUMENTS[j][0] == self.instruments[order_number]:
					if self.sides[order_number] == SIDES[1]:
						list_prices.append(INSTRUMENTS[j][1])
					else:
						list_prices.append(INSTRUMENTS[j][2])
		return list_prices


class PXFillGenerator(GeneratorInterface):
	def __init__(self, m: float, a: float, c: float, seeds: IdGenerator, prices: PXInitGenerator, statuses: StatusGenerator) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seeds = seeds
		self.init_prices = prices
		self.statuses_on_broker = statuses

	def generate_array(self):
		list_prices = []

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = round((self.multiplier * int(self.seeds[order_number], 16) + self.increment) % self.modulus, 5)
			if self.statuses_on_broker[order_number] == STATUSES[2][2]:
				fill_price = 0
			elif self.seed < 0.0005:
				fill_price = self.init_prices[order_number] + self.seed
			else:
				fill_price = self.init_prices[order_number] - self.seed

			list_prices.append(round(fill_price, 5))

		return list_prices


class VolumeInitGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seed: int) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seed = seed

	def generate_array(self):
		list_volumes = []
		rounding_number = 1000

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = (self.multiplier * int(str(self.seed), 16) + self.increment) % self.modulus
			self.seed = math.ceil(self.seed/rounding_number) * rounding_number - rounding_number

			list_volumes.append(self.seed)

		return list_volumes


class VolumeFillGenerator(GeneratorInterface):
	def __init__(self, a: int, c: int, seeds: IdGenerator, statuses: StatusGenerator, volumes: VolumeInitGenerator) -> None:
		self.multiplier = a
		self.increment = c
		self.seeds = seeds
		self.statuses_on_broker = statuses
		self.init_volumes = volumes

	def generate_array(self):
		list_volumes = []
		rounding_number = 1000

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = (self.multiplier * int(self.seeds[order_number], 16) + self.increment) % self.init_volumes[order_number]
			self.seed = math.ceil(self.seed/rounding_number) * rounding_number - rounding_number

			if self.statuses_on_broker[order_number] == STATUSES[2][1]:
				fill_volume = self.init_volumes[order_number] - self.seed
			elif self.statuses_on_broker[order_number] == STATUSES[2][2]:
				fill_volume = 0
			else:
				fill_volume = self.init_volumes[order_number]

			list_volumes.append(fill_volume)

		return list_volumes


class DateGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seed: int, date: str) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seed = seed
		self.start_date = date

	def generate_array(self):
		date = dt.datetime.strptime(self.start_date, DATE_FORMAT_FOR_DATE_ATTRIBUTE)
		list_dates = []

		for order_number in range(MAX_NUMBER_ORDERS):
			dates_for_order = []
			number_of_dates, _ = self.define_number_of_records_for_order(order_number)

			for record_number in range(number_of_dates):
				self.seed = (self.multiplier * self.seed + self.increment) % self.modulus

				increment_in_seconds = str(self.seed)[0]
				increment_in_milliseconds = f"{int(self.seed)}".zfill(3)

				date = date + dt.timedelta(seconds=int(increment_in_seconds))

				dates_for_order.append(date.strftime(DATE_FORMAT_FOR_DATE_ATTRIBUTE) + f".{increment_in_milliseconds}")
			
			list_dates.append(dates_for_order)

		return list_dates

	def define_number_of_records_for_order(self, order_number):
		if order_number < MAX_LIMIT_ORDERS_FOR_FIRST_SEGMENT:
			number_of_records = NUMBER_OF_RECORDS_FOR_FIRST_SEGMENT
			is_first_segment = True
		elif order_number < MAX_LIMIT_ORDERS_FOR_SECOND_SEGMENT:
			number_of_records = NUMBER_OF_RECORDS_FOR_SECOND_SEGMENT
			is_first_segment = False
		else:
			number_of_records = NUMBER_OF_RECORDS_FOR_THIRD_SEGMENT
			is_first_segment = False

		return number_of_records, is_first_segment


class NoteGenerator(GeneratorInterface):
	def __init__(self, m: int, a: int, c: int, seeds: IdGenerator) -> None:
		self.modulus = m
		self.multiplier = a
		self.increment = c
		self.seeds = seeds

	def generate_array(self):
		list_notes = []

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = (self.multiplier * int(self.seeds[order_number], 16) + self.increment) % self.modulus
			try:
				list_notes.append(NOTES[self.seed-1])
			except IndexError:
				list_notes.append(NOTES[10])

		return list_notes


class TagGenerator(GeneratorInterface):
	def __init__(self, n_m: int, n_a: int, n_c: int, t_m: int, t_a: int, t_c: int, seed: int) -> None:
		self.number_m = n_m
		self.number_a = n_a
		self.number_c = n_c
		self.tag_m = t_m
		self.tag_a = t_a
		self.tag_c = t_c
		self.seed = seed

	def generate_array(self):
		list_tags = []
		tags_kit = self._generate_tags_matrix(self.seed)

		for order_number in range(MAX_NUMBER_ORDERS):
			self.seed = (self.number_a * self.seed + self.number_c) % self.number_m

			list_tags.append(', '.join([tag for tag in tags_kit[self.seed] if tag]))

		return list_tags

	def _generate_tags_matrix(self, seed):
		matrix_tags = np.zeros((NUMBER_OF_DIFFERENT_TAGS_SETS, len(TAGS))).astype("str")

		for row in range(NUMBER_OF_DIFFERENT_TAGS_SETS):
			for column in range(len(TAGS)):
				seed = (self.tag_a * seed + self.tag_c) % self.tag_m

				matrix_tags[row][column] = TAGS[column] if seed % 2 else ''

		return matrix_tags


if __name__ == "__main__":
	id_obj = IdGenerator(4294967296, 65539, 0, 1)
	id_ = id_obj.generate_array()

	side_obj = SideGenerator(100, 1, 3, id_)
	sides = side_obj.generate_array()

	instrument_obj = InstrumentGenerator(13, 1, 3, id_)
	instruments = instrument_obj.generate_array()

	status_obj = StatusGenerator(300, 7, 4, id_)
	statuses_on_broker = status_obj.generate_array()

	pxinit_obj = PXInitGenerator(instruments, sides)
	pxinit = pxinit_obj.generate_array()

	pxfill_obj = PXFillGenerator(0.00101, 0.0002, 0.00032, id_, pxinit, statuses_on_broker)
	pxfill = pxfill_obj.generate_array()

	volume_init_obj = VolumeInitGenerator(1000000, 1000, 4432423, 1)
	volume_init = volume_init_obj.generate_array()

	volume_fill_obj = VolumeFillGenerator(1000, 4432423, id_, statuses_on_broker, volume_init)
	volume_fill = volume_fill_obj.generate_array()

	date_obj = DateGenerator(1000, 12, 7, 1, '01.02.2021  0:00:00')
	dates = date_obj.generate_array()

	note_obj = NoteGenerator(13, 1, 3, id_)
	notes = note_obj.generate_array()

	tag_obj = TagGenerator(13, 1, 3, 423543, 1000, 43232, 1)
	tags = tag_obj.generate_array()