from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ExpPage(Page):
    form_model = 'player'
    form_fields = ['expected_value']

    def vars_for_template(self):
        lottery = Constants.lottery_types[self.round_number-1]
        treatment = self.session.config['treatment']
        return {
            'lottery_display_id': self.round_number,
            'alpha': lottery.alpha,
            'beta': lottery.beta,
            'p': '' if treatment == 'cp' else lottery.c,
            'treatment': treatment,
            'value': '' if treatment == 'cv' else lottery.c,
            'min_bid': 0,
            'max_bid': 100,
            'round_number': self.round_number,
        }


page_sequence = [
    ExpPage,
]
