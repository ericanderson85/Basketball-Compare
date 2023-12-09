import json
from ordered_set import OrderedSet


class NBAPlayer:
    def __init__(self, file_name: str):
        self.file_name = file_name
        with open(f"cache/{file_name}", "r") as file:
            self.data = json.load(file)
        self.player_name = self.data[1]["resultSets"][0]["rowSet"][0][3]
        self.player_id = self.data[1]["resultSets"][0]["rowSet"][0][0]

    def get_stat_totals(self):
        stats = {}
        for season in self.data[0]["resultSets"][0]["rowSet"]:
            stats[season[1]] = {"PLAYER_ID": season[0],
                                "SEASON_ID": season[1],
                                "LEAGUE_ID": season[2],
                                "TEAM_ID": season[3],
                                "TEAM_ABBREVIATION": season[4],
                                "PLAYER_AGE": season[5],
                                "GP": season[6],
                                "GS": season[7],
                                "MIN": season[8],
                                "FGM": season[9],
                                "FGA": season[10],
                                "FG_PCT": season[11],
                                "FG3M": season[12],
                                "FG3A": season[13],
                                "FG3_PCT": season[14],
                                "FTM": season[15],
                                "FTA": season[16],
                                "FT_PCT": season[17],
                                "OREB": season[18],
                                "DREB": season[19],
                                "REB": season[20],
                                "AST": season[21],
                                "STL": season[22],
                                "BLK": season[23],
                                "TOV": season[24],
                                "PF": season[25],
                                "PTS": season[26]}
        return stats

    def seasons(self):
        # List of all the seasons a player played
        l = OrderedSet()
        for season in self.data[0]["resultSets"][0]["rowSet"]:
            l.add(season[1])
        return l

    def get_stats_per_game(self):
        stats = {}
        for season in self.data[0]["resultSets"][0]["rowSet"]:
            games = season[6]
            if games <= 0:
                continue
            # Some values will be None. These are the stats that weren't always recorded
            stats[season[1]] = {"PLAYER_ID": season[0],
                                "SEASON_ID": season[1],
                                "LEAGUE_ID": season[2],
                                "TEAM_ID": season[3],
                                "TEAM_ABBREVIATION": season[4],
                                "PLAYER_AGE": int(season[5]),
                                "GP": games,
                                "GS": season[7],
                                "MIN": round(season[8] / games, 1) if season[8] is not None else None,
                                "FGM": round(season[9] / games, 1) if season[9] is not None else None,
                                "FGA": round(season[10] / games, 1) if season[10] is not None else None,
                                "FG_PCT": round(season[11] * 100, 1) if season[11] is not None else None,
                                "FG3M": round(season[12] / games, 1) if season[12] is not None else None,
                                "FG3A": round(season[13] / games, 1) if season[13] is not None else None,
                                "FG3_PCT": round(season[14] * 100, 1) if season[14] is not None else None,
                                "FTM": round(season[15] / games, 1) if season[15] is not None else None,
                                "FTA": round(season[16] / games, 1) if season[16] is not None else None,
                                "FT_PCT": round(season[17] * 100, 1) if season[17] is not None else None,
                                "OREB": round(season[18] / games, 1) if season[18] is not None else None,
                                "DREB": round(season[19] / games, 1) if season[19] is not None else None,
                                "REB": round(season[20] / games, 1) if season[20] is not None else None,
                                "AST": round(season[21] / games, 1) if season[21] is not None else None,
                                "STL": round(season[22] / games, 1) if season[22] is not None else None,
                                "BLK": round(season[23] / games, 1) if season[23] is not None else None,
                                "TOV": round(season[24] / games, 1) if season[24] is not None else None,
                                "PF": round(season[25] / games, 1) if season[25] is not None else None,
                                "PTS": round(season[26] / games, 1) if season[26] is not None else None}
        return stats

    def get_stats_simple(self):
        stats = []
        for season in self.data[0]["resultSets"][0]["rowSet"]:
            if season[6] <= 0:
                continue
            games = season[6]
            season_stats = [
                round(season[26] / games,
                      1) if season[26] is not None else None,
                round(season[21] / games,
                      1) if season[21] is not None else None,
                round(season[20] / games,
                      1) if season[20] is not None else None,
                round(season[23] / games,
                      1) if season[23] is not None else None,
                round(season[22] / games,
                      1) if season[22] is not None else None,
                round(season[24] / games,
                      1) if season[24] is not None else None,
                round(season[10] / games,
                      1) if season[10] is not None else None,
                round(season[9] / games,
                      1) if season[9] is not None else None,
                round(season[11] * 100, 1) if season[11] is not None else None,
                round(season[13] / games,  # 3pt Attempted, 9 13.2
                      1) if season[13] is not None else None,
                round(season[12] / games,  # 3pt Made, 10 5.5
                      1) if season[12] is not None else None,
                # 3pt percentage, 11
                round(season[14] * 100, 1) if season[14] is not None else None]
            stats.append((season[0], season[1], season_stats))
        return stats

    def get_stats_per_36(self):
        stats = {}
        for season in self.data[0]["resultSets"][0]["rowSet"]:
            if season[8] == None or season[8] <= 0:
                continue
            # Some values will be None. These are the stats that weren't always recorded
            stats[season[1]] = {"PLAYER_ID": season[0],
                                "SEASON_ID": season[1],
                                "LEAGUE_ID": season[2],
                                "TEAM_ID": season[3],
                                "TEAM_ABBREVIATION": season[4],
                                "PLAYER_AGE": season[5],
                                "GP": season[6],
                                "GS": season[7],
                                "MIN": 36,
                                "FGM": round(36 * season[9] / season[8], 1),
                                "FGA": round(36 * season[10] / season[8], 1),
                                "FG_PCT": season[11],
                                "FG3M": round(36 * season[12] / season[8], 1) if season[12] is not None else None,
                                "FG3A": round(36 * season[13] / season[8], 1) if season[13] is not None else None,
                                "FG3_PCT": season[14],
                                "FTM": round(36 * season[15] / season[8], 1),
                                "FTA": round(36 * season[16] / season[8], 1),
                                "FT_PCT": season[17],
                                "OREB": round(36 * season[18] / season[8], 1) if season[18] is not None else None,
                                "DREB": round(36 * season[19] / season[8], 1) if season[19] is not None else None,
                                "REB": round(36 * season[20] / season[8], 1) if season[20] is not None else None,
                                "AST": round(36 * season[21] / season[8], 1),
                                "STL": round(36 * season[22] / season[8], 1) if season[22] is not None else None,
                                "BLK": round(36 * season[23] / season[8], 1) if season[23] is not None else None,
                                "TOV": round(36 * season[24] / season[8], 1) if season[24] is not None else None,
                                "PF": round(36 * season[25] / season[8], 1),
                                "PTS": round(36 * season[26] / season[8], 1)}
        return stats

    def get_info(self):
        rowSet = self.data[1]["resultSets"][0]["rowSet"][0]
        return {"PERSON_ID": rowSet[0],
                "FIRST_NAME": rowSet[1],
                "LAST_NAME": rowSet[2],
                "DISPLAY_FIRST_LAST": rowSet[3],
                "DISPLAY_LAST_COMMA_FIRST": rowSet[4],
                "DISPLAY_FI_LAST": rowSet[5],
                "PLAYER_SLUG": rowSet[6],
                "BIRTHDATE": rowSet[7],
                "SCHOOL": rowSet[8],
                "COUNTRY": rowSet[9],
                "LAST_AFFILIATION": rowSet[10],
                "HEIGHT": rowSet[11],
                "WEIGHT": rowSet[12],
                "SEASON_EXP": rowSet[13],
                "JERSEY": rowSet[14],
                "POSITION": rowSet[15],
                "ROSTERSTATUS": rowSet[16],
                "GAMES_PLAYED_CURRENT_SEASON_FLAG": rowSet[17],
                "TEAM_ID": rowSet[18],
                "TEAM_NAME": rowSet[19],
                "TEAM_ABBREVIATION": rowSet[20],
                "TEAM_CODE": rowSet[21],
                "TEAM_CITY": rowSet[22],
                "PLAYERCODE": rowSet[23],
                "FROM_YEAR": rowSet[24],
                "TO_YEAR": rowSet[25],
                "DLEAGUE_FLAG": rowSet[26],
                "NBA_FLAG": rowSet[27],
                "GAMES_PLAYED_FLAG": rowSet[28],
                "DRAFT_YEAR": rowSet[29],
                "DRAFT_ROUND": rowSet[30],
                "DRAFT_NUMBER": rowSet[31],
                "GREATEST_75_FLAG": rowSet[32]}
