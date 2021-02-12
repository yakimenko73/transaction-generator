import math
import numpy as np
import datetime as dt

from constants import *


def id_generator(m, a, c, seed):
	list_id = []

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = (a * seed + c) % m

		list_id.append(hex(seed))

	return list_id


def side_generator(m, a, c, seeds):
	list_sides = []

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[order_number], 16) + c) % m
		if seed <= 50:
			list_sides.append(SIDES[0])
		else:
			list_sides.append(SIDES[1])

	return list_sides


def instrument_generator(m, a, c, seeds):
	list_instruments = []

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[order_number], 16) + c) % m
		try:
			list_instruments.append(INSTRUMENTS[seed-1][0])
		except IndexError:
			list_instruments.append(INSTRUMENTS[10][0])

	return list_instruments


def status_generator(m, a, c, seeds):
	list_statuses_on_broker = []

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[order_number], 16) + c) % m
		if seed <= 100:
			list_statuses_on_broker.append(STATUSES[2][0])
		elif seed >= 101 and seed <= 200:
			list_statuses_on_broker.append(STATUSES[2][1])
		else:
			list_statuses_on_broker.append(STATUSES[2][2])

	return list_statuses_on_broker


def pxinit_generator(instruments, sides):
	list_prices = []

	for order_number in range(MAX_NUMBER_ORDERS):
		for j in range(len(INSTRUMENTS)):
			if INSTRUMENTS[j][0] == instruments[order_number]:
				if sides[order_number] == "BUY":
					list_prices.append(INSTRUMENTS[j][1])
				else:
					list_prices.append(INSTRUMENTS[j][2])
	return list_prices


def pxfill_generator(m, a, c, seeds, init_prices):
	list_prices = []

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = round((a * int(seeds[order_number], 16) + c) % m, 5)
		if seed < 0.0005:
			fill_price = init_prices[order_number] + seed
		else:
			fill_price = init_prices[order_number] - seed

		list_prices.append(round(fill_price, 5))

	return list_prices


def volumeinit_generator(m, a, c, seed):
	list_volumes = []
	rounding_number = 1000

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = (a * int(str(seed), 16) + c) % m
		seed = math.ceil(seed/rounding_number) * rounding_number - rounding_number

		list_volumes.append(seed)

	return list_volumes


def volumefill_generator(a, c, seeds, statuses_on_broker, init_volumes):
	list_volumes = []
	rounding_number = 1000

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[order_number], 16) + c) % init_volumes[order_number]
		seed = math.ceil(seed/rounding_number) * rounding_number - rounding_number

		if statuses_on_broker[order_number] == STATUSES[2][1]:
			fill_volume = init_volumes[order_number] - seed
		elif statuses_on_broker[order_number] == STATUSES[2][2]:
			fill_volume = 0
		else:
			fill_volume = init_volumes[order_number]

		list_volumes.append(fill_volume)

	return list_volumes


def date_generator(m, a, c, seed, start_date):
	date = dt.datetime.strptime(start_date, '%d.%m.%Y %H:%M:%S')
	list_dates = []

	for order_number in range(MAX_NUMBER_ORDERS):
		dates_for_order = []
		if order_number <= NUMBER_ORDERS_FOR_FIRST_SEGMENT-1:
			number_dates = NUMBER_RECORDS_FOR_FIRST_SEGMENT
		elif order_number <= NUMBER_ORDERS_FOR_SECOND_SEGMENT-1:
			number_dates = NUMBER_RECORDS_FOR_SECOND_SEGMENT
		else:
			number_dates = NUMBER_RECORDS_FOR_THIRD_SEGMENT

		for record_number in range(number_dates):
			seed = (a * seed + c) % m

			increment_in_seconds = str(seed)[0]
			increment_in_milliseconds = f".{int(seed)}"

			date = date + dt.timedelta(seconds=int(increment_in_seconds))

			dates_for_order.append(date.strftime('%d.%m.%Y %H:%M:%S') + increment_in_milliseconds)
		
		list_dates.append(dates_for_order)

	return list_dates


