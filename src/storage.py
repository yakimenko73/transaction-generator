from __future__ import annotations


class RecordRepository:
    def __init__(self, storage: StorageInterface):
        self._storage = storage

    def show_all(self):
        return self._storage.find_all()

    def find_by_id(self, id):
        return self._storage.find_by_id(id)

    def create(self, data):
        return self._storage.create(data)



