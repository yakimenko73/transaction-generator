import math
import datetime as dt

from constants import *


def id_generator(m, a, c, seed):
	list_id = []

	for i in range(MAX_NUMBER_ORDERS):
		seed = (a * seed + c) % m

		list_id.append(hex(seed))

	return list_id


def side_generator(m, a, c, seeds):
	list_sides = []

	for i in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[i], 16) + c) % m

		if seed <= 50:
			list_sides.append(SIDES[0])
		else:
			list_sides.append(SIDES[1])

	return list_sides


def instrument_generator(m, a, c, seeds):
	list_instruments = []

	for i in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[i], 16) + c) % m
		try:
			list_instruments.append(INSTRUMENTS[seed-1][0])
		except IndexError:
			list_instruments.append(INSTRUMENTS[0][0])

	return list_instruments

def status_generator(m, a, c, seeds):
	list_statuses_on_broker = []

	for i in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[i], 16) + c) % m

		if seed <= 100:
			list_statuses_on_broker.append(STATUSES[2][0])
		elif seed >= 101 and seed <= 200:
			list_statuses_on_broker.append(STATUSES[2][1])
		else:
			list_statuses_on_broker.append(STATUSES[2][2])

	return list_statuses_on_broker


def pxinit_generator(instruments, sides):
	list_prices = []

	for i in range(MAX_NUMBER_ORDERS):
		for j in range(len(INSTRUMENTS)):
			if INSTRUMENTS[j][0] == instruments[i]:
				if sides[i] == "BUY":
					list_prices.append(INSTRUMENTS[j][1])
				else:
					list_prices.append(INSTRUMENTS[j][2])
	return list_prices


def pxfill_generator(m, a, c, seeds, init_prices):
	list_prices = []

	for i in range(MAX_NUMBER_ORDERS):
		seed = round((a * int(seeds[i], 16) + c) % m, 5)

		if seed < 0.0005:
			fill_price = init_prices[i] + seed
		else:
			fill_price = init_prices[i] - seed

		list_prices.append(round(fill_price, 5))

	return list_prices


def volumeinit_generator(m, a, c, seed):
	list_volumes = []
	rounding_number = 1000

	for i in range(MAX_NUMBER_ORDERS):
		seed = (a * int(str(seed), 16) + c) % m
		seed = math.ceil(seed/rounding_number)*rounding_number-rounding_number

		list_volumes.append(seed)

	return list_volumes


def volumefill_generator(a, c, seeds, statuses_on_broker, init_volumes):
	list_volumes = []
	rounding_number = 1000

	for i in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[i], 16) + c) % init_volumes[i]
		seed = math.ceil(seed/rounding_number)*rounding_number-rounding_number

		if statuses_on_broker[i] == STATUSES[2][1]:
			fill_volume = init_volumes[i] - seed
		elif statuses_on_broker[i] == STATUSES[2][2]:
			fill_volume = 0
		else:
			fill_volume = init_volumes[i]

		list_volumes.append(fill_volume)

	return list_volumes


def date_generator(m, a, c, start_date, seeds):
	date = dt.datetime.strptime(start_date, '%d.%m.%Y %H:%M:%S.%f')
	print(date.time())
	print(date.mill)
	list_dates = []

	divisor_number = MAX_NUMBER_ORDERS/100
	number_records = int(divisor_number * ORDERS_CREATED_BEFORE_RECORDING * NUMBER_RECORDS_FIRST_SEGMENT +
		divisor_number * ORDERS_CREATED_AND_DONE * NUMBER_RECORDS_SECOND_SEGMENT +
		divisor_number * ORDERS_COMPLETED_AFTER_RECORDING * NUMBER_RECORDS_THIRD_SEGMENT
	)

	# for i in range(number_records):
	# 	if i == 0:
	# 		list_dates.append(date)
		
	# 	date = date + 0.000001

	# 	list_dates.append(date)

	# return list_dates


def generate_orders(parameters):
	id_ = id_generator(*parameters["IDSettings"].values())
	sides = side_generator(*parameters["SideSettings"].values())
	instruments = instrument_generator(*parameters["InstrumentSettings"].values())
	statuses_on_broker = status_generator(*parameters["StatusSettings"].values())

	list_orders = [
		*generate_first_segment(
			ORDERS_CREATED_BEFORE_RECORDING, 
			id_, 
			sides, 
			instruments, 
			statuses_on_broker,
		),
		*generate_second_segment(ORDERS_CREATED_AND_DONE, 
			id_, 
			sides, 
			instruments, 
			statuses_on_broker,
		),
		*generate_third_segment(ORDERS_COMPLETED_AFTER_RECORDING, 
			id_, 
			sides, 
			instruments, 
			statuses_on_broker,
		),
	]

	return list_orders


def generate_first_segment(percent, id_, sides, instruments, statuses_on_broker):
	number_records_to_generate = int((MAX_NUMBER_ORDERS/100) * percent)
	list_orders = []

	for order_number in range(number_records_to_generate):
		order = []
		for i in range(3):
			if i == 1:
				status = statuses_on_broker[order_number]
			else:
				status = STATUSES[i+1]
			record = [
				id_[order_number],
				sides[order_number],
				instruments[order_number],
				status,
			]
			order.append(record)
		list_orders.append(order)

	return list_orders


def generate_second_segment(percent, id_, sides, instruments, statuses_on_broker):
	number_records_to_generate = int((MAX_NUMBER_ORDERS/100) * percent)
	list_orders = []

	for order_number in range(number_records_to_generate):
		order = []
		for i in range(4):
			if i == 2:
				status = statuses_on_broker[order_number]
			else:
				status = STATUSES[i]
			record = [
				id_[order_number],
				sides[order_number],
				instruments[order_number],
				status,
			]
			order.append(record)
		list_orders.append(order)

	return list_orders


def generate_third_segment(percent, id_, sides, instruments, statuses_on_broker):
	number_records_to_generate = int((MAX_NUMBER_ORDERS/100) * percent)
	list_orders = []

	for order_number in range(number_records_to_generate):
		order = []
		for i in range(3):
			if i == 2:
				status = statuses_on_broker[order_number]
			else:
				status = STATUSES[i]
			record = [
				id_[order_number],
				sides[order_number],
				instruments[order_number],
				status,
			]
			order.append(record)
		list_orders.append(order)

	return list_orders