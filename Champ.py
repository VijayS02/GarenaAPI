from Information import get_champion_detailed, get_champion_json
RAW_CHAMP = get_champion_json()
CHAMP_SUMMARY = {champ['id']: champ for champ in RAW_CHAMP}
CHAMP_DATA = {}

class Champion():

    def __init__(self, champId):
        self.id = champId
        self.info = None
        self.details = None
        self.info = CHAMP_SUMMARY[self.id]

    def get_details(self):
        self.details = get_champion_detailed(self.id, CHAMP_DATA)
        return self.details

    def get_name(self):
        return self.info['name']

    def __repr__(self):
        return self.get_name()
