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
			list_instruments.append(INSTRUMENTS[10][0])

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
		seed = math.ceil(seed/rounding_number) * rounding_number - rounding_number

		list_volumes.append(seed)

	return list_volumes


def volumefill_generator(a, c, seeds, statuses_on_broker, init_volumes):
	list_volumes = []
	rounding_number = 1000

	for i in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[i], 16) + c) % init_volumes[i]
		seed = math.ceil(seed/rounding_number) * rounding_number - rounding_number

		if statuses_on_broker[i] == STATUSES[2][1]:
			fill_volume = init_volumes[i] - seed
		elif statuses_on_broker[i] == STATUSES[2][2]:
			fill_volume = 0
		else:
			fill_volume = init_volumes[i]

		list_volumes.append(fill_volume)

	return list_volumes


def date_generator(m, a, c, seed, start_date):
	date = dt.datetime.strptime(start_date, '%d.%m.%Y %H:%M:%S.%f')
	list_dates = []

	for order_number in range(MAX_NUMBER_ORDERS):
		dates_for_order = []
		if order_number < 599:
			number_dates = NUMBER_RECORDS_FOR_FIRST_SEGMENT
		elif order_number >= 600 and order_number <= 1799:
			number_dates = NUMBER_RECORDS_FOR_SECOND_SEGMENT
		else:
			number_dates = NUMBER_RECORDS_FOR_THIRD_SEGMENT

		for record_number in range(number_dates):
			seed = (a * seed + c) % m

			date = date + dt.timedelta(milliseconds=seed)

			dates_for_order.append(date.strftime('%d.%m.%Y %H:%M:%S.%f')[:-3])
		
		list_dates.append(dates_for_order)

	return list_dates


def note_generator(m, a, c, seeds):
	list_notes = []

	for i in range(MAX_NUMBER_ORDERS):
		seed = (a * int(seeds[i], 16) + c) % m
		try:
			list_notes.append(NOTES[seed-1])
		except IndexError:
			list_notes.append(NOTES[10])

	return list_notes


def generate_attributes(parameters):
	id_ = id_generator(*parameters["IDSettings"].values())
	sides = side_generator(*parameters["SideSettings"].values(), id_)
	instruments = instrument_generator(*parameters["InstrumentSettings"].values(), id_)
	statuses_on_broker = status_generator(*parameters["StatusSettings"].values(), id_)
	init_prices = pxinit_generator(instruments, sides)
	fill_prices = pxfill_generator(
		*parameters["PXFillSettings"].values(), 
		id_, 
		init_prices
	)
	init_volumes = volumeinit_generator(*parameters["VolumeInitSettings"].values())
	fill_volumes = volumefill_generator(
		*parameters["VolumeFillSettings"].values(), 
		id_, 
		statuses_on_broker, 
		init_volumes
	)
	notes = note_generator(*parameters["NoteSettings"].values(), id_)
	dates = date_generator(*parameters["DateSettings"].values())

	return id_, sides, instruments, statuses_on_broker, init_prices, fill_prices, init_volumes, fill_volumes, notes, dates


def create_list_orders(parameters):
	list_orders = []

	attributes = generate_attributes(parameters)

	for i in range(MAX_NUMBER_ORDERS):
		if i < 599:
			number_records = NUMBER_RECORDS_FOR_FIRST_SEGMENT
			is_first_segment = True
		elif i >=600 and i <=1799:
			number_records = NUMBER_RECORDS_FOR_SECOND_SEGMENT
			is_first_segment = False
		else:
			number_records = NUMBER_RECORDS_FOR_THIRD_SEGMENT
			is_first_segment = False

		order = create_order(attributes[0][i],
			attributes[1][i],
			attributes[2][i],
			attributes[3][i],
			attributes[4][i],
			attributes[5][i],
			attributes[6][i],
			attributes[7][i],
			attributes[8][i],
			dates=attributes[9][i],
			number_records=number_records,
			is_first_segment=is_first_segment,
		)

		list_orders.append(order)

	return list_orders

def create_order(*attributes, dates, number_records, is_first_segment):
	order = []
	id_, side, instrument, status_on_broker, init_price, fill_price, init_volume, fill_volume, note = attributes

	for record_number in range(number_records):
		record = []
		if number_records == NUMBER_RECORDS_FOR_FIRST_SEGMENT \
		and is_first_segment:
			if record_number == 1:
				status = status_on_broker
			else:
				status = STATUSES[record_number+1]

			if status == STATUSES[0] or status == STATUSES[1]:
				fvolume = 0
			else:
				fvolume = fill_volume
		elif number_records == NUMBER_RECORDS_FOR_SECOND_SEGMENT \
		or number_records == NUMBER_RECORDS_FOR_THIRD_SEGMENT:
			if record_number == 2:
				status = status_on_broker
			else:
				status = STATUSES[record_number]

			if status == STATUSES[0] or status == STATUSES[1]:
				fvolume = 0
			else:
				fvolume = fill_volume

		record = [
			id_, side, 
			instrument, status, 
			init_price, fill_price, 
			init_volume, fvolume, 
			note, dates[record_number]
		]

		order.append(record)

	return order