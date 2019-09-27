import math
import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import LotterySpecification, Lottery
from auction.models import Constants as AuctionConstants

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
        # LotterySpecification(30, 90, 60, 8),
        # 6
        # LotterySpecification(10, 70, 40, 8),
        # 7
        # LotterySpecification(30, 90, 40, 8),
        # 8
        # LotterySpecification(10, 70, 60, 8),
    ]
    num_rounds = num_lottery_types


class Subsession(BaseSubsession):
    def creating_session(self):
        treatment = self.session.config['treatment']
        for player in self.get_players():  # type: Group
            if self.round_number == 1:
                player.participant.vars["phase_one_lottery_order"] = []
                player.participant.vars["phase_one_lotteries"] = []
                for lid in range(1, Constants.num_lottery_types + 1):
                    lottery_id = int(self.session.config["lottery_{}".format(lid)].strip())
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
    winner = models.BooleanField()
    payoff = models.IntegerField()

    pass_code = models.IntegerField(blank=True)

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
        # If the player's bid is equal to the random lottery price, a coin is flipped to break the tie.
        if self.expected_value >= self.computer_random_val:
            self.payoff = self.outcome - self.computer_random_val
            self.winner = True
        # The Player's valuation is lower than the computers
        else:
            self.payoff = 0
            self.winner = False

    def set_payoffs(self):
        part_1_2_payment_round = self.participant.vars["part_1_2_payment_round"]
        if part_1_2_payment_round == self.round_number + AuctionConstants.num_rounds:
            self.participant.vars['auction_data'] = {
                'phase': 2,
                'winner': self.winner,
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
                'part_1_2_payment_round': part_1_2_payment_round,
                'display_round_number': self.round_number + AuctionConstants.num_rounds,
                'round_number': self.round_number,
                'total_payoff': self.payoff + c(self.session.config['endowment_tokens']),
            }




