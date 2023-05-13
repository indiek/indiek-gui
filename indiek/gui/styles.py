from tkinter import ttk
from typing import Optional, Mapping, Any

DEBUG_STYLES = {
    'buttons': {
        'IndieKDebug.TButton': {
            'background': 'blue'
        }
    }
}

class ButtonStyle(ttk.Style):
    _ik_options = dict(
        background='red',
    )
    ik_name = 'IndieK.TButton'

    def __init__(
            self, 
            style_name: Optional[str] = None, 
            options: Optional[Mapping[str, Any]] = None, 
            ):
        super().__init__()
        if style_name is None:
            style_name = self.ik_name
        if options is None:
            options = self._ik_options
        self.configure(style_name, **options)


class IndiekTheme:
    def __init__(self, debug: bool = False):
        if debug:
            btn_index = 'IndieKDebug.TButton'
            btn_config = DEBUG_STYLES['buttons'][btn_index]
            self.button = ButtonStyle(btn_index, btn_config)
        else:
            self.button = ButtonStyle()
