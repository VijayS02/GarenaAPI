from Champ import Champion

class Team():
    """
    Team object
    """

    def __init__(self, data, parent_game):
        self.teamId = data['teamId']
        self.parent_game = parent_game

        if data['win'] == "Win":
            self.victory = True
        else:
            self.victory = False

        self.first_blood = data['firstBlood']
        self.first_tower = data['firstTower']
        self.first_inhib = data['firstInhibitor']
        self.first_baron = data['firstBaron']
        self.first_dragon = data['firstDragon']
        self.first_rift_herald = data['firstRiftHerald']
        self.tower_kills = data['towerKills']
        self.inhib_kills = data['inhibitorKills']
        self.baron_kills = data['baronKills']
        self.dragon_kills = data['dragonKills']
        self.rift_kills = data['riftHeraldKills']
        self.bans = []
        for ban in data['bans']:
            self.bans.append(Champion(ban['championId']))

    def __repr__(self):
        if self.teamId == 100:
            return f"<Team Red- Game:{self.parent_game.gameId}>"
        return f"<Team Blue- Game:{self.parent_game.gameId}>"
