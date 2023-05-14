from tkinter import ttk
from typing import Optional, Mapping, Any


_ENTRY_DEFAULT_LENGTH = 54
DEFAULT_FONT = 'Century 9'
_STYLES = {
    'entries': {
        'Generic.TEntry': dict(
            width=_ENTRY_DEFAULT_LENGTH,
            padding=1,
        ),
        'DebugGeneric.TEntry': dict(
            width=_ENTRY_DEFAULT_LENGTH,
            padding=1,
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
        'Toggle.TCheckbutton': dict(),
        'DebugToggle.TCheckbutton': dict(),
        'DebugGeneric.TButton': dict(),
        'Generic.TButton': dict()
    },
    'panels': {
        'DebugRightpanel.TLabelframe': dict(  # https://stackoverflow.com/a/70601534
            background='green',
            relief='ridge',
            padding=10,
        ),
        'Rightpanel.TLabelframe': dict(
            padding=10,
            relief='ridge',
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
        'ItemSnippet.TLabelframe': dict(),
        'DebugItemSnippet.TLabelframe': dict(),
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
        'buttons',
        'panels',
        'frames',
        'panels',
        'labels',
        'frames',
        'entries',
        'frames',
    )

    style_names = (
        'Toggle.TCheckbutton',
        'Generic.TButton',
        'Rightpanel.TLabelframe',
        'Searchbar.TFrame',
        'Leftpanel.TLabelframe',
        'Generic.TLabel',
        'ItemView.TFrame',
        'Generic.TEntry',
        'ItemSnippet.TLabelframe',
    )

    attr_names = (
        'item_button',
        'button',
        'right_panel',
        'searchbar',
        'left_panel',
        'generic_label',
        'item_view',
        'generic_entry',
        'item_snippet',
    )

    def __init__(self, debug: bool = False):
        if debug:
            names = list(map(lambda x: 'Debug' + x, self.style_names))        
        else:
            names = self.style_names

        iterator = zip(self.attr_names, self.indices, names)
        for attr_name, index, style_name in iterator:
            self.initialize_attr(attr_name, index, style_name)

        self.apply_maps()

    def initialize_attr(self, attr_name, index, style_name):
        config = _STYLES[index][style_name]
        attr_val = IndieKStyle(style_name, config)
        setattr(self, attr_name, attr_val)
        
    def apply_maps(self):
        pass
        # self.item_button.map(
        #     self.item_button.ik_name,
        #     relief=[('active', 'sunken')]
        # )
        # self.item_snippet.map(
        #     self.item_snippet.ik_name, 
        #     relief=[('focus', 'sunken'), ('!selected', 'raised')]
        #     )