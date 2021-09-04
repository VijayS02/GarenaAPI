from Champ import Champion
from Item import Item


class Participant():
    """
    Participants are different from users in that a participant id refers to an instance of a player in the given game.
    Participant ids are separate from AccountIds but this object allows them to be linked for a simpler approach.
    """

    def __init__(self, json_data, identity, game):
        self.data = json_data
        self.parent_game = game
        self.identity = identity['player']
        self.summoner = identity['player']['summonerName']
        self.accid = identity['player']['accountId']
        self.partId = json_data['participantId']
        self.champion = Champion(json_data['championId'])

    def get_data(self):
        """
        Simple data getter
        :return: the data of the current game's participant
        """
        return self.data

    def get_stats(self):
        return self.data['stats']

    def get_items(self):
        """
        Get the final items from the given participant
        :return: A list of item objects
        """
        stats = self.get_stats()
        items = []
        for i in range(0, 6):
            itemid = stats[f'item{i}']
            if itemid != 0:
                items.append(Item(itemid))
        return items

    def get_kda(self):
        """
        Gets the KDA of the participant in the given game.
        :return: A tuple containing the (kills, deaths, and assists).
        """
        stats = self.get_stats()
        return (stats['kills'], stats['deaths'], stats['assists'])

    def get_kda_table(self, username=False, KDA=True, WL=True, Champ=True):
        """
        Generate a KDA table similar to op.gg that allows to give a quick overview of a given game.
        :param username: Whether or not to display the username.
        :param KDA: Whether or not to display the KDA.
        :param WL: Whether or not to display the win/loss status.
        :param Champ: Whether or not to display the champion's name.
        :return: Tuple containing the selected items
        """
        win_loss_text = ""
        if self.get_stats()['win']:
            win_loss_text = "Won"
        else:
            win_loss_text = "Loss"
        kills, deaths, assists = self.get_kda()

        ret_val = []
        if username:
            ret_val.append(self.summoner)
        if WL:
            ret_val.append(win_loss_text)
        if KDA:
            ret_val.append(kills)
            ret_val.append(deaths)
            ret_val.append(assists)
        if Champ:
            ret_val.append(self.champion.get_name())
        return tuple(ret_val)

    def __repr__(self):
        return f"<Participant {repr(self.champion)} Game_id:{self.parent_game.get_id()}>"
