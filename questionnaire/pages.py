from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class PartOne(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'major']


class PartTwoA(Page):
    form_model = 'player'
    form_fields = ['q1a', 'q1b', 'q1c', 'q1d', 'q1e', 'q1exp']

    def vars_for_template(self):
        treatment = self.session.config['treatment']
        if treatment != 'cp' and treatment != 'cv':
            treatment = 'cp'

        if treatment == 'cp':
            template_vars = {
                'q1_lottery': {'low': 60, 'high': 90, 'value': 75},

            }
        else:
            template_vars = {
                'q1_lottery': {'p': 75, 'low': 60, 'high': 90},
            }

        template_vars.update({
            'treatment': treatment,
            'q1a': {'s': 65, 'low': 61, 'high': 69},
            'q1b': {'s': 70, 'low': 66, 'high': 74},
            'q1c': {'s': 75, 'low': 71, 'high': 79},
            'q1d': {'s': 80, 'low': 76, 'high': 84},
            'q1e': {'s': 85, 'low': 81, 'high': 89},
        })
        return template_vars


class PartTwoB(Page):
    form_model = 'player'
    form_fields = ['q2', 'q3', 'q3exp', 'q4']

    def vars_for_template(self):
        treatment = self.session.config['treatment']
        if treatment != 'cp' and treatment != 'cv':
            treatment = 'cp'

        if treatment == 'cp':
            template_vars = {
                'q2_lottery': {'low': 10, 'high': 40, 'value': 25},

            }
        else:
            template_vars = {
                'q2_lottery': {'p': 25, 'low': 10, 'value': 40},
            }

        template_vars.update({
            'treatment': treatment,
            'q2': {'s': 28, 'low': 24, 'high': 32},
            'q3': {'s': 30, 'low': 26, 'high': 34},
        })
        return template_vars


class PartTwoC(Page):
    form_model = 'player'
    form_fields = ['q5', 'q5exp', 'q6', 'q6exp']

    def vars_for_template(self):
        treatment = self.session.config['treatment']
        if treatment != 'cp' and treatment != 'cv':
            treatment = 'cp'

        if treatment == 'cp':
            template_vars = {
                'treatment': treatment,
                'q5a_lottery': {'low': 60, 'high': 90, 'value': 75},
                'q5b_lottery': {'p': 75, 'low': 60, 'high': 90},

            }
        else:
            template_vars = {
                'treatment': treatment,
                'q5a_lottery': {'p': 75, 'low': 60, 'value': 90},
                'q5b_lottery': {'low': 60, 'high': 90, 'value': 75},
            }

        return template_vars


class PartThree(Page):
    form_model = 'player'
    form_fields = ['q7', 'q8', 'q9']


page_sequence = [
    PartOne, PartTwoA, PartTwoB, PartTwoC, PartThree
]
