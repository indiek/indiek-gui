from tkinter import ttk


class ButtonStyle(ttk.Style):
    _ik_options = dict(
        background='red',
    )
    ik_name = 'IndieK.TButton'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(self.ik_name, **self._ik_options)


class IndiekTheme:
    def __init__(self):
        self.button = ButtonStyle()
