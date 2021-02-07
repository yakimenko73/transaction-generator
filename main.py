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
		parameters_set["Path"]["PATH_TO_LOG"], 
		*parameters_set["LoggingSettings"].values(),
	)

	return parameters_set


def config_setup():
	config = configparser.ConfigParser()
	config.read("settings/config.ini")

	try:
		parameters_set = {
			"Path": {
				"PATH_TO_LOG": config["Path"]["PATH_TO_LOG"],
			},
			"LoggingSettings": {
				"LEVEL": config["LoggingSettings"]["LEVEL"].upper(),
				"FILEMODE": config["LoggingSettings"]["FILEMODE"].lower(),
			},
			"IDSettings": {
				"MODULUS": int(config["IDSettings"]["MODULUS"]),
				"MULTIPLIER": int(config["IDSettings"]["MULTIPLIER"]),
				"INCREMENT": int(config["IDSettings"]["INCREMENT"]),
				"SEED": int(config["IDSettings"]["SEED"]),
			},
			"SideSettings": {
				"MODULUS": int(config["SideSettings"]["MODULUS"]),
				"MULTIPLIER": int(config["SideSettings"]["MULTIPLIER"]),
				"INCREMENT": int(config["SideSettings"]["INCREMENT"]),
			},
			"InstrumentSettings": {
				"MODULUS": int(config["InstrumentSettings"]["MODULUS"]),
				"MULTIPLIER": int(config["InstrumentSettings"]["MULTIPLIER"]),
				"INCREMENT": int(config["InstrumentSettings"]["INCREMENT"]),
			},
			"StatusSettings": {
				"MODULUS": int(config["StatusSettings"]["MODULUS"]),
				"MULTIPLIER": int(config["StatusSettings"]["MULTIPLIER"]),
				"INCREMENT": int(config["StatusSettings"]["INCREMENT"]),
			},
			"PXFillSettings": {
				"MODULUS": float(config["PXFillSettings"]["MODULUS"]),
				"MULTIPLIER": float(config["PXFillSettings"]["MULTIPLIER"]),
				"INCREMENT": float(config["PXFillSettings"]["INCREMENT"]),
			},
			"VolumeInitSettings": {
				"MODULUS": int(config["VolumeInitSettings"]["MODULUS"]),
				"MULTIPLIER": int(config["VolumeInitSettings"]["MULTIPLIER"]),
				"INCREMENT": int(config["VolumeInitSettings"]["INCREMENT"]),
				"SEED": int(config["VolumeInitSettings"]["SEED"]),
			},
			"VolumeFillSettings": {
				"MULTIPLIER": int(config["VolumeFillSettings"]["MULTIPLIER"]),
				"INCREMENT": int(config["VolumeFillSettings"]["INCREMENT"]),
			},
			"DateSettings": {
				"MODULUS": int(config["DateSettings"]["MODULUS"]),
				"MULTIPLIER": int(config["DateSettings"]["MULTIPLIER"]),
				"INCREMENT": int(config["DateSettings"]["INCREMENT"]),
				"SEED": int(config["DateSettings"]["SEED"]),
				"START_DATE": config["DateSettings"]["START_DATE"],
			},
			"NoteSettings": {
				"MODULUS": int(config["NoteSettings"]["MODULUS"]),
				"MULTIPLIER": int(config["NoteSettings"]["MULTIPLIER"]),
				"INCREMENT": int(config["NoteSettings"]["INCREMENT"]),
			},
		}
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
	orders = create_list_orders(parameters)

	for i in range(len(orders)):
		print(*orders[i], end='\n')
		if i == 2000:
			break


if __name__ == "__main__":
	parameters_set = setup()
	workflow(parameters_set)