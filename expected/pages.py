from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree.api import (Currency as c)
from auction.models import Constants as AuctionConstants

import ast

class ExpPage(Page):
    form_model = 'player'
    form_fields = ['expected_value']

    def vars_for_template(self):
        return {
            'endowment': c(self.session.config['endowment_tokens']),
            'display_round_number': self.round_number + AuctionConstants.num_rounds,
            'alpha': self.player.alpha,
            'beta': self.player.beta,
            'p': '' if self.player.treatment == 'cp' else self.player.c,
            'treatment': self.player.treatment,
            'value': '' if self.player.treatment == 'cv' else self.player.c,
            'max_outcome': self.player.c if self.player.treatment == 'cp' else self.player.beta,
            'min_bid': 0,
            'img': "expected/{}{}.png".format(self.player.treatment, self.player.lottery_id),
            'legend': "expected/{}l{}.png".format(self.player.treatment, self.player.lottery_id),
        }

    def before_next_page(self):
        self.player.becker_degroot_marschak_payment_method()
        self.player.set_payoffs()


class PasswordWaitPage(Page):
    form_model = 'player'
    form_fields = ['pass_code']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        if 'pass_code' not in values:
            return ' You must wait for the researcher to provide you with the correct password'
        elif not (values['pass_code'] == 42):
            return ' You must wait for the researcher to provide you with the correct password'


page_sequence = [
    PasswordWaitPage, ExpPage,
]
