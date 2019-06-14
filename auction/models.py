import math
import random
from typing import List

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import LotterySpecification, Lottery

doc = """
Phase 1: Auction Phase: Set to 80 rounds, 10 for each lottery.
"""


class Constants(BaseConstants):
    name_in_url = 'auction'
    players_per_group = None
    rounds_per_lottery = 2  # 10
    num_lottery_types = 8
    num_rounds = rounds_per_lottery * num_lottery_types
    lottery_types = [
        LotterySpecification(30, 90, 60, 4),
        LotterySpecification(10, 70, 40, 4),
        LotterySpecification(30, 90, 40, 4),
        LotterySpecification(10, 70, 60, 4),
        LotterySpecification(30, 90, 60, 8),
        LotterySpecification(10, 70, 40, 8),
        LotterySpecification(30, 90, 40, 8),
        LotterySpecification(10, 70, 60, 8),
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():  # type: Group
            if self.round_number == 1:
                # Get and save the order in which the lottery types should be viewed
                player.participant.vars["lottery_type_order"] = []
                for l in range(1, Constants.num_lottery_types + 1):
                    player.participant.vars["lottery_type_order"].append(int(self.session.config["lottery_{}".format(l)].strip()))

                player.payment_round = random.randint(1, Constants.num_rounds)
                player.participant.vars["payment_round"] = player.payment_round
                lotteries = [[] for i in range(Constants.num_lottery_types)]
                for l in range(Constants.num_lottery_types):
                    for r in range(Constants.rounds_per_lottery):
                        lotteries[l].append(Lottery(Constants.lottery_types[l], self.session.config['treatment']))
                # set the player's lotteries
                player.participant.vars["lotteries"] = lotteries

            player.set_round_lottery()

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

    def set_round_lottery(self):
        stage_number = math.floor((self.round_number - 1) / int(Constants.rounds_per_lottery))

        self.lottery_id = self.participant.vars["lottery_type_order"][stage_number]
        self.lottery_display_id = stage_number + 1
        self.treatment = self.session.config['treatment']

        round_number = (self.round_number-1) % Constants.rounds_per_lottery
        lottery = self.participant.vars["lotteries"][stage_number][round_number]

        self.alpha = lottery.alpha
        self.beta = lottery.beta
        self.epsilon = lottery.epsilon
        self.p = lottery.p
        self.value = lottery.value
        self.random_value = lottery.random_value
        self.outcome = lottery.outcome
        self.signal = lottery.signal

    def set_winning_player(self):
        self.computer_random_val = random.randint(0, 100)
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
