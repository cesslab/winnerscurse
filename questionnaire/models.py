from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

doc = """
Final Questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField()
    age = models.IntegerField(min=18, max=100)
    major = models.StringField()
    q1a = models.IntegerField()
    q1b = models.IntegerField()
    q1c = models.IntegerField()
    q1d = models.IntegerField()
    q1e = models.IntegerField()
    q1exp = models.LongStringField()
    q2 = models.IntegerField(choices=[
        [1, 'I would bid less than my valuation.'],
        [2, 'I would bid my valuation.'],
        [3, 'I would bid more than my valuation']], widget=widgets.RadioSelect)
    q2exp = models.LongStringField()
    q3 = models.IntegerField()
    q4 = models.IntegerField(choices=[
        [1, 'I prefer lottery A.'], [2, 'I prefer lottery B.'], [3, 'I don\'t care.']], widget=widgets.RadioSelect)
    q4exp = models.LongStringField()
    q5 = models.IntegerField()
    q6 = models.IntegerField()
    q7 = models.IntegerField()
