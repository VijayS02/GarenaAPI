import numpy as np

from Requetsts_functions import general_data_request, raw_cache
VERSION = '11.14.1'

@raw_cache
def get_champion_detailed(id, searched):
    if id in searched:
        return searched[id]
    champ = general_data_request("https://raw.communitydragon.org/latest/plugins/"
                                 f"rcp-be-lol-game-data/global/default/v1/champions/{id}.json")

    searched[id] = champ
    return champ

@raw_cache
def get_champion_json():
    data = general_data_request("https://raw.communitydragon.org/latest/plugins/"
                                "rcp-be-lol-game-data/global/default/v1/champion-summary.json")

    return data

@raw_cache
def get_item_json():
    data = general_data_request("https://raw.communitydragon.org/latest/plugins/"
                                "rcp-be-lol-game-data/global/default/v1/items.json")
    return data


def rolling_average(x, window_size=5):
    # https://stackoverflow.com/a/54628145
    return np.convolve(x, np.ones(window_size), 'valid') / window_size

if __name__ == "__main__":
    print(get_item_json()['1036'])
