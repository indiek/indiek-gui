from tkinter import ttk
from typing import Optional, Mapping, Any


_ENTRY_DEFAULT_LENGTH = 54
_DEFAULT_FONT = ('Century 9')
_STYLES = {
    'entries': {
        'Generic.TEntry': dict(
            font=_DEFAULT_FONT,
            width=_ENTRY_DEFAULT_LENGTH,
        ),
        'DebugGeneric.TEntry': dict(
            font=_DEFAULT_FONT,
            width=_ENTRY_DEFAULT_LENGTH,
        ),
    },
    'labels': {
        'Generic.TLabel': dict(
            padding=3
        ),
        'DebugGeneric.TLabel': dict(
            borderwidth=1,
            relief='solid',
            padding=3
        ),
    },
    'buttons': {
        'DebugGeneric.TButton': dict(),
        'Generic.TButton': dict()
    },
    'panels': {
        'DebugRightpanel.TLabelframe': dict(
            background='green',
            padding=10,
        ),
        'Rightpanel.TLabelframe': dict(
            padding=10,
        ),
        'Leftpanel.TLabelframe': dict(
            foreground='black',
            padding=10,
            ),
        'DebugLeftpanel.TLabelframe': dict(
            background='yellow',
            foreground='black',
            padding=10,
            ),
    },
    'frames': {
        'Searchbar.TFrame': dict(
            foreground='black',
            padding=5
        ),
        'DebugSearchbar.TFrame': dict(
            background='orange',
            foreground='black',
            padding=5
        ),
        'ItemView.TFrame': dict(
            borderwidth=1, 
            relief='groove'
        ),
        'DebugItemView.TFrame': dict(
            borderwidth=1, 
            relief='groove'
        ),
    }
}


class IndieKStyle(ttk.Style):   
    def __init__(
            self, 
            style_name: Optional[str] = None, 
            options: Optional[Mapping[str, Any]] = None, 
            ):
        super().__init__()
        
        self.ik_name = style_name
        if options is None:
            options = self._ik_options
        self.configure(self.ik_name, **options)


class IndiekTheme:
    indices = (
        'buttons',
        'panels',
        'frames',
        'panels',
        'labels',
        'frames',
        'entries',
    )

    style_names = (
        'Generic.TButton',
        'Rightpanel.TLabelframe',
        'Searchbar.TFrame',
        'Leftpanel.TLabelframe',
        'Generic.TLabel',
        'ItemView.TFrame',
        'Generic.TEntry'
    )

    attr_names = (
        'button',
        'right_panel',
        'searchbar',
        'left_panel',
        'generic_label',
        'item_view',
        'generic_entry',
    )

    def __init__(self, debug: bool = False):
        if debug:
            names = list(map(lambda x: 'Debug' + x, self.style_names))        
        else:
            names = self.style_names

        iterator = zip(self.attr_names, self.indices, names)
        for attr_name, index, style_name in iterator:
            self.initialize_attr(attr_name, index, style_name)

    def initialize_attr(self, attr_name, index, style_name):
        config = _STYLES[index][style_name]
        attr_val = IndieKStyle(style_name, config)
        setattr(self, attr_name, attr_val)
        