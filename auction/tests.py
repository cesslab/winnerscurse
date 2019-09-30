from otree.api import Currency as c, currency_range, expect, SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants

from .pages import QuizPartOne, QuizPartTwo, InstructionPage, NewLotteryReminder, ValuationPage, BidPage


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield(SubmissionMustFail(QuizPartOne, {'q1': ['2'], 'q2': ['1']}))
            yield(SubmissionMustFail(QuizPartOne, {'q1': ['1'], 'q2': ['1']}))
            yield(QuizPartOne, {'q1': ['2'], 'q2': ['2']})
            expect(self.player.q1, "['2']")
            expect(self.player.q2, "['2']")

            yield(SubmissionMustFail(QuizPartTwo, {'q3': ['2'], 'q4': ['1']}))
            yield(QuizPartTwo, {'q3': ['2', '3', '4'], 'q4': ['1', '3']})

            yield(InstructionPage)
            # yield(ValuationPage, {'bid': 0})
            # yield(BidPage, {'bid': 0})
        # elif ((self.round_number-1) % (Constants.rounds_per_lottery + 1)) == 0:
        #     pass
        # elif self.round_number != 1 and ((self.round_number-1) % (Constants.rounds_per_lottery + 1)) == 0:
        #     yield(NewLotteryReminder)


