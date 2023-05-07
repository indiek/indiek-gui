from tkinter import StringVar
from indiek.core.items import (Item as CoreItem,
                               Definition as CoreDefinition,
                               Proof as CoreProof,
                               Theorem as CoreTheorem)


class Item(CoreItem):
    """
    Indiek GUI Item.

    This subclasses the core Item class and adds some GUI-specific functionality.
    """

    def __str__(self):
        return f"GUI {self.__class__.__name__} with ID {self._ikid} and name {self.name}"

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


class Definition(Item, CoreDefinition):
    pass


class Proof(Item, CoreProof):
    pass


class Theorem(Item, CoreTheorem):
    pass


CORE_TO_GUI_TYPES = {
    CoreDefinition: Definition,
    CoreProof: Proof,
    CoreTheorem: Theorem
}


def core_to_gui_item(core_item: CoreItem, name_var: StringVar, content_var: StringVar) -> Item:
    return CORE_TO_GUI_TYPES[core_item.__class__](
        name_var=name_var,
        content_var=content_var,
        name=core_item.name,
        content=core_item.content,
        _ikid=core_item._ikid
    )
