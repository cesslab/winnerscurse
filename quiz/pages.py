from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import ast


class QuizPartOne(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4']

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
                'q1': {
                    'question': 'What happens if the random price falls above your willingness to pay in a given round?',
                    'labels': ['You play the lottery.', 'You do not play the lottery.']
                },
                'q2': {
                    'question': 'Suppose you play the lottery in a given round. What are your earnings in that round?',
                    'labels': [
                        'The {} of the lottery minus the random price.'.format(cterm),
                        'The outcome of the lottery minus the random price.'],
                },
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

    def q3_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return "An error was found in question 5."

        if len(values) == 3 and '2' in values and '3' in values and '4' in values:
            return
        else:
            print(values)
            return "Your selection for question 3 was incorrect."

    def q4_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return "An error was found in question 6."

        if len(values) == 2 and '1' in values and '3' in values:
            return
        else:
            print(values)
            return "Your selection for question 4 was incorrect."


page_sequence = [
    QuizPartOne
]
