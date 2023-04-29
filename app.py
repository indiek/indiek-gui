# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk


class Orchestrator:
    def __init__(self, root):       
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky='news')
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=2)
        self.mainframe.rowconfigure(0, weight=1)

        self._initialize_left_panel()

        right_panel_style = ttk.Style()
        right_panel_style.configure(
            'Rightpanel.TFrame', 
            font='helvetica 24', 
            background='green', 
            padding=10
        )

        self.right_panel= ttk.Frame(
                self.mainframe, 
                borderwidth=5, 
                relief="ridge", 
                width=800,
                height=900,
                style='Rightpanel.TFrame'
            )
        
        self.right_panel.grid(row=0, column=1, sticky=(E, N, S))

    def _initialize_left_panel(self):
        self.left_panel_style_name = 'Leftpanel.TFrame'
        self.left_panel_style = ttk.Style()
        self.left_panel_style.configure(
            self.left_panel_style_name, 
            font='helvetica 24', 
            background='yellow', 
            foreground='black',
            padding=10
        )
        self.left_panel= ttk.Frame(
                self.mainframe, 
                borderwidth=5, 
                relief="ridge", 
                style=self.left_panel_style_name
            )

        self.left_panel.grid(row=0, column=0, sticky=(W, N, S))
        self.left_panel_widgets = {}
        ttk.Label(self.left_panel, text="filter").grid(column=0, row=0, sticky=(N,E,))
        # ttk.Radiobutton()
        ttk.Label(self.left_panel, text="search").grid(column=0, row=1, sticky=(E,))

        # for child in self.left_panel.winfo_children(): 
        #     child['style'] = self.left_panel_style_name

if __name__ == '__main__':
    # import sys

    root = Tk()
    root.title("IndieK v0.0.1")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.configure(width=1600, height=1000)

    Orchestrator(root)

    root.bind('q', lambda e: root.destroy())
    root.mainloop()
