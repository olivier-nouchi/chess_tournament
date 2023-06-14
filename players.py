class ChessPlayer:

    def __init__(self, player_id: int, first_name: str, last_name: str, is_active: bool = True, is_paired: bool = False,
                 elo_rating: int = 0, points: float = 0, tb_points: float = 0):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.elo_rating = elo_rating
        self.is_active = is_active
        self.is_paired = is_paired
        self.points = points
        self.tb_points = tb_points
        self.round_colors = {"white": 0, "black": 0}
        self.times_win_draw_loss_bye = {"win": 0, "draw": 0, "loss": 0, "bye": 0}
        self.previous_opponents = []

    def __str__(self):
        return f"({str(self.player_id)})- {self.full_name} ({str(self.points)} points)"

    def __repr__(self):
        return f"({str(self.player_id)})- {self.full_name} ({str(self.points)} points)"

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def nb_rounds_played(self):
        return self.round_colors["white"] + self.round_colors["black"]

    def register_round(self, outcome, points, round_color, opponent_name):
        """
        Given the outcome of a round and how many points the player gets, the player state changes
        Outcome: is a win, draw or loss
        Points: how many points the player gets from the round
        Round color: the color of pieces the player played with.
        """

        self.times_win_draw_loss_bye[outcome] += 1
        self.previous_opponents.append(opponent_name)
        self.points += points
        self.round_colors[round_color] += 1

# print(players)
# for player in players:
#     print(f"{player.first_name}, {player.player_id}: {player.points}")
