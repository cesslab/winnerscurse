import random


class LotterySpecification:
    def __init__(self, alpha: int, beta: int, p: float, epsilon: float):
        self.alpha = alpha
        self.beta = beta
        self.p = p
        self.epsilon = epsilon


class Lottery:
    def __init__(self, spec: LotterySpecification):
        # random value used to determine whether the value will be zero
        # or a value between alpha and beta, inclusively.
        self.r1 = random.random()
        self.r2 = random.randint(spec.alpha, spec.beta)
        if self.r1 <= (1 - spec.p):
            self.value = 0
        else:
            self.value = self.r2

        self.low_signal = self.value - spec.epsilon
        self.high_signal = self.value + spec.epsilon
