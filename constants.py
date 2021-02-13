MAX_NUMBER_ORDERS = 2000

# percentage of orders created before recording started
ORDERS_CREATED_BEFORE_RECORDING = 30

# percentage of orders that were created when the recording started
ORDERS_CREATED_AND_DONE = 60

# percentage of orders completed after the end of the recording
ORDERS_COMPLETED_AFTER_RECORDING = 10

# the number of orders to generate in each segment
MAX_LIMIT_ORDERS_FOR_FIRST_SEGMENT = 600

MAX_LIMIT_ORDERS_FOR_SECOND_SEGMENT = 1800

MAX_LIMIT_ORDERS_FOR_THIRD_SEGMENT = 2000

# the number of records to generate in each segment
NUMBER_RECORDS_FOR_FIRST_SEGMENT = 3

NUMBER_RECORDS_FOR_SECOND_SEGMENT = 4

NUMBER_RECORDS_FOR_THIRD_SEGMENT = 3

# number of unique generated tag sets
NUMBER_OF_DIFFERENT_TAGS_SETS = 13

ORDER_ATTRIBUTES = [
	'ID',
	'SIDE',
	'INSTRUMENT',
	'STATUS',
	'PX_INIT',
	'PX_FILL',
	'VOLUME_INIT',
	'VOLUME_FILL',
	'NOTE',
	'TAGS',
	'DATE',
]

SIDES = [
	"SELL",
	"BUY",
]

# title, buy price, sell price
INSTRUMENTS = [
	["EURGBP", 0.88491, 0.88473],
	["EURCHF", 1.08052, 1.02197],
	["EURCAD", 1.55111, 1.41313],
	["AUDEUR", 0.629698, 0.62963],
	["EURNZD", 1.68618, 1.68501],
	["EURJPY", 127.09323, 124.88801],
	["GBPJPY", 143.51412, 143.23002],
	["CHFJPY", 117.5189, 116.89021],
	["AUDJPY", 80.03001, 80.00315],
	["GBPCAD", 1.75086, 1.44401],
	["EURRUB", 91.99600, 91.31132],
]

STATUSES = [
	"NEW",
	"INPROCESS",
	[
		"FILL",
		"PARTIALFILL",
		"CANCEL",
	],
	"DONE",
]

NOTES = [
	"NOTE 1",
	"NOTE 2",
	"NOTE 3",
	"NOTE 4",
	"NOTE 5",
	"NOTE 6",
	"NOTE 7",
	"NOTE 8",
	"NOTE 9",
	"NOTE 10",
	"NOTE 11",
]

TAGS = [
	"TRADE",
	"DISTANCE TRADE",
	"REGULAR TRADE",
	"SPECIAL TRADE",
	"TRANSFER",
]

TRUE_LOG_LEVELS = [
	'critical', 
	'error', 
	'warning', 
	'info', 
	'debug', 
]

TRUE_FILE_MODES = [
	'r',
	'w',
	'x',
	'a',
	'b',
	't',
	'+',
]