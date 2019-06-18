import math
import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import LotterySpecification, Lottery
from auction.models import Constants as AuctionConstants
from django import forms

author = 'Anwar A. Ruff'

doc = """
Expected Value
"""


class Constants(BaseConstants):
    name_in_url = 'expected'
    players_per_group = None
    num_lottery_types = 4
    lottery_types = [
        # 1
        LotterySpecification(30, 90, 60, 4),
        # 2
        LotterySpecification(10, 70, 40, 4),
        # 3
        LotterySpecification(30, 90, 40, 4),
        # 4
        LotterySpecification(10, 70, 60, 4),
        # 5
        LotterySpecification(30, 90, 60, 8),
        # 6
        LotterySpecification(10, 70, 40, 8),
        # 7
        LotterySpecification(30, 90, 40, 8),
        # 8
        LotterySpecification(10, 70, 60, 8),
    ]
    num_rounds = 4


class Subsession(BaseSubsession):
    def creating_session(self):
        treatment = self.session.config['treatment']
        for player in self.get_players():  # type: Group
            if self.round_number == 1:
                # --------------------------------------------------
                #  Random payoff determination for phase one and two
                # --------------------------------------------------
                num_phase_one_valuations = Constants.num_lottery_types
                num_phase_two_stage_one_valuations = AuctionConstants.num_lottery_types
                num_phase_two_stage_two_valuations = AuctionConstants.num_rounds
                total_rounds = num_phase_one_valuations + num_phase_two_stage_one_valuations + num_phase_two_stage_two_valuations
                rround = random.randint(1, total_rounds)
                player.participant.vars["part_1_2_payment_round"] = rround
                print("Payment: payment round = {}".format(rround))

                player.participant.vars["phase_one_lottery_order"] = []
                player.participant.vars["phase_one_lotteries"] = []
                for l in range(1, Constants.num_lottery_types + 1):
                    lottery_id = int(self.session.config["lottery_{}".format(l)].strip())
                    lottery_type = Constants.lottery_types[lottery_id-1]
                    player.participant.vars["phase_one_lottery_order"].append(lottery_id)
                    player.participant.vars["phase_one_lotteries"].append(Lottery(lottery_type, treatment, with_signal=False))

            player.set_round_lottery()



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    expected_value = models.FloatField(blank=False)
    treatment = models.StringField(choices=['cp', 'cv'])

    # Lottery values
    lottery_id = models.IntegerField()
    alpha = models.IntegerField()
    beta = models.IntegerField()
    epsilon = models.IntegerField()
    c = models.IntegerField()
    p = models.IntegerField()
    value = models.IntegerField()
    random_value = models.IntegerField()
    outcome = models.IntegerField()

    # BDM
    computer_random_val = models.IntegerField()
    tie = models.BooleanField()
    winner = models.BooleanField()
    payoff = models.IntegerField()

    # Quiz
    q1 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"))), )
    q2 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"))), )

    def set_round_lottery(self):
        self.treatment = self.session.config['treatment']

        lottery = self.participant.vars["phase_one_lotteries"][self.round_number-1]
        self.lottery_id = self.participant.vars["phase_one_lottery_order"][self.round_number-1]
        self.alpha = lottery.alpha
        self.beta = lottery.beta
        self.epsilon = lottery.epsilon
        self.c = lottery.c
        self.p = lottery.p
        self.c = lottery.c
        self.value = lottery.value
        self.random_value = lottery.random_value
        self.outcome = lottery.outcome

    def becker_degroot_marschak_payment_method(self):
        self.computer_random_val = random.randint(0, 100)
        # The Player's valuation is the same as the computers, and a coin is flipped to break the tie
        if self.expected_value == self.computer_random_val:
            winner = random.randint(1, 2)
            # The player wins the coin toss
            if winner == 1:
                self.payoff = self.outcome - self.computer_random_val
                self.winner = True
                self.tie = True
            # The player loses the coin toss
            else:
                self.payoff = 0
                self.winner = False
                self.tie = True
        # The Player's valuation is greater than computer, and she wins the lottery
        if self.expected_value > self.computer_random_val:
            self.payoff = self.outcome - self.computer_random_val
            self.winner = True
            self.tie = False
        # The Player's valuation is lower than the computers
        else:
            self.payoff = 0
            self.winner = False
            self.tie = False

    def set_payoffs(self):
        part_1_2_payment_round = self.participant.vars["part_1_2_payment_round"]
        print("Phase 1 Test: payment round {} == current round {}".format(part_1_2_payment_round, self.round_number))
        if part_1_2_payment_round == self.round_number:
            print("Saving payment for phase 1 round {}".format(part_1_2_payment_round))
            self.participant.vars['auction_data'] = {
                'phase': 1,
                'winner': None,
                'bid': self.expected_value, # different
                'computer_random_val': self.random_value,
                'alpha': self.alpha,
                'beta': self.beta,
                'p': self.p,
                'comp_p': 100 - self.p,
                'treatment': self.treatment,
                'value': self.value,
                'outcome': self.outcome,
                'payoff': self.payoff,
                'part_1_2_payment_round': self.round_number,
                'round_number': self.round_number,
                'display_round_number': self.round_number,
                'tie': self.tie
            }




