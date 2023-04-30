# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from functools import partial


class Orchestrator:
    def __init__(self, root):       
        self.filters = []
        self.filter_callbacks = {}
        self.filter_buttons = {}
        self.filter_vars = {}
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
        
        self.right_panel.grid(row=0, column=1, sticky=(E, N, S, W))

    def _initialize_left_panel(self):
        """Setup left panel in main frame."""

        #-----------------
        # LEFT PANEL STYLE
        #-----------------
        left_panel_style_name = 'Leftpanel.TFrame'
        left_panel_style = ttk.Style()
        left_panel_style.configure(
            left_panel_style_name, 
            # font='helvetica 24', 
            background='yellow', 
            foreground='black',
            padding=10
        )

        #-----------------
        # LEFT PANEL FRAME
        #-----------------
        self.left_panel= ttk.Frame(
                self.mainframe, 
                borderwidth=5, 
                relief="ridge", 
                style=left_panel_style_name
            )
        self.left_panel.grid(row=0, column=0, sticky=(E, W, N, S))

        #--------------------
        # SEARCH FILTER BLOCK
        #--------------------
        ttk.Label(self.left_panel, text="filter").grid(column=0, row=0, sticky=(N,E,S))
        
        check_buttons_frame = ttk.Frame(self.left_panel, borderwidth=5)
        check_buttons_frame.grid(column=1, row=0, sticky='news')

        cats = ['Definitions', 'Theorems', 'Proofs']
        for cat in cats:
            custom_var = StringVar(value='')
            self.filter_vars[cat] = custom_var
            custom_filter = partial(self.update_filter, cat, custom_var)
            self.filter_callbacks[cat] = custom_filter

        for colix, cat in enumerate(cats):
            ttk.Checkbutton(
                    check_buttons_frame, 
                    text=cat, 
                    variable=self.filter_vars[cat],
                    compound='text',
                    onvalue=cat,
                    command=self.filter_callbacks[cat],
                    offvalue=''
                ).grid(row=0, column=colix)
            
        #----------------
        # SEARCHBAR BLOCK
        #----------------
        ttk.Label(self.left_panel, text="search").grid(column=0, row=1, sticky='news')
        self.search_var = StringVar()

        searchbar_style_name = 'Searchbar.TFrame'
        self.searchbar_style = ttk.Style()
        self.searchbar_style.configure(
            searchbar_style_name, 
            background='orange', 
            foreground='black',
            padding=5
        )
        searchbar= ttk.Frame(
                self.left_panel, 
                borderwidth=10,
                style=searchbar_style_name,
            )
        searchbar.grid(row=1, column=1, sticky=(E, W, N, S))

        entry_style = ttk.Style()
        entry_style.configure('Searchbar.TEntry')

        # inspired from: https://tkdocs.com/tutorial/widgets.html#entry (Validation section)
        search_entry = ttk.Entry(
                searchbar, 
                textvariable=self.search_var,
                validate='key', 
                validatecommand=(root.register(self.validate_search), '%P'),
                style='Searchbar.TEntry',
                width=300
                # borderwidth=15
            )
        search_entry.grid(row=0, column=0, sticky='news', pady=20)


    def validate_search(self, search_str: str):
        return all(map(str.isalnum, search_str.split()))
    
    def update_filter(self, ref, val_, *args):
        val = val_.get()
        if val:
            assert ref == val, f"{ref=}, {val=}"
            self.filters.append(val)
        else:
            self.filters = [v for v in self.filters if v != ref]
        # print(f"{self.filters=}")

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
