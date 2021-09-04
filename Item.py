from Information import get_item_json
# Load the raw item id
RAW_ITEM_DATA = get_item_json()
ITEM_INFO = {item['id']: item for item in RAW_ITEM_DATA}

class Item():
    def __init__(self, id):
        self.id = id
        if id == 0:
            self.info = {'name': "No item"}
        else:
            self.info = ITEM_INFO[id]

    def __repr__(self):
        return f"<Item Object - {self.info['name']}>"
