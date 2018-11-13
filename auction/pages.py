from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class InstructionPage(Page):
    def is_displayed(self):
        return self.round_number == 1


class BidPage(Page):
    form_model = 'player'
    form_fields = ['bid']

    def vars_for_template(self):
        return {
            'lottery_id': self.group.lottery_id,
            'signal': self.player.signal,
            'alpha': self.group.alpha,
            'beta': self.group.beta,
            'epsilon': self.group.epsilon,
            'min_signal': self.player.signal - self.group.epsilon,
            'max_signal': self.player.signal + self.group.epsilon,
            'p': self.group.p,
            'comp_p': 100 - self.group.p,
            'treatment': self.group.treatment,
            'value': self.group.value,
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
            'comp_p': 100 - self.group.p,
            'treatment': self.group.treatment,
            'value': self.group.value,
            'outcome': self.group.outcome,
            'payoff': self.player.payoff,
            'round_number': self.round_number,
            'tie': self.player.tie
        }

    def before_next_page(self):
        if self.player.participant.vars['payment_round'] == self.round_number:
            self.player.participant.vars['auction_data'] = {
            'winner': self.player.winner,
            'bid': self.player.bid,
            'highest_bid': self.group.highest_bid,
            'signal': self.player.signal,
            'alpha': self.group.alpha,
            'beta': self.group.beta,
            'p': self.group.p,
            'comp_p': 100 - self.group.p,
            'treatment': self.group.treatment,
            'value': self.group.value,
            'outcome': self.group.outcome,
            'payoff': self.player.payoff,
            'round_number': self.round_number,
            'tie': self.player.tie
            }


page_sequence = [
    InstructionPage, BidPage, DetermineGroupWinnerWaitPage, OutcomePage
]
