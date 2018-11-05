import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import RedBlueLottery


class Constants(BaseConstants):
    name_in_url = 'payoff'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_id = models.IntegerField()
    lottery_type = models.IntegerField()
    random_cutoff = models.FloatField()
    random_chip_id = models.IntegerField()
    num_red_chips = models.IntegerField()
    total_chips = models.IntegerField()
    red_chosen = models.BooleanField()
    phase_two_earnings = models.FloatField()
    earnings = models.FloatField()
    realized_value = models.FloatField()
    play_lottery = models.BooleanField()

    def player_dice_phase_payoffs(self):
        lottery: RedBlueLottery = self.participant.vars["red_blue_lottery"]
        self.task_id = self.participant.vars["die_side"]
        self.random_cutoff = random.randint(lottery.min_cutoff, lottery.max_cutoff)

        self.play_lottery = self.random_cutoff < self.participant.vars["cutoff"]

        if not self.play_lottery:
            self.earnings = float(self.random_cutoff)

        self.lottery_type = lottery.ltype
        if self.lottery_type == RedBlueLottery.ALL_KNOWN:
            self.random_chip_id = random.randint(1, lottery.total)
            self.num_red_chips = lottery.number_red
            self.total_chips = lottery.total
            self.red_chosen = self.random_chip_id <= self.num_red_chips

        elif self.lottery_type == RedBlueLottery.COMPOUND_RISK:
            self.num_red_chips = random.randint(0, lottery.total)
            self.total_chips = lottery.total
            self.random_chip_id = random.randint(1, lottery.total)
            self.red_chosen = self.random_chip_id <= self.num_red_chips
        else:
            self.random_chip_id = random.randint(1, lottery.total)
            self.num_red_chips = lottery.number_red
            self.total_chips = lottery.total
            self.red_chosen = self.random_chip_id <= self.num_red_chips

        if self.red_chosen and self.participant.vars["bet"] == RedBlueLottery.BET_HIGH_RED:
            self.realized_value = lottery.high_value
        else:
            self.realized_value = lottery.low_value

        if self.play_lottery:
            self.earnings = self.realized_value

