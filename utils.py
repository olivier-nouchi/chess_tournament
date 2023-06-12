from enum import Enum
from typing import List

from players import ChessPlayer


class ResultOutcome(Enum):
    win = "win"
    draw = "draw"
    loss = "loss"
    bye = "bye"


class PairingMethod(Enum):
    random = "Random"
    points = "Points"


BASE_VICTORY = 9
BASE_DRAW = 3
DRAW_PENALTY = 2  # the number of points won in a draw is divided by this penalty
sacrifices_points_mapping = {'knight': 3,
                             'bishop': 3,
                             'rook': 5,
                             'queen': 9}


BYE_PLAYER = ChessPlayer(player_id=0, first_name="", last_name="BYE", is_active=True, is_paired=True)


def display_players_ranking(players: List[ChessPlayer]):
    players_by_points = sorted(players, key=lambda p: p.points, reverse=True)

    print("----- RANKING -----")
    for ranking, player in enumerate(players_by_points):
        print(f"{ranking+1} - {player.full_name} - {player.points} points")
        

def display_players_stats(players: List[ChessPlayer]):
    print("----- PLAYERS STATS -----")
    
    for player in players:
        print(f"{player.full_name} - {str(player.points)} points - {player.times_win_draw_loss_bye} - {player.round_colors} - {player.previous_opponents}")
        

def send_pairings_to_WA(pairings= List):
    pass
