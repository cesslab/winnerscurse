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
    lottery_types = [
        LotterySpecification(30, 90, 60, 4),
        LotterySpecification(10, 70, 40, 4),
        LotterySpecification(30, 90, 40, 4),
        LotterySpecification(10, 70, 60, 4),
    ]
    num_rounds = len(lottery_types)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    expected_value = models.FloatField(blank=False)
