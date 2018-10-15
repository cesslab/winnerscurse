from random import random


class LotterySpecification:
    def __init__(self, alpha: int, beta: int, p: float, epsilon: float):
        self.alpha = alpha
        self.beta = beta
        self.p = p
        self.epsilon = epsilon

