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
            'max_bid': 100
        }


page_sequence = [
    BidPage,
]
