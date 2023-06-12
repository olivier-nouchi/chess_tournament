from players import ChessPlayer
from typing import List


class Tournament:

    def __init__(self, players=None, current_round: int=0):
        if players is None:
            players = []

        self.players = players
        self.current_round = current_round

    def get_tournament_state(self):
        for rank, player in enumerate(sorted(self.players, key=lambda p: p.points, reverse=True)):
            print(f"{rank+1} - {player.full_name} - {str(player.points)} points - {player.times_win_draw_loss_bye} - {player.round_colors} - {player.previous_opponents}")


