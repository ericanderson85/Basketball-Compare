import os
from nbaplayer import NBAPlayer
from nba_api.stats.static import players


def main():
    print(info(NBAPlayer("2200.json"))["TEAM_NAME"])


def priority(player, season, attributes, criteria="per_game"):
    # If only one attribute is given turn it to a list
    if not isinstance(attributes, list):
        attributes = [attributes]
    most_similar_season = []
    for other_player in all_players():
        if other_player.player_id == player.player_id:
            continue
        for other_season in other_player.seasons():
            # skip_season is true when the other player's attribute is unavailable or more than 50% different than the player's attribute
            skip_season = False
            try:
                other_attrs = []
                player_attrs = []
                for attr in attributes:
                    other_attr = get_stat(
                        other_player, attr, other_season, criteria)
                    try:
                        player_attr = get_stat(player, attr, season, criteria)
                    except TypeError:
                        # Attribute provided wasn't recorded in the given season
                        return "Attributes unavailable"
                    if other_attr == None or player_attr == None:
                        skip_season = True
                        break
                    difference = abs(player_attr - other_attr)
                    if other_attr + player_attr == 0 or (difference / ((other_attr + player_attr) / 2) * 100) > 50:
                        skip_season = True
                        break
                    # Create lists to find the euclidean distance of the percentage differences for the attributes
                    other_attrs.append(other_attr)
                    player_attrs.append(player_attr)
            except TypeError:
                continue
            if not skip_season:
                # Euclidean distance of the two players' seasons in regards to the percentage difference of each attribute
                similarity = distance(other_attrs, player_attrs)
                if len(most_similar_season) == 0 or similarity < most_similar_season[0]:
                    most_similar_season = [similarity, [
                        other_player.player_name, other_season]]
    # Return the closest season
    return most_similar_season[1]


def get_stat(player: NBAPlayer, attr: str, season: str, criteria: str):
    match criteria:
        case "totals":
            return totals(player=player, attribute=attr)[season]
        case "per_game":
            return per_game(player=player, attribute=attr)[season]
        case "per_36":
            return per_36(player=player, attribute=attr)[season]


def distance(a: list, b: list):
    distance = sum(abs((p - q) / ((p + q) / 2))
                   for p, q in zip(a, b) if p + q != 0)
    return distance


def all_players():
    # All players in NBA history as a list of Player objects
    players = []
    for file in os.listdir("cache/"):
        if ".json" in file:
            players.append(NBAPlayer(file))
    return players


def active_players():
    # List of all players currently playing in the NBA
    player_list = []
    for active_player in players.get_active_players():
        player_list.append(NBAPlayer(f"{active_player['id']}.json"))
    return player_list


def inactive_players():
    # List of all players currently playing in the NBA
    player_list = []
    for inactive_player in players.get_inactive_players():
        player_list.append(NBAPlayer(f"{inactive_player['id']}.json"))
    return player_list


def all_seasons():
    # 1946-47 -> 2023-24 as a list
    year = 1946
    seasons = []
    while year <= 2023:
        seasons.append(f"{year}-{str(year + 1)[-2:]}")
        year += 1
    return seasons


def info(player: NBAPlayer):
    # "PERSON_ID", "FIRST_NAME", "LAST_NAME", "DISPLAY_FIRST_LAST", "DISPLAY_LAST_COMMA_FIRST", "DISPLAY_FI_LAST", "PLAYER_SLUG",
    # "BIRTHDATE", "SCHOOL", "COUNTRY", "LAST_AFFILIATION", "HEIGHT", "WEIGHT", "SEASON_EXP", "JERSEY", "POSITION", "ROSTERSTATUS",
    # "TEAM_ID", "TEAM_NAME", "TEAM_ABBREVIATION", "TEAM_CODE", "TEAM_CITY", "PLAYERCODE", "FROM_YEAR", "TO_YEAR", "DLEAGUE_FLAG",
    # "NBA_FLAG", "GAMES_PLAYED_FLAG", "DRAFT_YEAR", "DRAFT_ROUND", "DRAFT_NUMBER"
    return player.get_info()


def totals(player: NBAPlayer, attribute: str):
    total_stats = player.get_stat_totals()
    attribute_all_seasons = {}
    for season in total_stats.keys():
        attribute_all_seasons[season] = (total_stats[season][attribute])
    return attribute_all_seasons


def per_game(player: NBAPlayer, attribute: str):
    per_game_stats = player.get_stats_per_game()
    attribute_all_seasons = {}
    for season in per_game_stats.keys():
        attribute_all_seasons[season] = (per_game_stats[season][attribute])
    return attribute_all_seasons


def per_36(player: NBAPlayer, attribute: str):
    per_36_stats = player.get_stats_per_36()
    attribute_all_seasons = {}
    for season in per_36_stats.keys():
        attribute_all_seasons[season] = (per_36_stats[season][attribute])
    return attribute_all_seasons


if __name__ == "__main__":
    main()
