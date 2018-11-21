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

        if treatment == 'cv':
            q4_labels = [
                'The Selected Value of the lottery minus your bid.',
                'The outcome of the lottery minus your bid.'
            ]
        else:
            q4_labels = [
                'The non-zero value of the lottery minus your bid.',
                'The outcome of the lottery minus your bid.'
            ]

        template_vars = {
            'questions': {
                'q1': {
                    'question': 'Suppose that you are not the highest bidder in an auction. How much do you have to pay?',
                    'labels': ['Your bid', 'The highest bid', 'Nothing']},
                'q2': {
                    'question': 'Which of the following alternatives is correct?',
                    'labels': [
                        'All four bidders bid for the same lottery ticket with the same Selected {}.'.format(ttype),
                        'All four bidders bid for lottery tickets with different Selected {}.'.format(ttype),
                        'All four bidders bid for lottery tickets with possibly different Selected {}.'.format(ttype)]
                },
                'q3': {
                    'question': 'Which of the following alternatives is correct?',
                    'labels': [
                        'All four bidders receive the same signal about the same Selected {}.'.format(ttype),
                        'All four bidders receive possibly different signals about the same Selected {}.'.format(ttype),
                        'All four bidders receive different signals because Selected {} differ for each of them.'.format(ttype)
                    ]
                },
                'q4': {
                    'question': 'Suppose you win the lottery ticket in a given auction. What are your earnings from this auction?',
                    'labels': q4_labels
                },
            }
        }

        return template_vars

    def q1_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return "An error was found in question 1."

        if len(values) == 1 and '3' in values:
            return
        else:
            print(values)
            return "Your selection for question 1 was incorrect."

    def q2_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return 'An error was found in question 2.'

        if len(values) == 1 and '1' in values:
            return
        else:
            print(values)
            return 'Your selection for question 2 was incorrect.'

    def q3_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return 'An error was found in question 3.'

        if len(values) == 1 and '2' in values:
            return
        else:
            print(values)
            return 'Your selection for question 3 was incorrect.'

    def q4_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return 'An error was found in question 4.'

        if len(values) == 1 and '2' in values:
            return
        else:
            print(values)
            return 'Your selection for question 4 was incorrect.'


class QuizPartTwo(Page):
    form_model = 'player'
    form_fields = ['q5', 'q6']

    def vars_for_template(self):
        treatment = self.session.config['treatment']
        if treatment != 'cp' and treatment != 'cv':
            treatment = 'cp'

        ttype = 'Value' if treatment == 'cv' else 'Probability'
        nf = '%' if treatment == 'cp' else ''

        if treatment == 'cv':
            q6_labels = ['0', '21 (= 30 x 70% + 0 x 30%)', '30']
        else:
            q6_labels = ['0', '21 (= 30% x 70 + 70% x 0)', '70']

        template_vars = {
            'treatment': treatment,
            'lottery': '',
            'questions': {
                'q5': {
                    'question': 'Suppose that you receive a signal 30 that is at most 8 percentage points away from the Selected {}. What could be the Selected {}? Select all that apply.'.format(ttype, ttype),
                    'labels': [
                        '20'.format(nf), '25'.format(nf), '30'.format(nf), '35'.format(nf), '40'.format(nf)]},
                'q6': {
                    'question': 'Suppose the Selected {} is 30{}, what could be the outcome of the lottery? Select all that apply.'.format(ttype, nf),
                    'labels': q6_labels
                },
            }
        }

        return template_vars

    def q5_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return "An error was found in question 5."

        if len(values) == 3 and '2' in values and '3' in values and '4' in values:
            return
        else:
            print(values)
            return "Your selection for question 5 was incorrect."

    def q6_error_message(self, value):
        values = ast.literal_eval(value)
        if len(values) == 0:
            return "An error was found in question 6."

        if len(values) == 2 and '1' in values and '3' in values:
            return
        else:
            print(values)
            return "Your selection for question 2 was incorrect."

page_sequence = [
    QuizPartOne, QuizPartTwo
]
