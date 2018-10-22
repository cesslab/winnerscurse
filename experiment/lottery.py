import random


class LotterySpecification:
    def __init__(self, alpha: int, beta: int, p: float, epsilon: int):
        assert(epsilon <= beta)
        self.alpha = alpha
        self.beta = beta
        self.p = p
        self.epsilon = epsilon


class Lottery:
    def __init__(self, spec: LotterySpecification):
        self.value = random.randint(spec.alpha, spec.beta)
        self.low_signal = self.value - spec.epsilon
        self.high_signal = self.value + spec.epsilon

        self.r1 = random.random()
        if self.r1 <= (1 - spec.p):
            self.outcome = 0
        else:
            self.outcome = self.value
