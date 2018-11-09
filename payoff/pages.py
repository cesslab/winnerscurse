from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from experiment.lottery import RedBlueLottery


class PayoffCalculationWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for player in self.group.get_players():
            player.dice_phase_payoffs()
            player.auction_payoff()
            player.final_payoff()


class MethodThreeResultsPage(Page):
    def vars_for_template(self):
        lotteries = self.player.participant.vars['RedBlueLotteries']
        lottery: RedBlueLottery = self.player.participant.vars['red_blue_lottery']
        lottery_ids = [lid for lid, value in lotteries.items()]

        die_labels = self.player.participant.vars['die_labels']
        die_lottery_ids = list(zip(die_labels, lottery_ids))

        context = {
            'rolled_side': self.player.participant.vars['die_side'],
            'rolled_side_encoded': die_labels[self.player.task_id-1],
            'die_encoding': die_lottery_ids,
            'bet_color': self.player.participant.vars['bet'],
            'bet_high_red': RedBlueLottery.BET_HIGH_RED,
            'bet_high_blue': RedBlueLottery.BET_HIGH_BLUE,
            'high_value': lottery.high_value,
            'low_value': lottery.low_value,
            'lottery': lottery,
            'lottery_type': lottery.ltype,
            'cutoff': self.player.participant.vars['cutoff'],
            'random_cutoff': self.player.random_cutoff,
            'play_lottery': self.player.play_lottery,
            'num_red': self.player.num_red_chips,
            'num_blue': self.player.total_chips - self.player.num_red_chips,
            'realized_value': self.player.realized_value,
            'earnings': self.player.phase_two_payoff_credits
        }

        return context


class PhaseOnePayoff(Page):
    def vars_for_template(self):
        return self.player.participant.vars['auction_data']


class TotalPayoff(Page):
    def vars_for_template(self):
        return {
            'phase_one_payoff_credits': self.player.phase_one_payoff_credits,
            'phase_two_payoff_credits': self.player.phase_two_payoff_credits,
            'phase_one_payoff_dollars': self.player.phase_one_payoff_dollars.to_real_world_currency(self.session),
            'phase_two_payoff_dollars': self.player.phase_two_payoff_dollars.to_real_world_currency(self.session),
            'endowment': c(self.session.config['endowment']).to_real_world_currency(self.session),
            'show_up_fee': c(self.session.config['participation_fee']).to_real_world_currency(self.session),
            'final_payoff': self.player.total_payoff_dollars.to_real_world_currency(self.session)
        }


page_sequence = [
    PayoffCalculationWaitPage,
    PhaseOnePayoff,
    MethodThreeResultsPage,
    TotalPayoff
]
