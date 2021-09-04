from Game import Game
from Information import rolling_average
from Requetsts_functions import general_data_request
from tqdm import tqdm
MIN_STEP = 10


class User():
    username: str
    accountId: str
    region: str
    games: dict
    game_data: list[Game]

    def __init__(self, username: str, region: str = "TW"):
        """
        Initializes a user object
        :param username: Username on the given region
        :param region: Region to look into (e.g. TW, PH, SG...)
        """
        user_info = {"name": username, "region": region}

        account_info = general_data_request("https://acs-garena.leagueoflegends.com/v1/players",
                                            params=user_info)

        self.username = username
        self.region = region
        self.accountId = account_info['accountId']

        link = f"https://acs-garena" \
               f".leagueoflegends.com/v1/stats/player_history/{self.region}/{self.accountId}"

        user_data = general_data_request(link)
        self.games = user_data['games']

    def get_games(self, n=None, inplace=True):
        """
        Loads the given numbere of games, if n is none, then it will select as many as available from the api.
        :param n: Number of games to lookup.
        :param inplace: Loads the game data into the User object's game_data attribute.
        :return: A list of game objects.
        """
        link = f"https://acs-garena" \
               f".leagueoflegends.com/v1/stats/player_history/{self.region}/{self.accountId}"
        print(link)
        if n is None:
            n = self.games['gameCount']

        game_data = []
        for i in tqdm(range(0, n, MIN_STEP)):
            data = general_data_request(link, params={'begIndex': i,
                                                      'endindex': min(n, i + MIN_STEP)})

            for game in data['games']['games']:
                game_data.append(Game(game))

            if len(data['games']['games']) != MIN_STEP:
                print("No more games.")
                break
        if inplace:
            self.game_data = game_data
            self.sort_games()
        return game_data

    def get_game_ids(self):
        """
        Gets the game identifier based on currently loaded games.
        :return: A list of ids
        """
        ids = []
        for game in self.game_data:
            ids.append(game.get_id())
        return ids

    def sort_games(self, reverse=True):
        """
        Sort game data loaded into the current object.
        :param reverse: To reverse the order of sorting
        """
        self.game_data = sorted(self.game_data, key=lambda x: x.meta_info['gameCreation'],
                                reverse=reverse)

    def get_kds(self, n):
        """
        Simple function to get KDAs of this current user based on n games
        :param n: the number of games to get kds for
        :return: lists, each containing the kds, kdas, kills and times of each game
        """
        if n is None:
            n = len(self.game_data)

        kds = []
        kdas = []
        kills = []
        times = []
        for i in range(n):
            _, k, d, a, _ = self.game_data[i].get_participant_acc(self.accountId).get_kda_table()
            time = self.game_data[i].get_game_time()
            if d == 0:
                d = 1
            kd = k/d
            kda = (k+a)/d
            kds.append(kd)
            kills.append(k)
            kdas.append(kda)
            times.append(time)
        return kds, kdas, kills, times

    def show_latest_games(self, n):
        """
        Display the games in a more neatly formatted order.
        :param n: Number of games to display
        """
        if n is None:
            n = len(self.game_data)

        rev_data = self.game_data
        print(f"{'#': ^4}| {'Res': ^5} | {'K': ^3}/{'D': ^3}/{'A': ^3} | {'Champion': ^12} | Time ")
        print('-' * 50)
        for i in tqdm(range(0, n)):
            try:
                part = rev_data[i].get_participant_acc(self.accountId)
                w_l, k, d, a, champ = part.get_kda_table()
                print(f"{i:^4}| {w_l:^5} | {k: ^ 3}/{d: ^ 3}/{a: ^ 3} |" \
                      f" {champ: ^12} | {rev_data[i].get_game_time_str()}")
            except IndexError:
                print("End of collected data.")
