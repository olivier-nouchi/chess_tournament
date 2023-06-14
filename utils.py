from enum import Enum
from typing import List
from collections import defaultdict

from players import ChessPlayer


class ResultOutcome(Enum):
    win = "win"
    draw = "draw"
    loss = "loss"
    bye = "bye"


class PairingMethod(Enum):
    random = "Random"
    points = "Points"
    mid_rating = "MidRating"  # 1st with n/2 2nd with n/2 +1 etc


BASE_VICTORY = 9
BASE_DRAW = 3
DRAW_PENALTY = 2  # the number of points won in a draw is divided by this penalty
sacrifices_points_mapping = {'knight': 3,
                             'bishop': 3,
                             'rook': 5,
                             'queen': 9}


BYE_PLAYER = ChessPlayer(player_id=0, first_name="", last_name="BYE", is_active=True, is_paired=True)


def display_players_ranking(players: List[ChessPlayer], display_elo=True, display_tb_points=False):
    players_by_points = sorted(players, key=lambda p: (p.points, p.tb_points), reverse=True)
    elo_rating_str = ""
    tb_points_str = ""

    print("----- RANKING -----")
    for ranking, player in enumerate(players_by_points):
        if display_elo:
            elo_rating_str = f"[ELO: {player.elo_rating}]"

        if display_tb_points:
            tb_points_str = f"({player.tb_points} TB pts)"
            
        print(f"{ranking+1} - {player.full_name} - {player.points} points {tb_points_str} {elo_rating_str}")
        

def display_players_stats(players: List[ChessPlayer]):
    print("----- PLAYERS STATS -----")
    
    for player in players:
            
        print(f"{player.full_name} - {str(player.points)} points - {player.times_win_draw_loss_bye} - {player.round_colors} - {player.previous_opponents}")
        

def display_pairings_by_player(pairings:List):
    players_from_pairings = defaultdict(dict)
    for pairing in pairings:
        player1, player2 = pairing
        players_from_pairings[player1.player_id]["color"] = "white"
        players_from_pairings[player1.player_id]["opp_id"] = player2.player_id

        players_from_pairings[player2.player_id]["color"] = "black"
        players_from_pairings[player2.player_id]["opp_id"] = player1.player_id

    sorted_player_by_id = dict(sorted(players_from_pairings.items()))
    print(sorted_player_by_id)

    for player_id, player_info in sorted_player_by_id.items():
        color = player_info["color"]
        opp_id = player_info["opp_id"]
        print(f"{player_id} - {color} - {opp_id}")


def send_pairings_to_WA(pairings:List):
    pass
