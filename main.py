import os
import re
import csv
import datetime as dt

import logging
import configparser

from generators import create_list_orders
from constants import * 


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


def workflow(parameters):
	logging.debug("Attempt to generate a list of orders")
	list_orders = create_list_orders(parameters)
	logging.debug(f"The list of orders has been generated successfully. Number of orders: {len(list_orders)}")

	path = create_file_path(parameters["Path"]["path_to_csv"])

	logging.debug(f"An attempt to write a list of orders to a csv file. Path: {path}.")
	write_csv(path, list_orders)

	logging.debug(f"An attempt to read a list of orders from a csv file. Path: {path}.")
	read_csv(path)


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


def write_csv(filename, list_orders):
	try:
		with open(filename, "w") as f:
			csv_f = csv.writer(f)
			csv_f.writerow(ORDER_ATTRIBUTES)

			for order in list_orders:
				for record in order:
					csv_f.writerow(record)
	except OSError as ex:
		logging.error(f"Failed to write data to file. Path: {filename}. Ex: {ex}")
		return 0


def read_csv(filename):
	try:
		with open(filename, "r", newline="") as f:
			csv_f = csv.reader(f)

			for row in csv_f:
				if row:
					print(FORMAT_DISPLAYING_ORDERS.format(*row))
	except OSError as ex:
		logging.error(f"Failed to read data from file. Path: {filename}. Example: {ex}")
		return 0


if __name__ == "__main__":
	parameters_set = setup()
	logging.debug("Config and logger setup was successful. " + 
		f"Number of sections from config: {len(parameters_set.keys())}")
	workflow(parameters_set)