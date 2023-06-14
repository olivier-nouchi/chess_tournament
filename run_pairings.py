"""
Starts the tournament
Given a spreadsheet with the relevant info, it loads the data and start the tournament with the players.

Need to write at the end of each round the state.


"""
from load_spreadsheet_data import players_from_spreadsheet
from pairings import create_pairings
from utils import PairingMethod, display_players_ranking, display_players_stats, display_pairings_by_player

# Enter the round number
ROUND_NUMBER = 1

if __name__ == "__main__":
    # print(players_from_spreadsheet)
    if ROUND_NUMBER == 1:
        pairings = create_pairings(players=players_from_spreadsheet,
                                   round_number=ROUND_NUMBER,
                                   method=PairingMethod.mid_rating,
                                   display_elo=True
                                   )

    else:
        pairings = create_pairings(players=players_from_spreadsheet,
                                   round_number=ROUND_NUMBER,
                                   method=PairingMethod.points,
                                   display_elo=True
                                   )

    display_pairings_by_player(pairings=pairings)

    display_players_ranking(players=players_from_spreadsheet, display_elo=True, display_tb_points=True)
    display_players_stats(players=players_from_spreadsheet)
