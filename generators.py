from constants import *


def id_generator(m, a, c, seed):
	list_id = []

	for i in range(2000):
		seed = (a * seed + c) % m

		list_id.append(seed)

	return list_id


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
			list_statuses_on_broker.append(STATUSES[2][0])
		elif seed >= 342 and seed <= 683:
			list_statuses_on_broker.append(STATUSES[2][1])
		else:
			list_statuses_on_broker.append(STATUSES[2][2])

	return list_statuses_on_broker


def generate_orders(parameters):
	id_ = id_generator(*parameters["IDSettings"].values())
	sides = side_generator(*parameters["SideSettings"].values())
	instruments = instrument_generator(*parameters["InstrumentSettings"].values())
	statuses_on_broker = status_generator(*parameters["StatusSettings"].values())

	list_orders = []
	for order_number in range(2000):
		order = []
		if order_number >= 0 and order_number <= 599:
			for i in range(3):
				if i == 1:
					status = statuses_on_broker[order_number]
				else:
					status = STATUSES[i+1]
				row = [
					id_[order_number],
					sides[order_number],
					instruments[order_number],
					status,
				]
				order.append(row)
			list_orders.append(order)
		else:
			break
	return list_orders
