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
	def __init__(self):
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
		self.__connection = MySQLConnector()
		self.__config = config
		self._create_database()
		self._use_database()
		self._create_table()

	def find_all(self):
		query = f"SELECT * FROM {TABLE_NAME}"
		cursor = self._execute_query(query)
		response = self._mapping_response(cursor)
		return response

	def find_by_id(self, id):
		query = f"SELECT * FROM {TABLE_NAME} WHERE ID = '{id}'"
		cursor = self._execute_query()
		response = self._mapping_response(cursor)
		return response[0]

	def create(self, data):
		record = data.__dict__
		query = "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(TABLE_NAME, *record.values())
		self._execute_query(query)

		return record

	def _execute_query(self, query):
		cursor = self.__connection.cursor()
		cursor.execute(query)
		self.__connection.commit()
		return cursor

	def _create_database(self):
		query = f""" 
			CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}
		"""
		
		self._execute_query(query)

	def _use_database(self):
		query = f"USE {DATABASE_NAME}"

		self._execute_query(query)

	def _create_table(self):
		query = f"""
		CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
			INT(5) PRIMARY KEY NOT NULL AUTO_INCREMENT, 
			ID VARCHAR(10),
			SIDE ENUM({', '.join(SIDES)}),
			INSTRUMENT ENUM({', '.join(map(lambda instrument: instrument[0], INSTRUMENTS))}),
			STATUS ENUM({', '.join(map(lambda status: ' '.join(status) if type(status) == list else status, STATUSES))}),
			PX_INIT INT(4),
			PX_FILL INT(4),
			VOLUME_INIT FLOAT(4),
			VOLUME_FILL FLOAT(4),
			NOTE VARCHAR(255),
			TAGS VARCHAR(100))
			DATE DATETIME(3),
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
	def __init__(self, user="root", password="root", host="127.0.0.1"):
		self._user = user
		self._password = password
		self._host = host

		self.connect = mysql.connector.connect(
			user=self._user, 
			password=self._password,
			host=self._host
		)

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.connect.close()