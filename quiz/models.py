from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django import forms


doc = """
Quiz
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"))), )
    q2 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"))), )
    q3 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"))), )
    q4 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"))), )
    q5 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"))), )
    q6 = models.StringField(widget=forms.CheckboxSelectMultiple(choices=(("1", "1"), ("2", "2"), ("3", "3"))), )



