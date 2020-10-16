import math
import random
from typing import List

from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from django import forms
from experiment.lottery import LotterySpecification, Lottery

doc = """
Phase 1: Auction Phase: Set to 80 rounds, 10 for each lottery.
"""


class Constants(BaseConstants):
    name_in_url = "lottery"
    players_per_group = None
    rounds_per_lottery = 10  # 10
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
                # --------------------------------------------------
                #  Random payoff determination for phase one and two
                # --------------------------------------------------
                total_rounds = Constants.num_rounds
                player.participant.vars["part_1_2_payment_round"] = random.randint(
                    1, total_rounds
                )

                # Get and save the order in which the lottery types should be viewed
                player.participant.vars["lottery_display_type"] = 1
                player.participant.vars["lottery_type_order"] = []

                # Get all of the lottery types
                for l in range(1, Constants.num_lottery_types + 1):
                    player.participant.vars["lottery_type_order"].append(
                        int(self.session.config["lottery_{}".format(l)].strip())
                    )

                lotteries = []
                for l in range(Constants.num_lottery_types):
                    lottery_type = Constants.lottery_types[
                        player.participant.vars["lottery_type_order"][l] - 1
                    ]
                    lotteries.append(
                        Lottery(lottery_type, self.session.config["treatment"])
                    )
                    for r in range(Constants.rounds_per_lottery):
                        lotteries.append(
                            Lottery(lottery_type, self.session.config["treatment"])
                        )
                # set the player's lotteries
                player.participant.vars["lotteries"] = lotteries

            player.set_round_lottery()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bid = models.IntegerField()

    treatment = models.StringField(choices=["cp", "cv"])
    part_1_2_payment_round = models.IntegerField()

    # BDM
    computer_random_val = models.IntegerField()
    winner = models.BooleanField()

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

    # Quiz 1
    q1 = models.StringField(
        widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"))),
    )
    q2 = models.StringField(
        widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"))),
    )

    # Quiz 2
    q3 = models.StringField(
        widget=forms.CheckboxSelectMultiple(
            choices=(("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"))
        ),
    )
    q4 = models.StringField(
        widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"))),
    )

    def set_round_lottery(self):
        stage_number = (
            math.floor((self.round_number - 1) / (Constants.rounds_per_lottery + 1)) + 1
        )

        self.lottery_id = self.participant.vars["lottery_type_order"][stage_number - 1]
        self.treatment = self.session.config["treatment"]

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
        # random lottery price
        self.computer_random_val = random.randint(0, 100)
        if self.bid >= self.computer_random_val:
            self.payoff = c(self.outcome - self.computer_random_val)
            self.winner = True
        # lose
        else:
            self.payoff = c(0)
            self.winner = False

    def set_payoffs(self, phase, stage):
        """
        Note: The first and second app, in this case auction and expected, are referred to as phase 1 and 2, respectively.
                 The auction app itself consists of two phases:
                    - Stage 1: No signal (one round per each lottery type)
                    - Stage 2: With signal (rounds_per_lottery rounds per each lottery type)
        """
        part_1_2_payment_round = self.participant.vars["part_1_2_payment_round"]

        if self.round_number == part_1_2_payment_round:
            self.participant.vars["auction_data"] = {
                "phase": phase,
                "stage": stage,
                "winner": self.winner,
                "bid": self.bid,  # different
                "computer_random_val": self.computer_random_val,
                "signal": self.signal,
                "alpha": self.alpha,
                "beta": self.beta,
                "p": self.p,
                "comp_p": 100 - self.p,
                "treatment": self.treatment,
                "value": self.value,
                "outcome": self.outcome,
                "payoff": self.payoff,
                "part_1_2_payment_round": part_1_2_payment_round,
                "lottery_display_type": self.lottery_display_type,
                "display_round_number": self.round_number,
                "round_number": self.round_number,
                "total_payoff": self.payoff + c(self.session.config["endowment_tokens"]),
                "endowment": c(self.session.config["endowment_tokens"]),
            }
