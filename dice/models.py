from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import RedBlueLottery

doc = """
Phase 2: Dice Phase, for lack of a better description. 
"""

class Constants(BaseConstants):
    name_in_url = 'dice'
    players_per_group = None
    num_rounds = 6
    passcode = 2600
    LOTTERIES = {
        1: {
            'id': 1,
            'type': 1,
            'matrix': [[100, 0], [10, 10]],
            'total': 20,
            'min': 0,
            'max': 100
        },
        2: {
            'id': 2,
            'type': 2,
            'matrix': [[100, 0], []],
            'total': 20,
            'min': 0,
            'max': 100
        },
        3: {
            'id': 3,
            'type': 3,
            # Type 3 will have an fixed number specified for red, but it will not be displayed to the subjects
            'matrix': [[100, 0], [17, -1]],
            'total': 20,
            'min': 0,
            'max': 100
        },
        4: {
            'id': 4,
            'type': 1,
            'matrix': [[150, 0], [15, 15]],
            'total': 30,
            'min': 0,
            'max': 150
        },
        5: {
            'id': 5,
            'type': 2,
            'matrix': [[150, 0], []],
            'total': 30,
            'min': 0,
            'max': 150
        },
        6: {
            'id': 6,
            'type': 3,
            'matrix': [[150, 0], [15, -1]],
            'total': 30,
            'min': 0,
            'max': 150
        },
    }


class Subsession(BaseSubsession):
    def creating_session(self):
        lotteries = {}
        for lid, params in Constants.LOTTERIES.items():
            lotteries[lid] = RedBlueLottery(
                lid=params['id'],
                ltype=params['type'],
                total=params['total'],
                matrix=params['matrix'],
                min_cutoff=params['min'],
                max_cutoff=params['max'],
            )
        for player in self.get_players():
            player.participant.vars['RedBlueLotteries'] = lotteries
            player.participant.vars['die_labels'] = ['B', 'A', 'C', 'E', 'F', 'D']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bet = models.IntegerField(blank=False)
    cutoff = models.FloatField(blank=False)
    clicked = models.IntegerField()
    lottery = models.IntegerField(blank=False)
    die_side = models.IntegerField()
    pass_code = models.IntegerField(blank=True)
