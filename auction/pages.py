import ast

from ._builtin import Page, WaitPage
from .models import Constants
from expected.models import Constants as ExpectedConstants

from otree.api import (Currency as c)

class InstructionPage(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'treatment': self.player.treatment
        }

class NewLotteryReminder(Page):
    def is_displayed(self):
        return self.round_number != 1 and ((self.round_number-1) % (Constants.rounds_per_lottery + 1)) == 0

    def vars_for_template(self):
        return {
            'rounds_per_lottery': Constants.rounds_per_lottery + 1
        }


class NewSignalReminder(Page):
    def is_displayed(self):
        return ((self.round_number-1) % (Constants.rounds_per_lottery + 1)) == 1

    def vars_for_template(self):
        return {
            'treatment': self.player.treatment,
            'rounds_per_lottery': Constants.rounds_per_lottery
        }


class ValuationPage(Page):
    form_model = 'player'
    form_fields = ['bid']

    def is_displayed(self):
        return ((self.round_number-1) % (Constants.rounds_per_lottery + 1)) == 0

    def vars_for_template(self):
        return {
            'endowment': c(self.session.config['endowment_tokens']),
            'display_round_number': self.round_number + ExpectedConstants.num_rounds,
            'lottery_display_type': self.player.lottery_display_type,
            'max_outcome': self.player.c if self.player.treatment == 'cp' else self.player.beta,
            'alpha': self.player.alpha,
            'beta': self.player.beta,
            'p': self.player.p,
            'comp_p': 100 - self.player.p,
            'treatment': self.player.treatment,
            'value': self.player.value,
            'min_bid': 0,
            'max_bid': self.player.c if self.player.treatment == 'cp' else self.player.beta,
        }

    def before_next_page(self):
        self.player.becker_degroot_marschak_payment_method()
        self.player.set_payoffs(2, 1)


class BidPage(Page):
    form_model = 'player'
    form_fields = ['bid']

    def is_displayed(self):
        return ((self.round_number-1) % (Constants.rounds_per_lottery + 1)) != 0

    def vars_for_template(self):
        return {
            'endowment': c(self.session.config['endowment_tokens']),
            'display_round_number': self.round_number + ExpectedConstants.num_rounds,
            'max_outcome': self.player.c if self.player.treatment == 'cp' else self.player.beta,
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
            'lottery_display_type': self.player.lottery_display_type
        }

    def before_next_page(self):
        self.player.becker_degroot_marschak_payment_method()
        self.player.set_payoffs(2, 2)


class OutcomePage(Page):

    def is_displayed(self):
        return ((self.round_number-1) % (Constants.rounds_per_lottery + 1)) != 0

    def vars_for_template(self):
        return {
            'endowment': c(self.session.config['endowment_tokens']),
            'total_payoff': self.player.payoff + c(self.session.config['endowment_tokens']),
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
            'tie': self.player.tie,
            'lottery_display_type': self.player.lottery_display_type,
            'display_round_number': self.round_number + ExpectedConstants.num_rounds,
        }


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


class QuizPartTwo(Page):
    form_model = 'player'
    form_fields = ['q3', 'q4']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        treatment = self.session.config['treatment']
        if treatment != 'cp' and treatment != 'cv':
            treatment = 'cp'

        ttype = "Value" if treatment == 'cv' else "Probability"
        cterm = "Selected Value" if treatment == 'cv' else "non-zero value"
        nf = '%' if treatment == 'cp' else ''
        if treatment == 'cv':
            q4_labels = ['0', '21 (= 30 x 70% + 0 x 30%)', '30']
            q3_type = 'units'
        else:
            q4_labels = ['0', '21 (= 30% x 70 + 70% x 0)', '70']
            q3_type = 'percentage points'

        template_vars = {
            'treatment': treatment,
            'questions': {
                'q3': {
                    'question': 'Suppose that you receive a signal of 30 that is at most 8 {} away from the Selected {}. What could be the Selected {}? Select all that apply.'.format(
                        q3_type, ttype, ttype),
                    'labels': ['20'.format(nf), '25'.format(nf), '30'.format(nf), '35'.format(nf), '40'.format(nf)]
                },
                'q4': {
                    'question': 'Suppose the Selected {} is 30{}, what could be the outcome of the lottery? Select all that apply.'.format(
                        ttype, nf),
                    'labels': q4_labels
                }
            },
        }

        return template_vars

    def q3_error_message(self, value):
        """ Question 3 - Correct Answers 2, 3, 4"""
        values = ast.literal_eval(value)
        if len(values) == 0:
            return "An error was found in question 5."

        if len(values) == 3 and '2' in values and '3' in values and '4' in values:
            return
        else:
            print(values)
            return "Your selection for question 3 was incorrect."

    def q4_error_message(self, value):
        """ Question 4 - Correct Answers 1, 3"""
        values = ast.literal_eval(value)
        if len(values) == 0:
            return "An error was found in question 6."

        if len(values) == 2 and '1' in values and '3' in values:
            return
        else:
            print(values)
            return "Your selection for question 4 was incorrect."

page_sequence = [
   PasswordWaitPage, QuizPartTwo, InstructionPage, NewLotteryReminder, ValuationPage, NewSignalReminder, BidPage, OutcomePage
]
