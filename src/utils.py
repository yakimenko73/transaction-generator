import re
import os


class Singleton(type):
	_instances = None

	def __call__(cls, *args, **kwargs):
		if not cls._instances:
			cls._instances = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances


def create_file_path(path):
	pathdir = ''.join(re.findall(r"\w+/", path))
	if pathdir:
		if not os.path.exists(pathdir):
			try:
				os.makedirs(pathdir)
			except OSError as ex:
				logging.warning("Failed to create file in the selected path. " +
					f"Created a file in the executing directory. Path: {path}. Ex: {ex}")
				path = os.path.basename(path)
	return path