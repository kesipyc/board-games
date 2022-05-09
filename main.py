import json

from bgg import BoardGameGeek
from spreadsheet import Spreadsheet


def get_config():
    with open("configuration.txt") as f:
        data = f.read()
    js = json.loads(data)
    return js


def func_is_game_for_n_players(n):
    return lambda game: game['minplayers'] <= n <= game['maxplayers']


def func_is_game_for_at_least_n_players(n):
    return lambda game: n <= game['maxplayers']


def main():
    config = get_config()

    login = config["bgg-login"]
    password = config["bgg-password"]

    bgg = BoardGameGeek(login, password)

    collection = bgg.get_my_collection()
    # ids_and_names = ({"id": item['objectid'], "name": item['name']['TEXT']} for item in collection['items']['item'])
    ids = (int(item['objectid']) for item in collection['items']['item'])
    # print(list(id_and_names))

    # game = bgg.get_game((63170, 423))
    games = list(bgg.get_games(list(ids)))

    player_1 = func_is_game_for_n_players(1)
    player_2 = func_is_game_for_n_players(2)
    player_3 = func_is_game_for_n_players(3)
    player_4 = func_is_game_for_n_players(4)
    player_5 = func_is_game_for_n_players(5)
    player_6 = func_is_game_for_n_players(6)
    player_7 = func_is_game_for_n_players(7)
    player_at_least_8 = func_is_game_for_at_least_n_players(8)

    games_1_player = list(filter(player_1, games))
    games_2_player = list(filter(player_2, games))
    games_3_player = list(filter(player_3, games))
    games_4_player = list(filter(player_4, games))
    games_5_player = list(filter(player_5, games))
    games_6_player = list(filter(player_6, games))
    games_7_player = list(filter(player_7, games))
    games_more_8_player = list(filter(player_at_least_8, games))

    # games_7_player = Stub.get_7_player()
    # games_more_8_player = Stub.get_at_least_8_player()

    sh = Spreadsheet(config["spreadsheet-credentials"])

    sh.create_tab(str(1), 1, games_1_player)
    sh.create_tab(str(2), 2, games_2_player)
    sh.create_tab(str(3), 3, games_3_player)
    sh.create_tab(str(4), 4, games_4_player)
    sh.create_tab(str(5), 5, games_5_player)
    sh.create_tab(str(6), 6, games_6_player)
    sh.create_tab(str(7), 7, games_7_player)
    sh.create_tab("8+", 8, games_more_8_player)


if __name__ == "__main__":
    main()
