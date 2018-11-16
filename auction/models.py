import math
import random
from typing import List

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from experiment.lottery import LotterySpecification

doc = """
Phase 1: Auction Phase: Set to 80 rounds, 10 for each lottery.
"""

class Constants(BaseConstants):
    name_in_url = 'auction'
    players_per_group = 4
    rounds_per_lottery = 3
    lotteries = [
        LotterySpecification(60, 90, 75, 4),
        LotterySpecification(10, 40, 25, 4),
        LotterySpecification(60, 90, 25, 4),
        LotterySpecification(10, 40, 75, 4),
        LotterySpecification(60, 90, 75, 8),
        LotterySpecification(10, 40, 25, 8),
        LotterySpecification(60, 90, 25, 8),
        LotterySpecification(10, 40, 75, 8),
    ]
    num_rounds = rounds_per_lottery*len(lotteries)


class Subsession(BaseSubsession):
    def set_group_size(self):
        players = self.get_players()
        group_matrix = []
        for i in range(0, len(players), Constants.players_per_group):
            group_matrix.append(players[i:i + Constants.players_per_group])
        self.set_group_matrix(group_matrix)

    def creating_session(self):
        self.set_group_size()
        self.group_randomly()

        for group in self.get_groups():  # type: Group
            group.set_round_lottery()
            for player in group.get_players():
                player.signal = group.get_signal()

        # Set the payoff relevant round
        if self.round_number == 1:
            for player in self.get_players():
                player.payment_round = random.randint(1, Constants.num_rounds)
                player.participant.vars["payment_round"] = player.payment_round


class Group(BaseGroup):
    lottery_id = models.IntegerField()
    lottery_display_id = models.IntegerField()
    alpha = models.IntegerField()
    beta = models.IntegerField()
    p = models.IntegerField()
    epsilon = models.IntegerField()
    value = models.IntegerField()
    random_value = models.IntegerField()
    outcome = models.IntegerField()
    highest_bid = models.IntegerField()
    treatment = models.StringField(choices=['cp', 'cv'])

    def get_treatment(self):
        treatment = self.session.config['treatment']
        if treatment != 'cp' and treatment != 'cv':
            treatment = 'cp'
        return treatment

    def set_round_lottery(self):
        lottery_order = []
        for i in range(1, 9):
            lottery_order.append(int(self.session.config["lottery_{}".format(i)].strip()))
        rounds_per_lottery = int(Constants.rounds_per_lottery)
        lottery_index_this_round = math.floor((self.round_number - 1) / rounds_per_lottery)
        self.lottery_id = lottery_order[lottery_index_this_round]
        self.lottery_display_id = lottery_index_this_round + 1

        self.treatment = self.get_treatment()

        lottery_spec: LotterySpecification = Constants.lotteries[self.lottery_id - 1]

        self.alpha = lottery_spec.alpha
        self.beta = lottery_spec.beta
        # epsilon is used to determine the player's signal
        self.epsilon = lottery_spec.epsilon

        if self.treatment == 'cv':
            self.p = lottery_spec.c
            self.value = random.randint(self.alpha, self.beta)

            self.random_value = random.randint(0, 100)
            if self.random_value <= self.p:
                self.outcome = self.value
            else:
                self.outcome = 0
        else:
            self.p = random.randint(self.alpha, self.beta)
            self.value = lottery_spec.c

            self.random_value = random.randint(0, 100)
            if self.random_value <= self.p:
                self.outcome = self.value
            else:
                self.outcome = 0

    def get_signal(self):
        if self.treatment == 'cv':
            return random.randint(self.value - self.epsilon, self.value + self.epsilon)
        else:
            return random.randint(self.p - self.epsilon, self.p + self.epsilon)

    def set_winning_player(self):
        players = self.get_players()
        max_bid = -1
        # find the max bid
        for p in players:
            if p.bid > max_bid:
                max_bid = p.bid

        self.highest_bid = max_bid

        winners = []
        for p in players:
            # set losers payoffs
            if p.bid < self.highest_bid:
                p.winner = False
                p.tie = False
                p.payoff = 0

            # record tied players
            elif p.bid == self.highest_bid:
                winners.append(p)

        winner_id = random.randint(0, len(winners)-1)
        for i, p in enumerate(winners):
            if i == winner_id:
                p.payoff = self.outcome - p.bid
                p.winner = True
                p.tie = True
            else:
                p.payoff = 0
                p.winner = False
                p.tie = True


class Player(BasePlayer):
    bid = models.IntegerField()
    signal = models.IntegerField()
    tie = models.BooleanField(default=False)
    winner = models.BooleanField()
    payoff = models.IntegerField()
    payment_round = models.IntegerField()

