import os
import re

import logging
import configparser


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


def id_generator():
	global a, m, c, seed
	list_numbers = []

	for i in range(2000):
		seed = (a * seed + c) % m

		list_numbers.append(seed)

	return list_numbers


def setup():
	regex_filepath = re.compile("\w+/")

	parameters_set = config_setup()
	logging_setup(regex_filepath, 
		parameters_set["Path"]["PATH_TO_LOG"], 
		*parameters_set["LoggingSettings"].values(),
	)


def config_setup():
	config = configparser.ConfigParser()
	config.read("settings/config.ini")

	try:
		path_to_log = config["Path"]["PATH_TO_LOG"]

		log_level = config["LoggingSettings"]["LEVEL"].upper()
		log_filemode = config["LoggingSettings"]["FILEMODE"].lower()

		ID_m = config["IDSettings"]["MODULUS"]
		ID_a = config["IDSettings"]["MULTIPLIER"]
		ID_c = config["IDSettings"]["INCREMENT"]
		ID_seed = config["IDSettings"]["SEED"]
	except KeyError as ex:
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
	}

	return parameters_set


def logging_setup(regex_filepath, path_to_log, log_filemode, log_level):
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


if __name__ == "__main__":
	setup()