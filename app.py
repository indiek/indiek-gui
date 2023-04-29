# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk


class Orchestrator:
    def __init__(self, root):       
        self.filters = []
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
        left_panel_style_name = 'Leftpanel.TFrame'
        left_panel_style = ttk.Style()
        left_panel_style.configure(
            left_panel_style_name, 
            font='helvetica 24', 
            background='yellow', 
            foreground='black',
            padding=10
        )
        self.left_panel= ttk.Frame(
                self.mainframe, 
                borderwidth=5, 
                relief="ridge", 
                style=left_panel_style_name
            )

        self.left_panel.grid(row=0, column=0, sticky=(W, N, S))

        ttk.Label(self.left_panel, text="filter").grid(column=0, row=0, sticky=(N,E,))
        ttk.Label(self.left_panel, text="search").grid(column=0, row=1, sticky=(E,))

        check_buttons_frame = ttk.Frame(self.left_panel, borderwidth=5)
        check_buttons_frame.grid(column=1, row=0, sticky='news')

        cats = ['Definitions', 'Theorems', 'Proofs']
        for colix, cat in enumerate(cats):
            custom_var = StringVar()
            def custom_filter(*args): 
                self.update_filter(cat, custom_var)
            ttk.Checkbutton(
                check_buttons_frame, 
                text=cat, 
                command=custom_filter,
                variable=custom_var,
                compound='bottom',
                onvalue=cat,
                offvalue=''
                ).grid(row=0, column=colix)
            
    def update_filter(self, ref, val_):
        val = val_.get()
        if val:
            assert ref == val, f"{ref=}, {val=}"
            self.filters.append(val)
        else:
            self.filters = [v for v in self.filters if v != ref]
        print(f"{self.filters=}")

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
