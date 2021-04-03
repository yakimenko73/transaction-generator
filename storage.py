from __future__ import annotations

import sys
# import mysql.connector
# from mysql.connector import errorcode

from interfaces import StorageInterface
from utils import Singleton
from constants import *


class RecordRepository:
	def __init__(self, storage: StorageInterface):
		self._storage = storage

	def show_all(self):
		return self._storage.find_all()

	def find_by_id(self, id):
		return self._storage.find_by_id(id)

	def create(self, data):
		return self._storage.create(data)


class ArrayStorage(StorageInterface):
	def __init__(self, config: dict=None):
		self.__array = []

	def find_all(self):
		return self.__array

	def find_by_id(self, id):
		try:
			record = self.__array[id]
		except IndexError as ex:
			record = None
		return record

	def create(self, data):
		record = data.__dict__
		self.__array.append(record)
		return record


class MySQLStorage(StorageInterface):
	def __init__(self, config: dict):
		self._config = config
		self.__connection = MySQLConnector(self._config)
		self._create_database()
		self._use_database()
		self._create_table()

	def find_all(self):
		query = f"SELECT * FROM {self._config['MySQLSettings']['table_name']}"
		cursor = self._execute_query(query)
		response = self._mapping_response(cursor)
		return response

	def find_by_id(self, id):
		query = f"SELECT * FROM {self._config['MySQLSettings']['table_name']} WHERE ID = '{id}'"
		cursor = self._execute_query()
		response = self._mapping_response(cursor)
		return response[0]

	def create(self, data):
		record = data.__dict__
		query = "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"\
			.format(self._config['MySQLSettings']['table_name'], *record.values())
		self._execute_query(query)

		return record

	def _execute_query(self, query):
		cursor = self.__connection.cursor()
		cursor.execute(query)
		self.__connection.commit()
		return cursor

	def _create_database(self):
		query = f""" 
			CREATE DATABASE IF NOT EXISTS {self._config['MySQLSettings']['database_name']}
		"""
		
		self._execute_query(query)

	def _use_database(self):
		query = f"USE {self._config['MySQLSettings']['database_name']}"

		self._execute_query(query)

	def _create_table(self):
		attr = ORDER_ATTRIBUTES
		query = f"""
		CREATE TABLE IF NOT EXISTS {self._config['MySQLSettings']['table_name']} (
			INT(5) PRIMARY KEY NOT NULL AUTO_INCREMENT, 
			{attr[0]} VARCHAR(10),
			{attr[1]} ENUM({', '.join(SIDES)}),
			{attr[2]} ENUM({', '.join(map(lambda instrument: instrument[0], INSTRUMENTS))}),
			{attr[3]} ENUM({', '.join(map(lambda status: ' '.join(status) if type(status) == list else status, STATUSES))}),
			{attr[4]} INT(4),
			{attr[5]} INT(4),
			{attr[6]} FLOAT(4),
			{attr[7]} FLOAT(4),
			{attr[8]} VARCHAR(255),
			{attr[9]} VARCHAR(100))
			{attr[10]} DATETIME(3),
		"""
		self._execute_query(query)

	def _mapping_response(self, cursor):
		response = []
		for item in cursor:
			record = {}
			for index, attribute in enumerate(ORDER_ATTRIBUTES):
				record[attribute] = item[index+1]
			response.append(record)
		return response


class MySQLConnector(metaclass=Singleton):
	def __init__(self, config):
		self._user = config['MySQLSettings']["user"]
		self._password = config['MySQLSettings']["password"]
		self._host = config['MySQLSettings']["host"]

		self.connect = mysql.connector.connect(
			user=self._user, 
			password=self._password,
			host=self._host
		)

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.connect.close()