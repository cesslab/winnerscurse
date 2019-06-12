import math
import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import LotterySpecification, Lottery

author = 'Anwar A. Ruff'

doc = """
Expected Value
"""


class Constants(BaseConstants):
    name_in_url = 'expected'
    players_per_group = None
    num_lottery_types = 8
    rounds_per_lottery = 10
    num_rounds = num_lottery_types
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
        if self.round_number == 1:
            for player in self.get_players():
                # Get and save the order in which the lottery types should be viewed
                player.participant.vars["lottery_type_order"] = []
                for l in range(1, Constants.num_lottery_types + 1):
                    player.participant.vars["lottery_type_order"].append(int(self.session.config["lottery_{}".format(i)].strip()))

                player.payment_round = random.randint(1, Constants.num_rounds)
                player.participant.vars["payment_round"] = player.payment_round
                lotteries = []
                for l in range(Constants.num_lottery_types):
                    lotteries.append([])
                    for r in range(Constants.rounds_per_lottery):
                        lotteries[l].append(Lottery(Constants.lottery_types[l], self.session.config['treatment']))
                # set the player's lotteries
                player.participant.vars["lotteries"] = lotteries


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    expected_value = models.FloatField(blank=False)
