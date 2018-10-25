from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage

from exp.util import Participant
from exp.lottery import Lottery


class InstructionsPage(Page):
    def is_displayed(self):
        return self.round_number == 1


class RollDicePage(Page):
    form_model = 'player'
    form_fields = ['die_side']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        print(values)
        if not ('die_side' not in values or 1 <= int(values['die_side']) <= 6):
            return 'You must roll the die before continuing.'

    def before_next_page(self):
        experiment = Participant.get_experiment(self.player)
        experiment.phase_four.set_die_side(self.player.die_side)


class MinBuyoutBetForLotteryPage(Page):
    form_model = 'player'
    form_fields = ['cutoff', 'bet', 'clicked']

    def vars_for_template(self):
        experiment = Participant.get_experiment(self.player)
        lottery = experiment.phase_four.get_lottery(self.round_number)
        return {
            'lottery': lottery,
            'lottery_type': lottery.ltype,
            'low_value': lottery.low_value,
            'high_value': lottery.high_value,
            'bet_high_red': lottery.BET_HIGH_RED,
            'bet_high_blue': lottery.BET_HIGH_BLUE,
            'num_red': lottery.number_red if lottery.has_number_red() else '',
            'num_blue': lottery.number_blue if lottery.has_number_blue() else '',
            'bags': [(i, lottery.total - i) for i in range(lottery.total + 1)]
        }

    def cutoff_max(self):
        experiment = Participant.get_experiment(self.player)
        return experiment.phase_four.get_lottery(self.round_number).max_cutoff

    def cutoff_min(self):
        experiment = Participant.get_experiment(self.player)
        return experiment.phase_four.get_lottery(self.round_number).min_cutoff

    def error_message(self, values):
        if not int(values['clicked']) == 1:
            return 'Please enter a minimum compensation for your preferred bet.'
        elif not (values['bet'] == Lottery.BET_HIGH_RED or values['bet'] == Lottery.BET_HIGH_BLUE):
            return 'Please select your preferred bet by pressing the red or blue button.'

    def before_next_page(self):
        experiment = Participant.get_experiment(self.player)
        experiment.phase_four.set_cutoff(self.round_number, float(self.player.cutoff))
        experiment.phase_four.set_bet(self.round_number, self.player.bet)

        self.player.lottery = Participant.get_experiment(self.player).phase_four.get_lottery(self.round_number).lid
        self.player.question = experiment.phase_four.get_lottery(self.round_number).lid


class PlayerWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 1


class InstructionsWaitPage(Page):
    form_model = 'player'
    form_fields = ['pass_code']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        if 'pass_code' not in values:
            return ' You must wait for the researcher to provide you with the correct password'
        elif not (values['pass_code'] == 2600):
            return ' You must wait for the researcher to provide you with the correct password'


page_sequence = [
    PlayerWaitPage,
    InstructionsWaitPage,
    RollDicePage,
    MinBuyoutBetForLotteryPage,
]
