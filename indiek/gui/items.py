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
    _str_var_names = ['name_var', 'content_var']
    _str_var_to_core_attr = {
        'name_var': 'name',
        'content_var': 'content'
    }
    _core_attr_to_str_var = {v: k for k, v in _str_var_to_core_attr.items()}

    def __str__(self):
        return f"GUI {self.__class__.__name__} with ID {self._ikid} and name {self.name}"

    def __init__(self, name_var: StringVar, content_var: StringVar, **kwargs):
        super().__init__(**kwargs)
        self.name_var = name_var
        self.content_var = content_var

    def update_str_var(self, var_name: str, new_value: str, set_core_attr: bool = False):
        getattr(self, var_name).set(new_value)
        if set_core_attr:
            setattr(self, self._str_var_to_core_attr[var_name], new_value)

    def reload(self):
        super().reload()
        for core_attr, str_var in self._core_attr_to_str_var.items():
            new_val = getattr(self, core_attr)
            self.update_str_var(str_var, new_val, set_core_attr=False)

    def delete(self):
        super().delete()
        for n in self._str_var_names:
            self.update_str_var(n, '', set_core_attr=True)

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
    kwargs = dict(name_var=name_var, content_var=content_var)
    kwargs.update({a: getattr(core_item, a) for a in core_item._attr_defs})
    return CORE_TO_GUI_TYPES[core_item.__class__](**kwargs)
