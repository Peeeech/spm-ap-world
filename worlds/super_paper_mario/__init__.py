from worlds.AutoWorld import World
from BaseClasses import Item, Location
from .items import item_name_to_id, item_id_to_name

#NOTE: in-code game name subject to change--was the result of the Manual APWorld Builder

class SuperPaperMarioItem(Item):
    game = "Manual_SuperPaperMario_L5050PeeeeeechSeaturtle"


class SuperPaperMarioLocation(Location):
    game = "Manual_SuperPaperMario_L5050PeeeeeechSeaturtle"


class SuperPaperMarioWorld(World):
    game = "Manual_SuperPaperMario_L5050PeeeeeechSeaturtle"

    item_name_to_id = {
        "Placeholder Item": 1
    }

    location_name_to_id = {
        "Placeholder Location": 1
    }

    def create_item(self, name: str):
        return SuperPaperMarioItem(
            name,
            classification=0,  # filler
            code=self.item_name_to_id[name],
            player=self.player
        )
