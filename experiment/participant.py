from experiment.auction import Auction


class Participant:
    @staticmethod
    def get_auction(player) -> Auction:
        return player.participant.vars['auction']

    @staticmethod
    def set_experiment(player, auction: Auction) -> None:
        player.participant.vars['auction'] = auction
