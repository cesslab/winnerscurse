import math
import random
from typing import List

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django import forms
from experiment.lottery import LotterySpecification, Lottery

doc = """
Phase 1: Auction Phase: Set to 80 rounds, 10 for each lottery.
"""


class Constants(BaseConstants):
    name_in_url = 'auction'
    players_per_group = None
    rounds_per_lottery = 10  # 10
    num_lottery_types = 8
    num_part_one_rounds = 4
    num_rounds = num_lottery_types + rounds_per_lottery * num_lottery_types
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
                player.participant.vars["lottery_display_type"] = 1
                player.participant.vars["lottery_type_order"] = []
                # Get all of the lottery types
                for l in range(1, Constants.num_lottery_types + 1):
                    player.participant.vars["lottery_type_order"].append(int(self.session.config["lottery_{}".format(l)].strip()))

                lotteries = []
                for l in range(Constants.num_lottery_types):
                    lottery_type = Constants.lottery_types[player.participant.vars["lottery_type_order"][l] - 1]
                    lotteries.append(Lottery(lottery_type, self.session.config['treatment']))
                    for r in range(Constants.rounds_per_lottery):
                        lotteries.append(Lottery(lottery_type, self.session.config['treatment']))
                # set the player's lotteries
                player.participant.vars["lotteries"] = lotteries

            player.set_round_lottery()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bid = models.IntegerField()

    treatment = models.StringField(choices=['cp', 'cv'])
    part_1_2_payment_round = models.IntegerField()

    # BDM
    computer_random_val = models.IntegerField()
    tie = models.BooleanField(default=False)
    winner = models.BooleanField()
    payoff = models.IntegerField()

    # Lottery values
    lottery_id = models.IntegerField()
    lottery_display_type = models.IntegerField()
    alpha = models.IntegerField()
    beta = models.IntegerField()
    c = models.IntegerField()
    p = models.IntegerField()
    epsilon = models.IntegerField()
    signal = models.IntegerField()
    value = models.IntegerField()
    random_value = models.IntegerField()
    outcome = models.IntegerField()
    pass_code = models.IntegerField(blank=True)

    # Quiz 2
    q3 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"))), )
    q4 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"))), )

    def set_round_lottery(self):
        stage_number = math.floor((self.round_number - 1) / (Constants.rounds_per_lottery + 1)) + 1

        self.lottery_id = self.participant.vars["lottery_type_order"][stage_number - 1]
        self.treatment = self.session.config['treatment']

        lottery = self.participant.vars["lotteries"][self.round_number - 1]

        self.lottery_display_type = stage_number
        self.alpha = lottery.alpha
        self.beta = lottery.beta
        self.epsilon = lottery.epsilon
        self.p = lottery.p
        self.c = lottery.c
        self.value = lottery.value
        self.random_value = lottery.random_value
        self.outcome = lottery.outcome
        self.signal = lottery.signal

    def becker_degroot_marschak_payment_method(self):
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

    def set_payoffs(self, phase, stage):
        part_1_2_payment_round = self.participant.vars["part_1_2_payment_round"]
        display_round_number = self.round_number + Constants.num_part_one_rounds

        print("Phase {} Stage {} Round: {}, payment round: {}".format(phase, stage, display_round_number, part_1_2_payment_round))
        if display_round_number == part_1_2_payment_round:
            print("Saving payment: for phase {}, stage {}, round {}".format(phase, stage, display_round_number))
            self.participant.vars['auction_data'] = {
                'phase': phase,
                'stage': stage,
                'winner': self.winner,
                'bid': self.bid, # different
                'computer_random_val': self.computer_random_val,
                'signal': self.signal,
                'alpha': self.alpha,
                'beta': self.beta,
                'p': self.p,
                'comp_p': 100 - self.p,
                'treatment': self.treatment,
                'value': self.value,
                'outcome': self.outcome,
                'payoff': self.payoff,
                'part_1_2_payment_round': part_1_2_payment_round,
                'lottery_display_type': self.lottery_display_type,
                'round_number': part_1_2_payment_round,
                'tie': self.tie
            }
