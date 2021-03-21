from __future__ import annotations

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
		self._builder.produce_dates()
		self._builder.produce_notes()
		self._builder.produce_tags()
		print(self._builder._record_attributes)


class RecordBuilder(RecordBuilderInterface):
	def __init__(self):
		self._record_attributes = {}

	def record(self):
		pass

	def produce_id(self):
		logging.info('Generating the "id" attribute')
		id_obj = IdGenerator(4294967296, 65539, 0, 1)
		id_ = id_obj.generate_array()
		self._record_attributes["id"] = id_

		return id_

	def produce_sides(self):
		try:
			id_ = self._record_attributes["id"]
		except KeyError as ex:
			logging.warning('Unable to generate "side" attribute because "id" attribute was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["id"] = id_

		logging.info('Generating the "side" attribute')
		side_obj = SideGenerator(100, 1, 3, id_)
		sides = side_obj.generate_array()
		self._record_attributes["sides"] = sides

		return sides

	def produce_instruments(self):
		try:
			id_ = self._record_attributes["id"]
		except KeyError as ex:
			logging.warning('Unable to generate "instrument" attribute because "id" attribute was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["id"] = id_

		logging.info('Generating the "instrument" attribute')
		instrument_obj = InstrumentGenerator(13, 1, 3, id_)
		instruments = instrument_obj.generate_array()
		self._record_attributes["instruments"] = instruments

		return instruments

	def produce_statuses(self):
		try:
			id_ = self._record_attributes["id"]
		except KeyError as ex:
			logging.warning('Unable to generate "status" attribute because "id" attribute was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["id"] = id_

		logging.info('Generating the "status" attribute')
		status_obj = StatusGenerator(300, 7, 4, id_)
		statuses_on_broker = status_obj.generate_array()
		self._record_attributes["statuses_on_broker"] = statuses_on_broker

		return statuses_on_broker

	def produce_pxinit(self):
		try:
			instruments = self._record_attributes["instruments"]
			sides = self._record_attributes["sides"]
		except KeyError as ex:
			logging.warning('Unable to generate "px_init" attribute because "instrument" or "side" attributes was not generated')

			logging.info('Forced generation of the "instrument" attribute')
			instruments = self.produce_instruments()
			self._record_attributes["instruments"] = instruments

			logging.info('Forced generation of the "side" attribute')
			sides = self.produce_sides()
			self._record_attributes["sides"] = sides

		logging.info('Generating the "px_init" attribute')
		pxinit_obj = PXInitGenerator(instruments, sides)
		init_prices = pxinit_obj.generate_array()
		self._record_attributes["init_prices"] = init_prices

		return init_prices

	def produce_pxfill(self):
		try:
			id_ = self._record_attributes["id"]
			statuses_on_broker = self._record_attributes["statuses_on_broker"]
			init_prices = self._record_attributes["init_prices"]
		except KeyError as ex:
			logging.warning('Unable to generate "px_fill" attribute because "id", "px_init" or "status" attributes was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["id"] = id_

			logging.info('Forced generation of the "status" attribute')
			statuses_on_broker = self.produce_statuses()
			self._record_attributes["statuses_on_broker"] = statuses_on_broker

			logging.info('Forced generation of the "px_init" attribute')
			init_prices = self.produce_pxinit()
			self._record_attributes["init_prices"] = init_prices

		logging.info('Generating the "px_fill" attribute')
		pxfill_obj = PXFillGenerator(0.00101, 0.0002, 0.00032, id_, init_prices, statuses_on_broker)
		fill_prices = pxfill_obj.generate_array()
		self._record_attributes["fill_prices"] = fill_prices

		return fill_prices

	def produce_volumeinit(self):
		logging.info('Generating the "volume_init" attribute')
		init_volumes_obj = VolumeInitGenerator(1000000, 1000, 4432423, 1)
		init_volumes = init_volumes_obj.generate_array()
		self._record_attributes["init_volumes"] = init_volumes

		return init_volumes

	def produce_volumefill(self):
		try:
			id_ = self._record_attributes["id"]
			statuses_on_broker = self._record_attributes["statuses_on_broker"]
			init_volumes = self._record_attributes["init_volumes"]
		except KeyError as ex:
			logging.warning('Unable to generate "volume_fill" attribute because "id", "status" or "volume_init" attributes was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["id"] = id_

			logging.info('Forced generation of the "status" attribute')
			statuses_on_broker = self.produce_statuses()
			self._record_attributes["statuses_on_broker"] = statuses_on_broker

			logging.info('Forced generation of the "volume_init" attribute')
			init_volumes = self.produce_volumeinit()
			self._record_attributes["init_volumes"] = init_volumes

		logging.info('Generating the "volume_fill" attribute')
		fill_volumes_obj = VolumeFillGenerator(1000, 4432423, id_, statuses_on_broker, init_volumes)
		fill_volumes = fill_volumes_obj.generate_array()
		self._record_attributes["fill_volumes"] = fill_volumes

		return fill_volumes

	def produce_dates(self):
		logging.info('Generating the "date" attribute')
		date_obj = DateGenerator(1000, 12, 7, 1, '01.02.2021  0:00:00')
		dates = date_obj.generate_array()
		self._record_attributes["dates"] = dates

		return dates

	def produce_notes(self):
		try:
			id_ = self._record_attributes["id"]
		except KeyError as ex:
			logging.warning('Unable to generate "note" attribute because "id" attribute was not generated')

			logging.info('Forced generation of the "id" attribute')
			id_ = self.produce_id()
			self._record_attributes["id"] = id_


		logging.info('Generating the "note" attribute')
		note_obj = NoteGenerator(13, 1, 3, id_)
		notes = note_obj.generate_array()
		self._record_attributes["notes"] = notes

		return notes

	def produce_tags(self):
		logging.info('Generating the "tags" attribute')
		tag_obj = TagGenerator(13, 1, 3, 423543, 1000, 43232, 1)
		tags = tag_obj.generate_array()
		self._record_attributes["tags"] = tags

		return tags

	def collect_record(self):
		pass


if __name__ == "__main__":
	parameters_set = setup()
	logging.debug("Config and logger setup was successful. " + 
		f"Number of sections from config: {len(parameters_set.keys())}")

	factory = RecordFactory()
	factory.create_list_records()
	
