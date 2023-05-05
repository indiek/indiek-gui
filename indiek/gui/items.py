from indiek.core.items import Item


class GUIItem(Item):
    def display(self):
        return str(self.to_dict())
    

def core_to_gui_item(core_item: Item) -> GUIItem:
    return GUIItem(name=core_item.name, content=core_item.content)