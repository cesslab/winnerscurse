import ast

from ._builtin import Page, WaitPage
from .models import Constants

from otree.api import Currency as c


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {"treatment": self.player.treatment}


class Update(Page):
    def is_displayed(self):
        return ((self.round_number - 1) % Constants.rounds_per_lottery) == 0

    def vars_for_template(self):
        return {
            "treatment": self.player.treatment,
            "rounds_per_lottery": Constants.rounds_per_lottery,
        }


class LotteryValuation(Page):
    form_model = "player"
    form_fields = ["bid", "min_worth", "max_worth"]

    def vars_for_template(self):
        return {
            "endowment": c(self.session.config["endowment_tokens"]),
            "display_round_number": self.round_number,
            "lottery_max_value": self.player.lottery_max_value,
            "signal": self.player.signal,
            "alpha": self.player.alpha,
            "beta": self.player.beta,
            "epsilon": self.player.epsilon,
            "min_signal": self.player.signal - self.player.epsilon,
            "max_signal": self.player.signal + self.player.epsilon,
            "p": self.player.p,
            "comp_p": 100 - self.player.p,
            "treatment": self.player.treatment,
            "is_probability_treatment": self.player.is_probability_treatment,
            "value": self.player.value,
            "min_bid": 0,
            "max_bid": 100,
            "round_number": self.round_number,
            "lottery_display_type": self.player.lottery_display_type,
        }

    def js_vars(self):
        return dict(
            lottery_max_value=self.player.lottery_max_value,
            mapping_divisor=self.player.mapping_divisor,
            is_probability_treatment=self.player.is_probability_treatment,
        )

    def error_message(self, values):
        try:
            min_worth = int(values["min_worth"])
            max_worth = int(values["max_worth"])
            bid = int(values["bid"])
            if not (min_worth < bid < max_worth):
                return "Your Minimum Worth must be less than your Willingness to Pay, and your Willingness to Pay must be less than your Maximum Worth"
        except ValueError:
            return "All values must be specified"

    def before_next_page(self):
        self.player.becker_degroot_marschak_payment_method()
        self.player.set_payoffs(1, 2)


page_sequence = [Instructions, Update, LotteryValuation]
