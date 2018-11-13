from typing import List


class LotterySpecification:
    def __init__(self, alpha: int, beta: int, c: int, epsilon: int):
        assert(epsilon <= beta)
        self.alpha = alpha
        self.beta = beta
        self.c = c
        self.epsilon = epsilon


class RedBlueLottery:
    HIGH = 0
    LOW = 1
    VALUE = 0
    NUMBER = 1
    ALL_KNOWN = 1
    COMPOUND_RISK = 2
    AMBIGUITY = 3
    BET_HIGH_RED = 0
    BET_HIGH_BLUE = 1

    def __init__(self, lid: int, ltype: int, total: int, matrix: List, min_cutoff: int, max_cutoff: int):
        self.lid = lid
        self.ltype = ltype
        self.total = total
        self.matrix = matrix
        self.max_cutoff = max_cutoff
        self.min_cutoff = min_cutoff

    @property
    def high_value(self):
        return self.matrix[RedBlueLottery.VALUE][RedBlueLottery.HIGH]

    @property
    def low_value(self):
        return self.matrix[RedBlueLottery.VALUE][RedBlueLottery.LOW]

    @property
    def number_red(self):
        assert self.ltype == RedBlueLottery.ALL_KNOWN or self.ltype == RedBlueLottery.AMBIGUITY
        return self.matrix[RedBlueLottery.NUMBER][RedBlueLottery.HIGH]

    @property
    def number_blue(self):
        assert self.ltype == RedBlueLottery.ALL_KNOWN
        return self.matrix[RedBlueLottery.NUMBER][RedBlueLottery.LOW]

    def has_number_blue(self):
        return self.ltype == RedBlueLottery.ALL_KNOWN

    def has_number_red(self):
        return self.ltype == RedBlueLottery.ALL_KNOWN or self.ltype == RedBlueLottery.AMBIGUITY

    def __str__(self):
        return 'RedBlueLottery ' % self.lid

    def __rpr__(self):
        return "RedBlueLottery: {}, Type: {}".format(self.lid, self.ltype)

