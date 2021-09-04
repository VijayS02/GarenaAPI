from datetime import datetime

from Participant import Participant
from Requetsts_functions import general_data_request
from Team import Team


def data_req(func):
    def wrapper(*args, **kwargs):
        if not args[0].lookedUp:
            print("Game data not checked, making request")
            args[0].get_data()
            return func(*args, **kwargs)
            # raise KeyError("This function requires looked up data. Please run get_data first.")
        else:
            return func(*args, **kwargs)

    return wrapper


class Game():
    gameId: str
    teams: list[Team]
    region: str
    participants: list[Participant]
    meta_info: dict
    lookedUp: bool

    def __init__(self, json_data):
        self.gameId = json_data['gameId']
        self.region = json_data['platformId']
        self.participants = self.setup_participants(json_data['participants'],
                                                    json_data['participantIdentities'])

        del json_data['participants']
        del json_data['participantIdentities']
        del json_data['platformId']
        del json_data['gameId']

        self.meta_info = json_data
        self.lookedUp = False

    def __repr__(self):
        return f"<Game Object- GameId:{self.gameId}>"

    def get_data(self):
        link = f"https://acs-garena.leagueoflegends.com/v1/stats/game/{self.region}/{self.gameId}"
        game_data = general_data_request(link)
        return_value = game_data.copy()

        self.participants = self.setup_participants(game_data['participants'],
                                                    game_data['participantIdentities'])

        self.teams = []
        for team in game_data['teams']:
            self.teams.append(Team(team, self))

        del game_data['participants']
        del game_data['participantIdentities']
        del game_data['teams']
        del game_data['platformId']
        del game_data['gameId']

        self.meta_info = game_data
        self.lookedUp = True
        return return_value

    def setup_participants(self, participants, identities):
        parts = []
        for participant in participants:
            for identity in identities:
                if identity['participantId'] == participant['participantId']:
                    parts.append(Participant(participant, identity, self))
        return parts

    def get_game_time_str(self, format='%Y-%m-%d %H:%M:%S'):
        return self.get_game_time().strftime(format)

    def get_game_time(self):
        return datetime.utcfromtimestamp(self.meta_info['gameCreation'] / 1000)

    @data_req
    def get_winning_team(self):
        for team in self.teams:
            if team.victory:
                return team

        # Should be impossible
        return None

    def get_participant_name(self, name):
        for participant in self.participants:
            if participant.summoner == name:
                return participant
        raise ValueError(f"Player {name} was not in game {self.gameId}.")

    def get_participant_acc(self, acc):
        for participant in self.participants:
            if participant.accid == acc:
                return participant
        raise ValueError(f"Player {acc} was not in game {self.gameId}.")

    @data_req
    def get_game_information(self):
        print(f"{'Champion': ^12} | {'K': ^3} / {'D': ^3} / {'A': ^3} "
              f"| {'Summoner': <}")
        print("-"*50)
        for participant in self.participants:
            username, k, d, a, champ = participant.get_kda_table(username=True, WL=False)
            print(f"{champ: ^12} | {k: ^ 3} / {d: ^ 3} / {a: ^ 3} |" \
                  f" {username:<}")


    def get_id(self):
        return self.gameId
