from __future__ import annotations
from dataclasses import dataclass

import os
import re
import csv
import datetime as dt
import logging
import configparser

from abc import ABC, abstractmethod, abstractproperty

from constants import * 
from generators import * 


def setup():
	parameters_set = config_setup()
	logging_setup(
		parameters_set["Path"]["path_to_log"], 
		*parameters_set["LoggingSettings"].values(),
	)

	return parameters_set


def config_setup():
	path_to_config = 'settings/config.ini'
	config = configparser.ConfigParser()
	config.read(path_to_config)

	parameters_set = {}

	try:
		for section in config:
			if section != "DEFAULT":
				parameters_set[section] = {}
			for field in config[section]:
				if section == "LoggingSettings":
					parameters_set[section][field] = config[section][field].lower()

				elif section == "DateSettings" or section == "PXFillSettings":
					if field == "start_date":
						dt.datetime.strptime(config[section][field], DATE_FORMAT_FOR_DATE_ATTRIBUTE)
						parameters_set[section][field] = config[section][field]
					else:
						parameters_set[section][field] = float(config[section][field])

				elif section == "Path":
					parameters_set[section][field] = config[section][field]
				else:
					parameters_set[section][field] = int(config[section][field])
		if not parameters_set:
			raise FileNotFoundError("Config file not found")
	except (ValueError, FileNotFoundError, ) as ex:
		print("Incorrect parameters in the config file or the file is missing at all. " +
			f"Path: {path_to_config}. Ex: {ex}")

		os._exit(0)

	return parameters_set


def logging_setup(path_to_log, log_level, log_filemode):
	if not log_level in TRUE_LOG_LEVELS:
		log_level = 'DEBUG'

	if not log_filemode in TRUE_FILE_MODES:
		log_filemode = 'a'

	path = create_file_path(path_to_log)

	logging.basicConfig(filename=path, 
		level=log_level,
		filemode=log_filemode, 
		format=MESSAGE_FORMAT_FOR_LOGGER,
		datefmt=DATE_FORMAT_FOR_LOGGER)


def create_file_path(path):
	pathdir = ''.join(re.findall(r"\w+/", path))
	if pathdir:
		if not os.path.exists(pathdir):
			try:
				os.makedirs(pathdir)
			except OSError as ex:
				logging.warning("Failed to create file in the selected path. " +
					f"Created a file in the executing directory. Path: {path}. Ex: {ex}")
				path = os.path.basename(path)
	return path


class RecordFactoryInterface(ABC):
	@abstractmethod
	def create_list_records(self) -> list:
		pass


class RecordBuilderInterface(ABC):
	@abstractproperty
	def record(self) -> None:
		pass

	@abstractmethod
	def produce_id(self) -> list:
		pass

	@abstractmethod
	def produce_sides(self) -> list:
		pass

	@abstractmethod
	def produce_instruments(self) -> list:
		pass

	@abstractmethod
	def produce_statuses(self) -> list:
		pass

	@abstractmethod
	def produce_pxinit(self) -> list:
		pass

	@abstractmethod
	def produce_pxfill(self) -> list:
		pass

	@abstractmethod
	def produce_volumeinit(self) -> list:
		pass

	@abstractmethod
	def produce_volumefill(self) -> list:
		pass

	@abstractmethod
	def produce_dates(self) -> list:
		pass

	@abstractmethod
	def produce_notes(self) -> list:
		pass

	@abstractmethod
	def produce_tags(self) -> list:
		pass

	@abstractmethod
	def collect_record(self) -> list:
		pass


class RecordFactory(RecordFactoryInterface):
	def __init__(self) -> None:
		self._builder = RecordBuilder()

	@property
	def builder(self) -> RecordBuilder:
		return self._builder

	@builder.setter
	def builder(self, builder: RecordBuilder) -> None:
		self._builder = builder

	def create_list_records(self) -> None:
		self._builder.produce_id()
		self._builder.produce_sides()
		self._builder.produce_instruments()
		self._builder.produce_statuses()
		self._builder.produce_pxinit()
		self._builder.produce_pxfill()
		self._builder.produce_volumeinit()
		self._builder.produce_volumefill()
		self._builder.produce_notes()
		self._builder.produce_tags()
		self._builder.produce_dates()
		self._builder.collect_record()


