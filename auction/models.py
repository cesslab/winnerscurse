import math
import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import LotterySpecification


class Constants(BaseConstants):
    name_in_url = 'auction'
    players_per_group = 4
    num_rounds = 4


class Subsession(BaseSubsession):
    def set_group_size(self):
        players = self.get_players()
        players_per_group = self.session.config['players_per_group']
        group_matrix = []
        for i in range(0, len(players), players_per_group):
            group_matrix.append(players[i:i + players_per_group])
        self.set_group_matrix(group_matrix)

    def creating_session(self):
        self.set_group_size()
        self.group_randomly()

        specs = [
            LotterySpecification(60, 90, .75, 4),
            LotterySpecification(10, 40, .25, 4),
            LotterySpecification(60, 90, .25, 4),
            LotterySpecification(10, 40, .75, 4),
            LotterySpecification(60, 90, .75, 8),
            LotterySpecification(10, 40, .25, 8),
            LotterySpecification(60, 90, .25, 8),
            LotterySpecification(10, 40, .75, 8),
        ]

        for group in self.get_groups():
            group.set_lottery(specs)
            for player in group.get_players():
                player.signal = group.get_signal()

        # Set the payoff relevant round
        if self.round_number == 1:
            for player in self.get_players():
                player.payment_round = random.randint(1, Constants.num_rounds)
                player.participant.vars["payment_round"] = player.payment_round


class Group(BaseGroup):
    lottery_id = models.IntegerField()
    alpha = models.IntegerField()
    beta = models.IntegerField()
    p = models.FloatField()
    epsilon = models.IntegerField()
    value = models.IntegerField()
    random_value = models.FloatField()
    outcome = models.IntegerField()
    highest_bid = models.IntegerField()

    def set_lottery(self, specs):
        rounds_per_lottery = self.session.config['rounds_per_lottery']
        self.lottery_id = math.floor((self.round_number - 1) / rounds_per_lottery)
        lottery = specs[self.lottery_id]

        self.alpha = lottery.alpha
        self.beta = lottery.beta
        self.p = lottery.p
        self.epsilon = lottery.epsilon
        self.value = random.randint(self.alpha, self.beta)

        self.random_value = random.random()
        if self.random_value <= (1 - self.p):
            self.outcome = 0
        else:
            self.outcome = self.value

    def get_signal(self):
        return random.randint(self.value - self.epsilon, self.value + self.epsilon)

    def set_winning_player(self):
        players = self.get_players()
        player = players[0]
        for p in players[1:]:
            if player.bid == p.bid:
                # Break ties randomly
                if random.random() < 0.5:
                    player.payoff = 0
                    player.winner = False
                    player = p
            elif player.bid < p.bid:
                player.payoff = 0
                player.winner = False
                player = p
        player.winner = True
        player.payoff = self.outcome - player.bid
        self.highest_bid = player.bid


class Player(BasePlayer):
    bid = models.IntegerField()
    signal = models.IntegerField()
    winner = models.BooleanField()
    payoff = models.IntegerField()
    payment_round = models.IntegerField()

