from tkinter import ttk
from typing import Optional, Mapping, Any

_STYLES = {
    'buttons': {
        'DebugGeneric.TButton': dict(),
        'Generic.TButton': dict()
    },
    'panels': {
        'DebugRightpanel.TLabelframe': dict(
            background='green',
            padding=10
        ),
        'Rightpanel.TLabelframe': dict(
            padding=10
        ),
        'Leftpanel.TLabelframe': dict(
            foreground='black',
            padding=10
            ),
        'DebugLeftpanel.TLabelframe': dict(
            background='yellow',
            foreground='black',
            padding=10
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

    style_names = [
        'Generic.TButton',
        'Rightpanel.TLabelframe',
        'Searchbar.TFrame',
        'Leftpanel.TLabelframe',
    ]

    indices = [
        'buttons',
        'panels',
        'frames',
        'panels'
    ]

    attr_names = [
        'button',
        'right_panel',
        'searchbar',
        'left_panel',
    ]

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
        