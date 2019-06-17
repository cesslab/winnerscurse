from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ExpPage(Page):
    form_model = 'player'
    form_fields = ['expected_value']

    def vars_for_template(self):
        return {
            'lottery_display_id': self.round_number,
            'alpha': self.player.alpha,
            'beta': self.player.beta,
            'p': '' if self.player.treatment == 'cp' else self.player.c,
            'treatment': self.player.treatment,
            'value': '' if self.player.treatment == 'cv' else self.player.c,
            'min_bid': 0,
            'max_bid': 100,
            'round_number': self.round_number,
            'img': "expected/{}{}.png".format(self.player.treatment, self.player.lottery_id),
        }

    def before_next_page(self):
        self.player.becker_degroot_marschak_payment_method()
        self.player.set_payoffs()




page_sequence = [
    ExpPage,
]
