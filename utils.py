from enum import Enum
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