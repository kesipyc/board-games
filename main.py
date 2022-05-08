from bgg import BoardGameGeek
import json


def get_config():
    with open("configuration.txt") as f:
        data = f.read()
    js = json.loads(data)
    return js


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
    print(games)


if __name__ == "__main__":
    main()
