from __future__ import annotations

from interfaces import StorageInterface


class RecordRepository:
	def __init__(self, storage: StorageInterface):
		self._storage = storage

	def show_all(self):
		return self._storage.find_all()

	def create(self, data):
		return self._storage.create(data)

	def find_by_id(self, id):
		return self._storage.find_by_id(id)


class ArrayStorage(StorageInterface):
	def __init__(self):
		self.__array = []

	def find_all(self):
		return self.__array

	def create(self, data):
		record = self.__array.append(data.__dict__)

		return record

	def find_by_id(self, id):
		try:
			record = self.__array[id]
		except IndexError as ex:
			record = None

		return record
