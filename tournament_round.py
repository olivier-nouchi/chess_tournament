from players import ChessPlayer
from typing import List
from board_result import BoardResult
from utils import ResultOutcome


class TournamentRound:

    def __init__(self, board_results: List[BoardResult] = None, round_number: int = None):
        if board_results is None:
            board_results = []
        self.board_results = board_results
        self.round_number = round_number

    @staticmethod
    def get_black_outcome(white_outcome: ResultOutcome):
        if white_outcome == ResultOutcome.win:
            return ResultOutcome.loss
        if white_outcome == ResultOutcome.loss:
            return ResultOutcome.win
        if white_outcome == ResultOutcome.draw:
            return ResultOutcome.draw
        if white_outcome == ResultOutcome.bye:
            return ResultOutcome.bye
        else:
            return None

    def apply_tournament_round_to_players(self, players: List[ChessPlayer]):
        PLAYERS_BY_ID = {player.player_id: player for player in players}
        for br in self.board_results:
            w_player = PLAYERS_BY_ID.get(br.white_player.player_id)
            if not w_player:
                continue
            b_player = PLAYERS_BY_ID.get(br.black_player.player_id)
            if not b_player:
                continue
            w_player.points += br.white_player_points
            b_player.points += br.black_player_points
            white_outcome = br.outcome
            black_outcome = self.get_black_outcome(white_outcome=white_outcome)
            w_player.round_colors["white"] += 1
            w_player.times_win_draw_loss_bye[white_outcome.value] += 1
            w_player.previous_opponents.append(b_player.player_id)
            b_player.round_colors["black"] += 1
            b_player.times_win_draw_loss_bye[black_outcome.value] += 1
            b_player.previous_opponents.append(w_player.player_id)
