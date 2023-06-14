import pandas as pd
from typing import List

from players import ChessPlayer
from spreadsheet_data import SHEET_ID, SHEET_ROUNDS, SHEET_PLAYERS


def load_df_from_spreadsheet(sheet_id: str, sheet_name: str):
    spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(spreadsheet_url, on_bad_lines='skip')
    return df


def create_players_from_spreadsheet(df: pd.DataFrame) -> List[ChessPlayer]:
    players = []

    players_ids = df["player_id"].unique()

    for player_id in players_ids:
        player_first_name = df[df["player_id"] == player_id]["first_name"].values[0]
        player_last_name = df[df["player_id"] == player_id]["last_name"].values[0]
        player_is_active = df[df["player_id"] == player_id]["is_active"].values[0]
        player_rating = df[df["player_id"] == player_id]["ELO"].values[0]

        player_points = sum(df[df["player_id"] == player_id]["points"].dropna().values)

        player_win = list(df[df["player_id"] == player_id]["win_loss_draw_bye"].dropna().values).count("win")
        player_draw = list(df[df["player_id"] == player_id]["win_loss_draw_bye"].dropna().values).count("draw")
        player_loss = list(df[df["player_id"] == player_id]["win_loss_draw_bye"].dropna().values).count("loss")
        player_bye = list(df[df["player_id"] == player_id]["win_loss_draw_bye"].dropna().values).count("bye")

        player_white = list(df[df["player_id"] == player_id]["white_black"].dropna().values).count("white")
        player_black = list(df[df["player_id"] == player_id]["white_black"].dropna().values).count("black")

        player_previous_opponents = df[df["player_id"] == player_id]["opponent_id"].dropna().astype(int).values

        player = ChessPlayer(player_id=player_id,
                             first_name=player_first_name,
                             last_name=player_last_name,
                             elo_rating=player_rating,
                             is_active=player_is_active,
                             is_paired=False)

        setattr(player, "points", player_points)
        setattr(player, "round_colors", {"white": player_white, "black": player_black})
        setattr(player, "times_win_draw_loss_bye",
                {"win": player_win, "draw": player_draw, "loss": player_loss, "bye": player_bye})
        setattr(player, "previous_opponents", player_previous_opponents)

        players.append(player)

    # set TB points
    PLAYERS_BY_ID = {player.player_id: player for player in players}
    for player in players:
        player.tb_points = sum([PLAYERS_BY_ID[player_id].points if player_id != 0 else 0 for player_id in player.previous_opponents])

    return players


rounds_df = load_df_from_spreadsheet(sheet_id=SHEET_ID, sheet_name=SHEET_ROUNDS)
players_from_spreadsheet = create_players_from_spreadsheet(df=rounds_df)
