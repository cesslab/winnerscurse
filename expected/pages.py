from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ExpPage(Page):
    form_model = 'player'
    form_fields = ['expected_value']

    def vars_for_template(self):
        lotteries = Constants.lottery_types
        return {
            'lottery_display_id': self.round_number,
            'alpha': lotteries[self.round_number-1].alpha,
            'beta': lotteries[self.round_number-1].beta,
            'p': self.player.p,
            'comp_p': 100 - self.player.p,
            'treatment': self.player.treatment,
            'value': self.player.value,
            'min_bid': 0,
            'max_bid': 100,
            'round_number': self.round_number,
        }


page_sequence = [
    ExpPage,
]
