from tkinter import StringVar
from indiek.core.items import Item as CoreItem


class GUIItem(CoreItem):
    """
    Indiek GUI Item.

    This subclasses the core Item class and adds some GUI-specific functionality.
    """
    def __str__(self):
        return f"GUI Item with ID {self._ikid} and name {self.name}"
    
    def __init__(self, name_var: StringVar, content_var: StringVar, **kwargs):
        super().__init__(**kwargs)
        self.name_var = name_var
        self.content_var = content_var

    def update_name(self, name: str):
        self.name_var.set(name)
        self.name = name

    def update_content(self, content: str):
        self.content_var.set(content)
        self.content = content


def core_to_gui_item(core_item: CoreItem, name_var: StringVar, content_var: StringVar) -> GUIItem:
    return GUIItem(
        name_var=name_var,
        content_var=content_var,
        name=core_item.name, 
        content=core_item.content, 
        _ikid=core_item._ikid
        )