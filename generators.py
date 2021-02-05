from constants import *


def id_generator(m, a, c, seed):
	list_numbers = []

	for i in range(2000):
		seed = (a * seed + c) % m

		list_numbers.append(seed)

	return list_numbers


def side_generator(m, a, c, seed):
	list_sides = []

	for i in range(2000):
		seed = (a * seed + c) % m

		if seed <= 500:
			list_sides.append(SIDES[0])
		else:
			list_sides.append(SIDES[1])

	return list_sides


def instrument_generator(m, a, c, seed):
	list_instruments = []

	for i in range(2000):
		seed = (a * seed + c) % m
		try:
			list_instruments.append(INSTRUMENTS[seed-1])
		except IndexError:
			list_instruments.append(INSTRUMENTS[0])

	return list_instruments

def status_generator(m, a, c, seed):
	list_statuses_on_broker = []

	for i in range(2000):
		seed = (a * seed + c) % m

		if seed <= 341:
			list_statuses_on_broker.append(STATUSES[2])
		elif seed >= 342 and seed <= 683:
			list_statuses_on_broker.append(STATUSES[3])
		else:
			list_statuses_on_broker.append(STATUSES[4])

	return list_statuses_on_broker


def generate_records(parameters):
	pass