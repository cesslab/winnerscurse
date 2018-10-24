from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class BidPage(Page):
    form_model = 'player'
    form_fields = ['bid']

    def vars_for_template(self):
        return {
            'signal': self.player.signal,
            'alpha': self.group.alpha,
            'beta': self.group.beta,
            'p': self.group.p,
            'comp_p': 1 - self.group.p,
            'min_bid': 0,
            'max_bid': 100,
            'round_number': self.round_number,
        }


class DetermineGroupWinnerWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_winning_player()


class OutcomePage(Page):
    def vars_for_template(self):
        return {
            'winner': self.player.winner,
            'bid': self.player.bid,
            'highest_bid': self.group.highest_bid,
            'signal': self.player.signal,
            'alpha': self.group.alpha,
            'beta': self.group.beta,
            'p': self.group.p,
            'outcome': self.group.outcome,
            'comp_p': 1 - self.group.p,
            'payoff': self.player.payoff,
            'round_number': self.round_number,
        }


page_sequence = [
    BidPage, DetermineGroupWinnerWaitPage, OutcomePage
]
