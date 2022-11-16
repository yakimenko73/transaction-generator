from enum import Enum


class OrderSide(Enum):
    UNRECOGNIZED = 0
    SELL = 1
    BUY = 2


class OrderInstrument(Enum):
    UNRECOGNIZED = 0
    EURGBP = 1
    EURCHF = 2
    EURCAD = 3
    AUDEUR = 4
    EURNZD = 5
    EURJPY = 6
    GBPJPY = 7
    CHFJPY = 8
    AUDJPY = 9
    GBPCAD = 10
    EURRUB = 11


class OrderInstrumentBuyPrice(Enum):
    UNRECOGNIZED = 0
    EURGBP = 0.88491
    EURCHF = 1.08052
    EURCAD = 1.55111
    AUDEUR = 0.629698
    EURNZD = 1.68618
    EURJPY = 127.09323
    GBPJPY = 143.51412
    CHFJPY = 117.5189
    AUDJPY = 80.03001
    GBPCAD = 1.75086
    EURRUB = 91.99600


class OrderInstrumentSellPrice(Enum):
    UNRECOGNIZED = 0
    EURGBP = 0.88473
    EURCHF = 1.02197
    EURCAD = 1.41313
    AUDEUR = 0.62963
    EURNZD = 1.68501
    EURJPY = 124.88801
    GBPJPY = 143.23002
    CHFJPY = 116.89021
    AUDJPY = 80.00315
    GBPCAD = 1.44401
    EURRUB = 91.31132


class OrderStatus(Enum):
    UNRECOGNIZED = 0
    NEW = 1
    IN_PROCESS = 2
    FILL = 3
    PARTIAL_FILL = 4
    CANCEL = 5
    DONE = 6


class OrderNote(Enum):
    UNRECOGNIZED = 0
    NOTE1 = 1
    NOTE2 = 2
    NOTE3 = 3
    NOTE4 = 4
    NOTE5 = 5
    NOTE6 = 6
    NOTE7 = 7
    NOTE8 = 8
    NOTE9 = 9


class OrderTag(Enum):
    UNRECOGNIZED = 0
    TRADE = 1
    DISTANCE_TRADE = 2
    REGULAR_TRADE = 3
    SPECIAL_TRADE = 4
    TRANSFER = 5
