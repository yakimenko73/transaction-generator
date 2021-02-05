import os
import re

import logging
import configparser

from generators import *


TRUE_LOG_LEVELS = [
	'CRITICAL', 
	'ERROR', 
	'WARNING', 
	'INFO', 
	'DEBUG', 
]

TRUE_FILE_MODES = [
	'r',
	'w',
	'x',
	'a',
	'b',
	't',
	'+',
]


def setup():
	regex_filepath = re.compile("\w+/")

	parameters_set = config_setup()
	logging_setup(regex_filepath, 
		parameters_set["Path"]["PATH_TO_LOG"], 
		*parameters_set["LoggingSettings"].values(),
	)

	return parameters_set


def config_setup():
	config = configparser.ConfigParser()
	config.read("settings/config.ini")

	try:
		path_to_log = config["Path"]["PATH_TO_LOG"]

		log_level = config["LoggingSettings"]["LEVEL"].upper()
		log_filemode = config["LoggingSettings"]["FILEMODE"].lower()

		ID_m = int(config["IDSettings"]["MODULUS"])
		ID_a = int(config["IDSettings"]["MULTIPLIER"])
		ID_c = int(config["IDSettings"]["INCREMENT"])
		ID_seed = int(config["IDSettings"]["SEED"])

		side_m = int(config["SideSettings"]["MODULUS"])
		side_a = int(config["SideSettings"]["MULTIPLIER"])
		side_c = int(config["SideSettings"]["INCREMENT"])
		side_seed = int(config["SideSettings"]["SEED"])

		instrument_m = int(config["InstrumentSettings"]["MODULUS"])
		instrument_a = int(config["InstrumentSettings"]["MULTIPLIER"])
		instrument_c = int(config["InstrumentSettings"]["INCREMENT"])
		instrument_seed = int(config["InstrumentSettings"]["SEED"])

		status_m = int(config["StatusSettings"]["MODULUS"])
		status_a = int(config["StatusSettings"]["MULTIPLIER"])
		status_c = int(config["StatusSettings"]["INCREMENT"])
		status_seed = int(config["StatusSettings"]["SEED"])
	except (KeyError, ValueError,) as ex:
		print("Incorrect parameters in the config file or the file is missing at all")

		os._exit(0)

	parameters_set = {
		"Path": {
			"PATH_TO_LOG": path_to_log,
		},
		"LoggingSettings": {
			"LEVEL": log_level,
			"FILEMODE": log_filemode,
		},
		"IDSettings": {
			"MODULUS": ID_m,
			"MULTIPLIER": ID_a,
			"INCREMENT": ID_c,
			"SEED": ID_seed,
		},
		"SideSettings": {
			"MODULUS": side_m,
			"MULTIPLIER": side_a,
			"INCREMENT": side_c,
			"SEED": side_seed,
		},
		"InstrumentSettings": {
			"MODULUS": instrument_m,
			"MULTIPLIER": instrument_a,
			"INCREMENT": instrument_c,
			"SEED": instrument_seed,
		},
		"StatusSettings": {
			"MODULUS": status_m,
			"MULTIPLIER": status_a,
			"INCREMENT": status_c,
			"SEED": status_seed,
		},
	}

	return parameters_set


def logging_setup(regex_filepath, path_to_log, log_level, log_filemode):
	if not log_level in TRUE_LOG_LEVELS:
		log_level = 'DEBUG'

	if not log_filemode in TRUE_FILE_MODES:
		log_filemode = 'a'

	pathdir = ''.join(regex_filepath.findall(path_to_log))
	if pathdir:
		if not os.path.exists(pathdir):
			os.makedirs(pathdir)

	logging.basicConfig(filename=path_to_log, 
		level=log_level,
		filemode=log_filemode, 
		format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s: %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S')


def workflow(parameters):
	id_ = id_generator(*parameters["IDSettings"].values())
	sides = side_generator(*parameters["SideSettings"].values())
	instruments = instrument_generator(*parameters["InstrumentSettings"].values())
	statuses = status_generator(*parameters["StatusSettings"].values())

	print(statuses)


if __name__ == "__main__":
	parameters_set = setup()
	workflow(parameters_set)