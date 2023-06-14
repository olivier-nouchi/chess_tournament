from typing import List

from players import ChessPlayer
from tournament_round import TournamentRound
from board_result import BoardResult
from random import shuffle, choice
from utils import PairingMethod, ResultOutcome, sacrifices_points_mapping, BASE_VICTORY, BASE_DRAW, DRAW_PENALTY, BYE_PLAYER
from players_list import PLAYERS_EXAMPLE
from tournament import Tournament


def create_pairings(players: List[ChessPlayer], round_number: int, method: PairingMethod = PairingMethod.points,
                    display_elo: bool = True):
    """ Given a list of players with points, it creates a pairing between the players based on the method used"""
    pairings = []
    for player in players:
        player.is_paired = False
    player1_BYE, player2_BYE = None, None

    if method == PairingMethod.points:
        shuffle(players)  # makes sure that even for the 1st round it's random
        sorted_player_by_points = sorted(players, key=lambda p: p.points, reverse=True)
        active_sorted_player_by_points = [p for p in sorted_player_by_points if p.is_active]

        # Give a BYE to non-active players and with no points

        # if the number of active players is odd, someone is going to get a BYE (and some points)
        if len(active_sorted_player_by_points) % 2 == 1:
            # pick the last player with no BYE already
            player1_BYE = [player for player in sorted_player_by_points if player.times_win_draw_loss_bye[ResultOutcome.bye.value] == 0][-1]
            player1_BYE.times_win_draw_loss_bye[ResultOutcome.bye.value] += 1
            player2_BYE = BYE_PLAYER
            player1_BYE.is_paired = True

        # Make sure that now the number of players is even
        not_paired_players = [player for player in active_sorted_player_by_points if not player.is_paired]
        assert len(not_paired_players) % 2 == 0

        while not_paired_players:
            possible_players = {}
            # Need to prioritize the pairing of players who have the least matchmaking possibilities
            for player in not_paired_players:
                possible_players_to_pair_with = [player_ for player_ in not_paired_players if player_ != player and player_.player_id not in player.previous_opponents]
                possible_players[player] = len(possible_players_to_pair_with)
            not_paired_players_sorted_by_n_opp = sorted(not_paired_players, key=lambda p: possible_players.get(p), reverse=False)

            player1 = not_paired_players_sorted_by_n_opp[0]  # the first player we want to match is the one with the least possible choices
            possible_players_to_pair_with = [player for player in not_paired_players_sorted_by_n_opp if player != player1 and player.player_id not in player1.previous_opponents]
            player2 = possible_players_to_pair_with[0]

            player1.is_paired = True
            player2.is_paired = True

            not_paired_players.remove(player1)
            not_paired_players.remove(player2)

            # Decide who is W and who is B
            if player1.round_colors.get("white") > player2.round_colors.get("white"):
                pairings.append((player2, player1))

            if player1.round_colors.get("white") < player2.round_colors.get("white"):
                pairings.append((player1, player2))

            if player1.round_colors.get("white") == player2.round_colors.get("white"):
                # randomize
                players12 = [player1, player2]
                shuffle(players12)
                pairings.append(tuple(players12))

    if method == PairingMethod.random:
        pass
    if method == PairingMethod.mid_rating:
        sorted_player_by_rating = sorted(players, key=lambda p: p.elo_rating, reverse=True)
        active_sorted_player_by_rating = [p for p in sorted_player_by_rating if p.is_active]

        if len(active_sorted_player_by_rating) % 2 == 1:
            # pick the last player with no BYE already
            player1_BYE = [player for player in active_sorted_player_by_rating if player.times_win_draw_loss_bye[ResultOutcome.bye.value] == 0][-1]
            player1_BYE.times_win_draw_loss_bye[ResultOutcome.bye.value] += 1
            player2_BYE = BYE_PLAYER
            player1_BYE.is_paired = True

        # Make sure that now the number of players is even
        not_paired_players = [player for player in active_sorted_player_by_rating if not player.is_paired]
        assert len(not_paired_players) % 2 == 0

        print(not_paired_players)
        for index, _ in enumerate(not_paired_players):
            if index == len(not_paired_players)//2:
                break
            player1, player2 = not_paired_players[index], not_paired_players[index+len(not_paired_players)//2]

            players12 = [player1, player2]
            shuffle(players12)
            pairings.append(tuple(players12))

    if player1_BYE and player2_BYE:
        pairings.append((player1_BYE, player2_BYE))

    inactive_players = [player for player in players if not player.is_active]
    if inactive_players:
        print(f"Careful, players {inactive_players} are not active")
    not_paired_players = [player for player in players if not player.is_paired]
    if not_paired_players:
        print(f"Careful, players {not_paired_players} are not paired")
    if not pairings:
        print(f"Careful, the pairings are empty!")

    display_pairings(pairings=pairings, round_number=round_number, display_elo=display_elo)
    return pairings


def display_pairings(pairings: List, round_number: int, display_elo: bool = False):
    print(f"----- Pairings for Round {round_number} -----")
    display_elo_str_1, display_elo_str_2 = "", ""
    for table_num, pairing in enumerate(pairings):
        player1, player2 = pairing

        if display_elo:
            display_elo_str_1 = f"[{player1.elo_rating}]"
            display_elo_str_2 = f"[{player2.elo_rating}]"

        print(f"Table {table_num+1} | {player1.full_name}{display_elo_str_1} ({player1.points} pts) (W) - {player2.full_name}{display_elo_str_2} ({player2.points} pts) (B)")


def create_random_tournament_round(players: List[ChessPlayer], round_number: int) -> TournamentRound:
    tr = TournamentRound(round_number=round_number)
    wpp, bpp = 0, 0
    total_points_round = 0

    pairings = create_pairings(players=players, method=PairingMethod.points)

    for pairing in pairings:
        player_w, player_b = pairing
        outcome = choice((ResultOutcome.win, ResultOutcome.draw, ResultOutcome.loss))
        if outcome == ResultOutcome.win:
            wpp = BASE_VICTORY + choice(list(sacrifices_points_mapping.values()))
            bpp = 0
        if outcome == ResultOutcome.loss:
            wpp = 0
            bpp = BASE_VICTORY + choice(list(sacrifices_points_mapping.values()))
        if outcome == ResultOutcome.draw:
            wpp = BASE_DRAW + choice(list(sacrifices_points_mapping.values())) / DRAW_PENALTY
            bpp = BASE_DRAW + choice(list(sacrifices_points_mapping.values())) / DRAW_PENALTY
        br = BoardResult(white_player=player_w,
                         black_player=player_b,
                         outcome=outcome,
                         white_player_points=wpp,
                         black_player_points=bpp)
        total_points_round += wpp + bpp
        tr.board_results.append(br)

    print(f"END OF ROUND {round_number}")

    return tr

# 
# # TODO: add a condition the #rounds > #players
# Tournament = Tournament(players=PLAYERS_EXAMPLE)
# for tr_n in range(7):
#     tr = create_random_tournament_round(players=PLAYERS_EXAMPLE, round_number=tr_n+1)
#     tr.apply_tournament_round_to_players(players=PLAYERS_EXAMPLE)
#     Tournament.get_tournament_state()
