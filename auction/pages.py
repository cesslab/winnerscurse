import math

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class InstructionPage(Page):
    def is_displayed(self):
        return self.round_number == 1


class NewLotteryReminder(Page):
    def is_displayed(self):
        return self.round_number != 1 and self.round_number % Constants.rounds_per_lottery == 1

    def vars_for_template(self):
        return {
            'rounds_per_lottery': Constants.rounds_per_lottery
        }

class BidPage(Page):
    form_model = 'player'
    form_fields = ['bid']

    def vars_for_template(self):
        return {
            'lottery_display_id': self.player.lottery_display_id,
            'signal': self.player.signal,
            'alpha': self.player.alpha,
            'beta': self.player.beta,
            'epsilon': self.player.epsilon,
            'min_signal': self.player.signal - self.player.epsilon,
            'max_signal': self.player.signal + self.player.epsilon,
            'p': self.player.p,
            'comp_p': 100 - self.player.p,
            'treatment': self.player.treatment,
            'value': self.player.value,
            'min_bid': 0,
            'max_bid': 100,
            'round_number': self.round_number,
        }

    def before_next_page(self):
        self.player.set_winning_player()

class OutcomePage(Page):
    def vars_for_template(self):
        return {
            'winner': self.player.winner,
            'bid': self.player.bid,
            'computer_random_val': self.player.computer_random_val,
            'signal': self.player.signal,
            'alpha': self.player.alpha,
            'beta': self.player.beta,
            'p': self.player.p,
            'comp_p': 100 - self.player.p,
            'treatment': self.player.treatment,
            'value': self.player.value,
            'outcome': self.player.outcome,
            'payoff': self.player.payoff,
            'round_number': self.round_number,
            'tie': self.player.tie
        }

    def before_next_page(self):
        if self.player.participant.vars['payment_round'] == self.round_number:
            self.player.participant.vars['auction_data'] = {
            'winner': self.player.winner,
            'bid': self.player.bid,
            'computer_random_val': self.player.computer_random_val,
            'signal': self.player.signal,
            'alpha': self.player.alpha,
            'beta': self.player.beta,
            'p': self.player.p,
            'comp_p': 100 - self.player.p,
            'treatment': self.player.treatment,
            'value': self.player.value,
            'outcome': self.player.outcome,
            'payoff': self.player.payoff,
            'round_number': self.round_number,
            'tie': self.player.tie
            }


page_sequence = [
    InstructionPage, NewLotteryReminder, BidPage, OutcomePage
]
