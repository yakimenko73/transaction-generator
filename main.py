from __future__ import annotations

import datetime as dt
import csv
import logging
import configparser

from dataclasses import dataclass

from constants import * 
from generators import * 
from interfaces import *
from utils import Singleton, create_file_path
from storage import RecordRepository, ArrayStorage, MySQLStorage


class RecordFactory(RecordFactoryInterface):
	def __init__(self, config: dict) -> None:
		self._builder = RecordBuilder(config)

	@property
	def builder(self) -> RecordBuilder:
		return self._builder

	@builder.setter
	def builder(self, builder: RecordBuilder) -> None:
		self._builder = builder

	def create_history_record(self) -> None:
		self._builder.produce_id()
		self._builder.produce_side()
		self._builder.produce_instrument()
		self._builder.produce_status()
		self._builder.produce_pxinit()
		self._builder.produce_pxfill()
		self._builder.produce_volumeinit()
		self._builder.produce_volumefill()
		self._builder.produce_note()
		self._builder.produce_tags()
		self._builder.produce_date()

		record = self._builder.collect_record()

		return record


class RecordBuilder(RecordBuilderInterface):
	def __init__(self, config):
		self._total_record_counter = 1
		self._record_attributes = {}
		self.record_model = RecordModel()

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

	def produce_id(self):
		if self._is_a_new_order_record("ID"):
			id_ = self.id_obj.generate_value()
			self._record_attributes["ID"] = id_

	def produce_side(self):
		if self._is_a_new_order_record("SIDE"):
			side = self.side_obj.generate_value()
			self._record_attributes["SIDE"] = side

	def produce_instrument(self):
		if self._is_a_new_order_record("INSTRUMENT"):
			instrument = self.instrument_obj.generate_value()
			self._record_attributes["INSTRUMENT"] = instrument

	def produce_status(self):
		if self._is_a_new_order_record("STATUS"):
			status_on_broker = self.status_obj.generate_value()
			self._record_attributes["STATUS"] = status_on_broker

	def produce_pxinit(self):
		if self._is_a_new_order_record("PX_INIT"):
			init_price = self.pxinit_obj.generate_value()
			self._record_attributes["PX_INIT"] = init_price

	def produce_pxfill(self):
		if self._is_a_new_order_record("PX_FILL"):
			fill_price = self.pxfill_obj.generate_value()
			self._record_attributes["PX_FILL"] = fill_price

	def produce_volumeinit(self):
		if self._is_a_new_order_record("VOLUME_INIT"):
			init_volume = self.volume_init_obj.generate_value()
			self._record_attributes["VOLUME_INIT"] = init_volume

	def produce_volumefill(self):
		if self._is_a_new_order_record("VOLUME_FILL"):
			fill_volume = self.volume_fill_obj.generate_value()
			self._record_attributes["VOLUME_FILL"] = fill_volume

	def produce_date(self):
		date = self.date_obj.generate_value()
		self._record_attributes["DATE"] = date

	def produce_note(self):
		if self._is_a_new_order_record("NOTE"):
			note = self.note_obj.generate_value()
			self._record_attributes["NOTE"] = note

	def produce_tags(self):
		if self._is_a_new_order_record("TAGS"):
			tags = self.tag_obj.generate_value()
			self._record_attributes["TAGS"] = tags

	def collect_record(self):
		self._total_record_counter += 1

		self.record_model.record = self._record_attributes
		self.record_model.parameter_mapping()
		self.record_model.convert_history_record_to_order_record()

		record = RecordDTO(*self.record_model.record.values())

		return record

	def _is_a_new_order_record(self, attribute_name, record_counters={}):
		try:
			record_counters[attribute_name] += 1
		except KeyError as ex:
			record_counters[attribute_name] = 1

		number_of_records_for_order = self._define_number_of_records_for_order()
		if record_counters[attribute_name] == 1:
			return True
		elif record_counters[attribute_name] == number_of_records_for_order:
			record_counters[attribute_name] = 0
			return False

	def _define_number_of_records_for_order(self):
		if self._total_record_counter <= MAX_LIMIT_RECORDS_FOR_FIRST_SEGMENT:
			number_of_records = NUMBER_OF_RECORDS_FOR_FIRST_SEGMENT
			is_first_segment = True
		elif self._total_record_counter <= MAX_LIMIT_RECORDS_FOR_SECOND_SEGMENT:
			number_of_records = NUMBER_OF_RECORDS_FOR_SECOND_SEGMENT
			is_first_segment = False
		else:
			number_of_records = NUMBER_OF_RECORDS_FOR_THIRD_SEGMENT
			is_first_segment = False

		return number_of_records


