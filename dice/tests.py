import random

from otree.api import Bot, SubmissionMustFail
from phase_four import pages
from exp.util import Participant


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            # Instructions Page
            yield (pages.InstructionsPage)

            # Roll Dice Page: Test incorrect input
            yield SubmissionMustFail(pages.RollDicePage, {'die_side': 0})
            yield SubmissionMustFail(pages.RollDicePage, {'die_side': 7})
            yield SubmissionMustFail(pages.RollDicePage)

            # Roll Dice Page: Test correct input
            r_side = random.randint(1, 6)
            yield (pages.RollDicePage, {'die_side': r_side})
            assert self.player.die_side == r_side, "Entered die-side {}, Player die-side {}".format(r_side, self.player.die_side)
            die_side = Participant.get_experiment(self.player).phase_four.die_side
            assert die_side == r_side, "Entered die-side {}, Phase die-side {}".format(r_side, die_side)

            # Bid and Cutoff Entry Page: Test incorrect input
            lottery = Participant.get_experiment(self.player).phase_four.get_lottery(self.player.round_number)
            r_bet = random.choice([lottery.BET_HIGH_RED, lottery.BET_HIGH_BLUE])
            r_cutoff = random.randint(lottery.min_cutoff, lottery.max_cutoff)
            yield SubmissionMustFail(pages.MinBuyoutBetForLotteryPage,)
            yield SubmissionMustFail(pages.MinBuyoutBetForLotteryPage, {'cutoff': lottery.min_cutoff})
            yield SubmissionMustFail(pages.MinBuyoutBetForLotteryPage, {'cutoff': lottery.max_cutoff, 'bet': lottery.BET_HIGH_RED})
            yield SubmissionMustFail(pages.MinBuyoutBetForLotteryPage, {
                'cutoff': lottery.max_cutoff+1, 'bet': lottery.BET_HIGH_RED, 'clicked': 1})
            yield SubmissionMustFail(pages.MinBuyoutBetForLotteryPage, {
                'cutoff': lottery.min_cutoff-1, 'bet': lottery.BET_HIGH_RED, 'clicked': 1})

            # Bid and Cutoff Entry Page: Test correct input
            yield (pages.MinBuyoutBetForLotteryPage, {'cutoff': r_cutoff, 'bet': r_bet, 'clicked': 1})
            assert self.player.cutoff == r_cutoff, "Entered cutoff {}, Player cutoff {}".format(r_cutoff, self.player.cutoff)
            assert self.player.bet == r_bet, "Entered bet {}, Player bet {}".format(r_cutoff, self.player.bet)
            assert self.player.clicked == 1, "Entered clicked {}, Player clicked {}".format(1, self.player.clicked)
        else:
            lottery = Participant.get_experiment(self.player).phase_four.get_lottery(self.player.round_number)
            r_bet = random.choice([lottery.BET_HIGH_RED, lottery.BET_HIGH_BLUE])
            r_cutoff = random.randint(lottery.min_cutoff, lottery.max_cutoff)
            yield (pages.MinBuyoutBetForLotteryPage, {'cutoff': r_cutoff, 'bet': r_bet, 'clicked': 1})
            assert self.player.cutoff == r_cutoff, "Entered cutoff {}, Player cutoff {}".format(r_cutoff, self.player.cutoff)
            assert self.player.bet == r_bet, "Entered bet {}, Player bet {}".format(r_cutoff, self.player.bet)
            assert self.player.clicked == 1, "Entered clicked {}, Player clicked {}".format(1, self.player.clicked)