class RecordBuilder(RecordBuilderInterface):
	def __init__(self):
		self._record_attributes = {}

	@property
	def record(self) -> RecordDTO:
		record = RecordDTO()
		return record

	def produce_id(self):
		logging.info('Generating the "id" attribute')
		id_obj = IdGenerator(4294967296, 65539, 0, 1)
		id_ = id_obj.generate_array()
		self._record_attributes["ID"] = id_

		return id_

	def produce_sides(self):
		try:
			id_ = self._record_attributes["ID"]
		except KeyError as ex:
			logging.warning('Unable to generate "side" attribute because "id" attribute was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["ID"] = id_

		logging.info('Generating the "side" attribute')
		side_obj = SideGenerator(100, 1, 3, id_)
		sides = side_obj.generate_array()
		self._record_attributes["SIDE"] = sides

		return sides

	def produce_instruments(self):
		try:
			id_ = self._record_attributes["ID"]
		except KeyError as ex:
			logging.warning('Unable to generate "instrument" attribute because "id" attribute was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["ID"] = id_

		logging.info('Generating the "instrument" attribute')
		instrument_obj = InstrumentGenerator(13, 1, 3, id_)
		instruments = instrument_obj.generate_array()
		self._record_attributes["INSTRUMENT"] = instruments

		return instruments

	def produce_statuses(self):
		try:
			id_ = self._record_attributes["ID"]
		except KeyError as ex:
			logging.warning('Unable to generate "status" attribute because "id" attribute was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["ID"] = id_

		logging.info('Generating the "status" attribute')
		status_obj = StatusGenerator(300, 7, 4, id_)
		statuses_on_broker = status_obj.generate_array()
		self._record_attributes["STATUS"] = statuses_on_broker

		return statuses_on_broker

	def produce_pxinit(self):
		try:
			instruments = self._record_attributes["INSTRUMENT"]
			sides = self._record_attributes["SIDE"]
		except KeyError as ex:
			logging.warning('Unable to generate "px_init" attribute because "instrument" or "side" attributes was not generated')

			logging.info('Forced generation of the "instrument" attribute')
			instruments = self.produce_instruments()
			self._record_attributes["INSTRUMENT"] = instruments

			logging.info('Forced generation of the "side" attribute')
			sides = self.produce_sides()
			self._record_attributes["SIDE"] = sides

		logging.info('Generating the "px_init" attribute')
		pxinit_obj = PXInitGenerator(instruments, sides)
		init_prices = pxinit_obj.generate_array()
		self._record_attributes["PX_INIT"] = init_prices

		return init_prices

	def produce_pxfill(self):
		try:
			id_ = self._record_attributes["ID"]
			statuses_on_broker = self._record_attributes["STATUS"]
			init_prices = self._record_attributes["PX_INIT"]
		except KeyError as ex:
			logging.warning('Unable to generate "px_fill" attribute because "id", "px_init" or "status" attributes was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["ID"] = id_

			logging.info('Forced generation of the "status" attribute')
			statuses_on_broker = self.produce_statuses()
			self._record_attributes["STATUS"] = statuses_on_broker

			logging.info('Forced generation of the "px_init" attribute')
			init_prices = self.produce_pxinit()
			self._record_attributes["PX_INIT"] = init_prices

		logging.info('Generating the "px_fill" attribute')
		pxfill_obj = PXFillGenerator(0.00101, 0.0002, 0.00032, id_, init_prices, statuses_on_broker)
		fill_prices = pxfill_obj.generate_array()
		self._record_attributes["PX_FILL"] = fill_prices

		return fill_prices

	def produce_volumeinit(self):
		logging.info('Generating the "volume_init" attribute')
		init_volumes_obj = VolumeInitGenerator(1000000, 1000, 4432423, 1)
		init_volumes = init_volumes_obj.generate_array()
		self._record_attributes["VOLUME_INIT"] = init_volumes

		return init_volumes

	def produce_volumefill(self):
		try:
			id_ = self._record_attributes["ID"]
			statuses_on_broker = self._record_attributes["STATUS"]
			init_volumes = self._record_attributes["VOLUME_INIT"]
		except KeyError as ex:
			logging.warning('Unable to generate "volume_fill" attribute because "id", "status" or "volume_init" attributes was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["ID"] = id_

			logging.info('Forced generation of the "status" attribute')
			statuses_on_broker = self.produce_statuses()
			self._record_attributes["STATUS"] = statuses_on_broker

			logging.info('Forced generation of the "volume_init" attribute')
			init_volumes = self.produce_volumeinit()
			self._record_attributes["VOLUME_INIT"] = init_volumes

		logging.info('Generating the "volume_fill" attribute')
		fill_volumes_obj = VolumeFillGenerator(1000, 4432423, id_, statuses_on_broker, init_volumes)
		fill_volumes = fill_volumes_obj.generate_array()
		self._record_attributes["VOLUME_FILL"] = fill_volumes

		return fill_volumes

	def produce_dates(self):
		logging.info('Generating the "date" attribute')
		date_obj = DateGenerator(1000, 12, 7, 1, '01.02.2021  0:00:00')
		dates = date_obj.generate_array()
		self._record_attributes["DATE"] = dates

		return dates

	def produce_notes(self):
		try:
			id_ = self._record_attributes["ID"]
		except KeyError as ex:
			logging.warning('Unable to generate "note" attribute because "id" attribute was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["ID"] = id_


		logging.info('Generating the "note" attribute')
		note_obj = NoteGenerator(13, 1, 3, id_)
		notes = note_obj.generate_array()
		self._record_attributes["NOTE"] = notes

		return notes

	def produce_tags(self):
		logging.info('Generating the "tags" attribute')
		tag_obj = TagGenerator(13, 1, 3, 423543, 1000, 43232, 1)
		tags = tag_obj.generate_array()
		self._record_attributes["TAGS"] = tags

		return tags

	def collect_record(self):
		for order_number in range(MAX_NUMBER_ORDERS):
			record_items = self.define_order_items(order_number)
			number_of_records, is_first_segment = self.define_number_of_records_for_order(order_number)
			for record_number in range(number_of_records):
				record_clear_items = {}
				for key in ORDER_ATTRIBUTES:
					try:
						if key == "DATE":
							record_clear_items[key] = record_items[key][record_number]
						else:
							record_clear_items[key] = record_items[key]
					except KeyError as ex:
						record_clear_items[key] = "NULL"

				try:
					if is_first_segment:
						if record_number == 1:
							record_clear_items["STATUS"] = record_items["STATUS"]
						else:
							record_clear_items["STATUS"] = STATUSES[record_number+1]
					elif record_number == 2:
						record_clear_items["STATUS"] = record_items["STATUS"]
					else:
						record_clear_items["STATUS"] = STATUSES[record_number]

					if record_clear_items["STATUS"] == STATUSES[0] or record_clear_items["STATUS"] == STATUSES[1]:
						record_clear_items["VOLUME_FILL"] = 0
						record_clear_items["PX_FILL"] = 0
					else:
						record_clear_items["VOLUME_FILL"] = record_items["VOLUME_FILL"]
						record_clear_items["PX_FILL"] = record_items["PX_FILL"]
				except KeyError as ex:
					pass

				record = RecordDTO(*record_clear_items.values())

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


	def define_order_items(self, order_number):
		order_items = {}
		for number_attribute, attribute_name in enumerate(self._record_attributes.keys()):
			order_items[attribute_name] = self._record_attributes[attribute_name][order_number]

		return order_items


@dataclass
class RecordDTO:
	id_: int  = "NULL"
	side: str = "NULL"
	instrument: str = "NULL"
	status: str = "NULL"
	px_init: float = "NULL"
	px_fill: float = "NULL"
	volume_init: int = "NULL"
	volume_fill: int = "NULL"
	note: str = "NULL"
	tags: str = "NULL"
	date: date = "NULL"


class RecordMapper:
	def __init__(self, *args, **kwargs):
		return 1


if __name__ == "__main__":
	parameters_set = setup()
	logging.debug("Config and logger setup was successful. " + 
		f"Number of sections from config: {len(parameters_set.keys())}")

	factory = RecordFactory()
	factory.create_list_records()
	