def note_generator(m, a, c, seeds):
	list_notes = []

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[order_number], 16) + c) % m
		try:
			list_notes.append(NOTES[seed-1])
		except IndexError:
			list_notes.append(NOTES[10])

	return list_notes


def tags_generator(number_m, number_a, number_c, tag_m, tag_a, tag_c, seed):
	list_tags = []
	tags_kit = generate_tags_matrix(tag_m, tag_a, tag_c, seed)

	for order_number in range(MAX_NUMBER_ORDERS):
		seed = (number_a * seed + number_c) % number_m

		list_tags.append(tags_kit[seed].tolist())

	return list_tags


def generate_tags_matrix(m, a, c, seed):
	matrix_tags = np.zeros((NUMBER_OF_DIFFERENT_TAGS_SETS, len(TAGS)))
	matrix_tags = matrix_tags.astype("str")

	for row in range(NUMBER_OF_DIFFERENT_TAGS_SETS):
		for column in range(len(TAGS)):
			seed = (a * seed + c) % m

			matrix_tags[row][column] = TAGS[column] if seed % 2 else ""

	return matrix_tags


def generate_order_attributes(parameters):
	id_ = id_generator(*parameters["IDSettings"].values())
	sides = side_generator(*parameters["SideSettings"].values(), id_)
	instruments = instrument_generator(*parameters["InstrumentSettings"].values(), id_)
	statuses_on_broker = status_generator(*parameters["StatusSettings"].values(), id_)
	init_prices = pxinit_generator(instruments, sides)
	fill_prices = pxfill_generator(
		*parameters["PXFillSettings"].values(), 
		id_, 
		init_prices,
	)
	init_volumes = volumeinit_generator(*parameters["VolumeInitSettings"].values())
	fill_volumes = volumefill_generator(
		*parameters["VolumeFillSettings"].values(), 
		id_, 
		statuses_on_broker, 
		init_volumes,
	)
	notes = note_generator(*parameters["NoteSettings"].values(), id_)
	tags = tags_generator(*parameters["TagSettings"].values())
	dates = date_generator(*parameters["DateSettings"].values())

	return (
		id_, sides, instruments,
		statuses_on_broker, init_prices, fill_prices,
		init_volumes, fill_volumes, notes,
		tags, dates,
	)


def create_list_orders(parameters):
	list_orders = []

	attributes = generate_order_attributes(parameters)

	for order_number in range(MAX_NUMBER_ORDERS):
		order_items = {}
		for number_attribute in range(len(ORDER_ATTRIBUTES)):
			order_items[ORDER_ATTRIBUTES[number_attribute]] = attributes[number_attribute][order_number]

		if order_number <= NUMBER_ORDERS_FOR_FIRST_SEGMENT-1:
			number_records = NUMBER_RECORDS_FOR_FIRST_SEGMENT
			is_first_segment = True
		elif order_number <= NUMBER_ORDERS_FOR_SECOND_SEGMENT-1:
			number_records = NUMBER_RECORDS_FOR_SECOND_SEGMENT
			is_first_segment = False
		else:
			number_records = NUMBER_RECORDS_FOR_THIRD_SEGMENT
			is_first_segment = False

		order = create_order(number_records,
			is_first_segment,
			order_items,
		)

		list_orders.append(order)

	return list_orders


def create_order(number_records, is_first_segment, order_items):
	order = []

	for record_number in range(number_records):
		record = []
		if is_first_segment:
			if record_number == 1:
				status = order_items["STATUS"]
			else:
				status = STATUSES[record_number+1]
		elif record_number == 2:
			status = order_items["STATUS"]
		else:
			status = STATUSES[record_number]

		if status == STATUSES[0] or status == STATUSES[1]:
			volume_fill = 0
		else:
			volume_fill = order_items["VOLUME_FILL"]

		record = [
			order_items["ID"], order_items["SIDE"], 
			order_items["INSTRUMENT"], status, 
			order_items["PX_INIT"], order_items["PX_FILL"], 
			order_items["VOLUME_INIT"], volume_fill, 
			order_items["NOTE"], order_items["TAGS"], 
			order_items["DATE"][record_number],
		]

		order.append(record)

	return order
