from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty

class RecordFactoryInterface(ABC):
	@abstractmethod
	def create_history_record(self) -> list:
		pass


class RecordBuilderInterface(ABC):
	@abstractmethod
	def produce_id(self) -> list:
		pass

	@abstractmethod
	def produce_side(self) -> list:
		pass

	@abstractmethod
	def produce_instrument(self) -> list:
		pass

	@abstractmethod
	def produce_status(self) -> list:
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
	def produce_date(self) -> list:
		pass

	@abstractmethod
	def produce_note(self) -> list:
		pass

	@abstractmethod
	def produce_tags(self) -> list:
		pass

	@abstractmethod
	def collect_record(self) -> list:
		pass


class StorageInterface(ABC):
	@abstractmethod
	def find_all(self) -> list:
		pass

	@abstractmethod
	def create(self) -> dict:
		pass

	@abstractmethod
	def find_by_id(self) -> dict:
		pass