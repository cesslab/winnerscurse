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
    valuation = models.IntegerField()
    bid = models.IntegerField()

    treatment = models.StringField(choices=['cp', 'cv'])
    payment_round = models.IntegerField()

    # BDM
    computer_random_val = models.IntegerField()
    tie = models.BooleanField(default=False)
    winner = models.BooleanField()
    payoff = models.IntegerField()

    # Lottery values
    lottery_id = models.IntegerField()
    lottery_display_id = models.IntegerField()
    alpha = models.IntegerField()
    beta = models.IntegerField()
    c = models.IntegerField()
    p = models.IntegerField()
    epsilon = models.IntegerField()
    signal = models.IntegerField()
    value = models.IntegerField()
    random_value = models.IntegerField()
    outcome = models.IntegerField()

    # Quiz 2
    q3 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"))), )
    q4 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"))), )

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
        self.c = lottery.c
        self.value = lottery.value
        self.random_value = lottery.random_value
        self.outcome = lottery.outcome
        self.signal = lottery.signal

    def becker_degroot_marschak_payment_method(self, valuation):
        self.computer_random_val = random.randint(0, 100)
        if valuation == self.computer_random_val:
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
        if valuation > self.computer_random_val:
            self.payoff = self.outcome - self.computer_random_val
            self.winner = True
            self.tie = False
        # lose
        else:
            self.payoff = self.computer_random_val - self.computer_random_val
            self.winner = False
            self.tie = False

    def set_payoffs(self):
        payment_phase = self.participant.vars["payment_phase"]
        payment_stage = self.participant.vars["payment_stage"]
        payment_round = self.participant.vars["payment_round"]
        if payment_phase == 2:
            print("Phase 2 Stage 1 and 2 Test: payment round {} == current round {}".format(payment_round, self.round_number))
            if payment_stage == 1 and payment_round == self.round_number:
                print("Saving payment: for phase 2, stage 1, round {}".format(payment_round))
                self.participant.vars['auction_data'] = {
                    'phase': 2,
                    'stage': 1,
                    'winner': self.winner,
                    'bid': self.valuation, # different
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
                    'lottery_display_id': self.lottery_display_id,
                    'round_number': self.round_number,
                    'tie': self.tie
                }
            elif payment_stage == 2 and payment_round == self.round_number:
                print("Saving payment: for phase 2, stage 2, round {}".format(payment_round))
                self.participant.vars['auction_data'] = {
                    'phase': 2,
                    'stage': 2,
                    'winner': self.winner,
                    'bid': self.bid,
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
                    'lottery_display_id': self.lottery_display_id,
                    'round_number': self.round_number,
                    'tie': self.tie
                }

