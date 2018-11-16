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
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q3exp = models.LongStringField()
    q4 = models.LongStringField()
    q5 = models.IntegerField(choices=[[1, 'I prefer lottery A.'], [2, 'I prefer lottery B.'], [3, 'I don\'t care.']], widget=widgets.RadioSelect)
    q5exp = models.LongStringField()
    q6 = models.IntegerField(choices=[[1, 'I prefer lottery A.'], [2, 'I prefer lottery B.'], [3, 'I don\'t care.']], widget=widgets.RadioSelect)
    q6exp = models.LongStringField()
    q7 = models.IntegerField()
    q8 = models.IntegerField()
    q9 = models.IntegerField()

