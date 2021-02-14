import os
import re
import csv

import logging
import configparser

from generators import *
from constants import TRUE_LOG_LEVELS, TRUE_FILE_MODES, ORDER_ATTRIBUTES


def setup():
	parameters_set = config_setup()
	logging_setup(
		parameters_set["Path"]["path_to_log"], 
		*parameters_set["LoggingSettings"].values(),
	)

	return parameters_set


def config_setup():
	config = configparser.ConfigParser()
	config.read("settings/config.ini")

	parameters_set = { }

	try:
		for section in config:
			if section != "DEFAULT":
				parameters_set[section] = {}
			for field in config[section]:
				if section == "LoggingSettings":
					parameters_set[section][field] = config[section][field].lower()

				elif (section == "DateSettings" and field != "start_date") \
				or section == "PXFillSettings":
					parameters_set[section][field] = float(config[section][field])

				elif (section == "DateSettings" and field == "start_date") \
				or section == "Path":
					parameters_set[section][field] = config[section][field]
				else:
					parameters_set[section][field] = int(config[section][field])
		if not parameters_set:
			raise(KeyError)
	except (KeyError, ValueError, ) as ex:
		print(f"Incorrect parameters in the config file or the file is missing at all {ex}")

		os._exit(0)

	return parameters_set


def logging_setup(path_to_log, log_level, log_filemode):
	if not log_level in TRUE_LOG_LEVELS:
		log_level = 'DEBUG'

	if not log_filemode in TRUE_FILE_MODES:
		log_filemode = 'a'

	create_file_path(path_to_log)

	logging.basicConfig(filename=path_to_log, 
		level=log_level,
		filemode=log_filemode, 
		format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s: %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S')


def create_file_path(path):
	pathdir = ''.join(re.findall("\w+/", path))
	if pathdir:
		if not os.path.exists(pathdir):
			os.makedirs(pathdir)


def workflow(parameters):
	orders = create_list_orders(parameters)
	path_to_csv = parameters["Path"]["path_to_csv"]

	create_file_path(path_to_csv)

	write_csv(path_to_csv, orders)
	read_csv(path_to_csv)


def write_csv(filename, orders):
	with open(filename, "w") as f:
		csv_f = csv.writer(f)
		csv_f.writerow(ORDER_ATTRIBUTES)

		for order in orders:
			for record in order:
				csv_f.writerow(record)


def read_csv(filename):
	with open(filename, "r", newline="") as f:
		csv_f = csv.reader(f)

		for row in csv_f:
			if row:
				print('{:<13}{:<7}{:<13}{:<14}{:<12}{:<12}{:<14}{:<14}{:<10}{:<64}{:<26}'.format(*row))


if __name__ == "__main__":
	parameters_set = setup()
	workflow(parameters_set)