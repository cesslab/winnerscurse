from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import ast

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
            'legend': "expected/{}l{}.png".format(self.player.treatment, self.player.lottery_id),
        }

    def before_next_page(self):
        self.player.becker_degroot_marschak_payment_method()
        self.player.set_payoffs()


class QuizPartOne(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        treatment = self.session.config['treatment']
        if treatment != 'cp' and treatment != 'cv':
            treatment = 'cp'

        ttype = "Value" if treatment == 'cv' else "Probability"
        cterm = "Selected Value" if treatment == 'cv' else "non-zero value"
        nf = '%' if treatment == 'cp' else ''
        template_vars = {
            'treatment': treatment,
            'questions': {
                'q1': {
                    'question': 'What happens if the random price falls above your valuation in a given round?',
                    'labels': ['You play the lottery.', 'You do not play the lottery.']
                },
                'q2': {
                    'question': 'Suppose you play the lottery in a given round. What are your earnings in that round?',
                    'labels': [
                        'Zero.',
                        'The outcome of the lottery minus the random price.',
                        'The outcome of the lottery.'
                    ],
                },
            },
        }

        return template_vars


    def q1_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return "An error was found in question 1."

        if len(values) == 1 and '2' in values:
            return
        else:
            print(values)
            return "Your selection for question 1 was incorrect."

    def q2_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return 'An error was found in question 2.'

        if len(values) == 1 and '2' in values:
            return
        else:
            print(values)
            return 'Your selection for question 2 was incorrect.'


page_sequence = [
    QuizPartOne, ExpPage,
]