@dataclass
class RecordDTO:
	id_: hex  = 0
	side: str = "NULL"
	instrument: str = "NULL"
	status: str = "NULL"
	px_init: float = 0.0
	px_fill: float = 0.0
	volume_init: int = 0
	volume_fill: int = 0
	note: str = "NULL"
	tags: str = "NULL"
	date: str = "NULL"


class RecordModel:
	def __init__(self):
		self._total_record_counter = 0
		self._record_number = -1

	@property
	def record(self):
		return self._record

	@record.setter
	def record(self, record: dict):
		self._record = record

	def parameter_mapping(self):
		mapped_record = {}
		for key in ORDER_ATTRIBUTES:
			try:
				mapped_record[key] = hex(self._record[key]) if key == "ID" else self._record[key]
			except KeyError as ex:
				mapped_record[key] = "NULL"
		self._record = mapped_record

	def convert_history_record_to_order_record(self):
		self._total_record_counter += 1
		self._record_number += 1
		number_of_records_for_order, is_first_segment = self._define_number_of_records_for_order()
		
		if is_first_segment:
			self._record["STATUS"] = self._record["STATUS"] if self._record_number == 1 else STATUSES[self._record_number+1]
		else:
			self._record["STATUS"] = self._record["STATUS"] if self._record_number == 2 else STATUSES[self._record_number]

		self._record["VOLUME_FILL"] = 0 if self._record["STATUS"] in STATUSES[:2] else self._record["VOLUME_FILL"]
		self._record["PX_FILL"] = 0 if self._record["STATUS"] in STATUSES[:2] else self._record["PX_FILL"]

		if self._record_number == number_of_records_for_order-1:
			self._record_number = -1

	def _define_number_of_records_for_order(self):
		if self._total_record_counter <= MAX_LIMIT_RECORDS_FOR_FIRST_SEGMENT:
			number_of_records = NUMBER_OF_RECORDS_FOR_FIRST_SEGMENT
			is_first_segment = True
		elif self._total_record_counter <= MAX_LIMIT_RECORDS_FOR_SECOND_SEGMENT:
			number_of_records = NUMBER_OF_RECORDS_FOR_SECOND_SEGMENT
			is_first_segment = False
		else:
			number_of_records = NUMBER_OF_RECORDS_FOR_THIRD_SEGMENT
			is_first_segment = False

		return number_of_records, is_first_segment


class Config(metaclass=Singleton):
	def __init__(self):
		self._path_to_config = 'settings/config.ini'
		self.parameters_set = {}

	def setup(self):
		config = configparser.ConfigParser()
		config.read(self._path_to_config)
		self.parameters_set = {}

		try:
			for section in config:
				if section != "DEFAULT":
					self.parameters_set[section] = {}
				for field in config[section]:
					if section == "LoggingSettings":
						self.parameters_set[section][field] = config[section][field].lower()

					elif section in ("DateSettings", "PXFillSettings", ):
						if field == "start_date":
							dt.datetime.strptime(config[section][field], DATE_FORMAT_FOR_DATE_ATTRIBUTE)
							self.parameters_set[section][field] = config[section][field]
						else:
							self.parameters_set[section][field] = float(config[section][field])

					elif section in ("Path", "MySQLSettings", ):
						self.parameters_set[section][field] = config[section][field]
					else:
						self.parameters_set[section][field] = int(config[section][field])
			if not self.parameters_set:
				raise FileNotFoundError("Config file not found")
		except (ValueError, FileNotFoundError, ) as ex:
			print("Incorrect parameters in the config file or the file is missing at all. " +
				f"Path: {path_to_config}. Ex: {ex}")

			os._exit(0)

		return self.parameters_set


def setup():
	config = Config()
	parameters_set = config.setup()
	logging_setup(
		parameters_set["Path"]["path_to_log"], 
		*parameters_set["LoggingSettings"].values(),
	)

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


def workflow(parameters_set):
	factory = RecordFactory(parameters_set)
	storage = ArrayStorage(parameters_set)
	repo = RecordRepository(storage)
	for i in range(7200):
		record = factory.create_history_record()
		repo.create(record)
	print(*repo.show_all())


if __name__ == "__main__":
	parameters_set = setup()
	logging.debug("Config and logger setup was successful. " + 
		f"Number of sections from config: {len(parameters_set.keys())}")

	workflow(parameters_set)
	