from utils import ResultOutcome


class BoardResult:
    def __init__(self, white_player, black_player, outcome: ResultOutcome, white_player_points, black_player_points):
        self.white_player = white_player
        self.black_player = black_player
        self.outcome = outcome
        self.white_player_points = white_player_points
        self.black_player_points = black_player_points

    def __str__(self):
        a = ''
        if self.outcome == ResultOutcome.draw:
            a = f"{self.outcome.value}!"
        if self.outcome == ResultOutcome.win:
            a = f"{self.white_player.full_name} wins!"
        if self.outcome == ResultOutcome.loss:
            a = f"{self.black_player.full_name} wins!"
        if self.outcome == ResultOutcome.bye:
            a = f"{self.white_player.full_name} takes a BYE!"

        b = f"{self.white_player.full_name} earns {self.white_player_points}"
        c = f"{self.black_player.full_name} earns {self.black_player_points}"
        return a + "\n" + b + "\n" + c
