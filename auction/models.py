from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import LotterySpecification
from experiment.participant import Participant
from experiment.auction import Auction


class Constants(BaseConstants):
    name_in_url = 'auction'
    players_per_group = 4
    rounds_per_lottery = 2
    num_rounds = 4


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()

        if self.round_number == 1:
            lottery_specs = [
                LotterySpecification(1, 5, 0.5, 2),
                LotterySpecification(10, 20, 0.5, 2)]
            for player in self.get_players():
                Participant.set_experiment(player, Auction(Constants.rounds_per_lottery, lottery_specs))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
