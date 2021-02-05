def id_generator(m, a, c, seed):
	list_numbers = []

	for i in range(2000):
		seed = (a * seed + c) % m

		list_numbers.append(seed)

	return list_numbers


def side_generator(m, a, c, seed):
	list_numbers = []

	for i in range(2000):
		seed = (a * seed + c) % m

		list_numbers.append(seed)

	return list_numbers