from libbgg.apiv1 import BGG
from libbgg.apiv2 import BGG as BGG2

import urllib.request

from stub import Stub


class BGG2WithAuth(BGG2):
    def __init__(self, login, password, url_base='http://www.boardgamegeek.com', path_base='xmlapi2'):
        self.login = login
        self.password = password
        super().__init__(url_base, path_base)

    def _get_opener(self):
        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, self.url_base, self.login, self.password)

        auth_handler = urllib.request.HTTPBasicAuthHandler(p)

        opener = urllib.request.build_opener(auth_handler)

        return opener


def convert_game(game):
    if type(game.name) == list:
        name = next(item.value for item in game.name if item.type == 'primary')
    else:
        name = game.name.value

    yearpublished = int(game.yearpublished.value)
    minplayers = int(game.minplayers.value)
    maxplayers = int(game.maxplayers.value)
    playingtime = int(game.playingtime.value)
    suggested_numplayers = next(item.results for item in game.poll if item.name == 'suggested_numplayers')
    averageweight = float(game.statistics.ratings.averageweight.value)

    return {
        'name': name,
        'yearpublished': yearpublished,
        'minplayers': minplayers,
        'maxplayers': maxplayers,
        'suggested_numplayers': suggested_numplayers,
        'playingtime': playingtime,
        'averageweight': averageweight
    }


class BoardGameGeek:
    # http://boardgamegeek.com/wiki/page/BGG_XML_API
    # http://boardgamegeek.com/wiki/page/BGG_XML_API2
    # bgg = BGG()

    def __init__(self, login, password) -> None:
        self.login = login
        self.password = password
        self.bgg2 = BGG2WithAuth(login, password)

    def get_games(self, games_ids):
        # games = self.bgg2.boardgame(games_ids, stats=True, ratingcomments=False)
        # return map(convert_game, games['items']['item'])
        return Stub.get_games()

    def get_my_collection(self):
        # return self.bgg2.get_collection(self.login, excludesubtype="boardgameexpansion", showprivate=1, own=1)
        return Stub.get_my_collection()
