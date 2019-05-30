import math
import random
from typing import List

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import LotterySpecification

doc = """
Phase 1: Auction Phase: Set to 80 rounds, 10 for each lottery.
"""

class Constants(BaseConstants):
    name_in_url = 'auction'
    players_per_group = None
    rounds_per_lottery = 10  # 10
    lotteries = [
        LotterySpecification(30, 90, 60, 4),
        LotterySpecification(10, 70, 40, 4),
        LotterySpecification(30, 90, 40, 4),
        LotterySpecification(10, 70, 60, 4),
        LotterySpecification(30, 90, 60, 8),
        LotterySpecification(10, 70, 40, 8),
        LotterySpecification(30, 90, 40, 8),
        LotterySpecification(10, 70, 60, 8),
    ]
    num_rounds = rounds_per_lottery*len(lotteries)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    first_valuation = models.IntegerField()
    bid = models.IntegerField()
    computer_random_val = models.IntegerField()
    signal = models.IntegerField()
    tie = models.BooleanField(default=False)
    winner = models.BooleanField()
    payoff = models.IntegerField()
    payment_round = models.IntegerField()

    lottery_id = models.IntegerField()
    lottery_display_id = models.IntegerField()
    alpha = models.IntegerField()
    beta = models.IntegerField()
    p = models.IntegerField()
    epsilon = models.IntegerField()
    value = models.IntegerField()
    random_value = models.IntegerField()
    outcome = models.IntegerField()
    treatment = models.StringField(choices=['cp', 'cv'])

    def set_computer_bid(self):
        self.computer_random_val = random.randint(0, 100)

    def get_treatment(self):
        treatment = self.session.config['treatment']
        if treatment != 'cp' and treatment != 'cv':
            treatment = 'cp'
        return treatment

    def set_round_lottery(self):
        lottery_order = []
        num_lotteries = len(Constants.lotteries)
        for i in range(1, num_lotteries + 1):
            lottery_order.append(int(self.session.config["lottery_{}".format(i)].strip()))
        rounds_per_lottery = int(Constants.rounds_per_lottery)
        lottery_index_this_round = math.floor((self.round_number - 1) / rounds_per_lottery)
        self.lottery_id = lottery_order[lottery_index_this_round]
        self.lottery_display_id = lottery_index_this_round + 1

        self.treatment = self.get_treatment()

        lottery_spec: LotterySpecification = Constants.lotteries[self.lottery_id - 1]

        self.alpha = lottery_spec.alpha
        self.beta = lottery_spec.beta
        # epsilon is used to determine the player's signal
        self.epsilon = lottery_spec.epsilon

        if self.treatment == 'cv':
            self.p = lottery_spec.c
            self.value = random.randint(self.alpha, self.beta)

            self.random_value = random.randint(0, 100)
            if self.random_value <= self.p:
                self.outcome = self.value
            else:
                self.outcome = 0
        else:
            self.p = random.randint(self.alpha, self.beta)
            self.value = lottery_spec.c

            self.random_value = random.randint(0, 100)
            if self.random_value <= self.p:
                self.outcome = self.value
            else:
                self.outcome = 0

    def get_signal(self):
        if self.treatment == 'cv':
            return random.randint(self.value - self.epsilon, self.value + self.epsilon)
        else:
            return random.randint(self.p - self.epsilon, self.p + self.epsilon)

    def set_first_valuation_outcome(self):
        pass
        # print(self.computer_random_val)
        # if self.bid == self.computer_random_val:
        #     # Break tie
        #     winner = random.randint(1, 2)
        #     # player wins
        #     if winner == 1:
        #         self.payoff = self.outcome - self.computer_random_val
        #         self.winner = True
        #         self.tie = True
        #     else:
        #         self.payoff = 0
        #         self.winner = False
        #         self.tie = True
        # # win the lottery ticket
        # if self.bid > self.computer_random_val:
        #     self.payoff = self.outcome - self.computer_random_val
        #     self.winner = True
        #     self.tie = False
        # # lose
        # else:
        #     self.payoff = self.computer_random_val - self.computer_random_val
        #     self.winner = False
        #     self.tie = False

    def set_winning_player(self):
        print(self.computer_random_val)
        if self.bid == self.computer_random_val:
            # Break tie
            winner = random.randint(1, 2)
            # player wins
            if winner == 1:
                self.payoff = self.outcome - self.computer_random_val
                self.winner = True
                self.tie = True
            else:
                self.payoff = 0
                self.winner = False
                self.tie = True
        # win the lottery ticket
        if self.bid > self.computer_random_val:
            self.payoff = self.outcome - self.computer_random_val
            self.winner = True
            self.tie = False
        # lose
        else:
            self.payoff = self.computer_random_val - self.computer_random_val
            self.winner = False
            self.tie = False
