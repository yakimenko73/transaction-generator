import os
import re

import logging
import configparser

from generators import *
from constants import TRUE_LOG_LEVELS, TRUE_FILE_MODES


def setup():
	regex_filepath = re.compile("\w+/")

	parameters_set = config_setup()
	logging_setup(
		regex_filepath, 
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
	dates = date_generator(*parameters["DateSettings"].values())

	for i in range(len(dates)):
		print(dates[i], end='\n')

if __name__ == "__main__":
	parameters_set = setup()
	workflow(parameters_set)