# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk


class Orchestrator:
    def __init__(self, root):       
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky='news')

        left_panel_style = ttk.Style()
        left_panel_style.configure(
            'Leftpanel.TFrame', font='helvetica 24', background='yellow', padding=10
        )

        self.left_panel= ttk.Frame(
                self.mainframe, 
                borderwidth=5, 
                relief="ridge", 
                width=400,
                height=900,
                style='Leftpanel.TFrame'
            )
        
        self.left_panel.grid(row=0, column=0, sticky=(W, N, S))


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
