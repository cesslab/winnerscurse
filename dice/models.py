from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'dice'
    players_per_group = None
    num_rounds = 6
    passcode = 2600


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bet = models.IntegerField(blank=False)
    cutoff = models.FloatField(blank=False)
    clicked = models.IntegerField()
    lottery = models.IntegerField(blank=False)
    die_side = models.IntegerField()
    pass_code = models.IntegerField(blank=True)
