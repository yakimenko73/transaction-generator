from enum import Enum


class OrderSide(Enum):
    UNSPECIFIED = 0
    SELL = 1
    BUY = 2

    def __str__(self):
        return self.name


class OrderInstrument(Enum):
    UNSPECIFIED = 0
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

    def __str__(self):
        return self.name


class OrderInstrumentBuyPrice(Enum):
    UNSPECIFIED = 0
    EURGBP = 1.00229
    EURCHF = 1.88491
    EURCAD = 1.97120
    AUDEUR = 0.62000
    EURNZD = 1.992710
    EURJPY = 127.07816
    GBPJPY = 145.69532
    CHFJPY = 118.11128
    AUDJPY = 79.32006
    GBPCAD = 1.32133
    EURRUB = 89.21300


class OrderInstrumentSellPrice(Enum):
    UNSPECIFIED = 0
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
    UNSPECIFIED = 0
    NEW = 1
    IN_PROCESS = 2
    FILL = 3
    PARTIAL_FILL = 4
    CANCEL = 5
    DONE = 6

    def __str__(self):
        return self.name


class OrderNote(Enum):
    UNSPECIFIED = 0
    NOTE1 = 1
    NOTE2 = 2
    NOTE3 = 3
    NOTE4 = 4
    NOTE5 = 5
    NOTE6 = 6
    NOTE7 = 7
    NOTE8 = 8
    NOTE9 = 9

    def __str__(self):
        return self.name


class OrderTag(Enum):
    UNSPECIFIED = 0
    TRADE = 1
    DISTANCE_TRADE = 2
    REGULAR_TRADE = 3
    SPECIAL_TRADE = 4
    TRANSFER = 5

    def __str__(self):
        return self.name
