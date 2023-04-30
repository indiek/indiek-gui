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

        self.mainframe = ttk.Panedwindow(root, orient=HORIZONTAL)  # ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky='news')
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=2)
        self.mainframe.rowconfigure(0, weight=1)

        self._initialize_left_panel()

        right_panel_style = ttk.Style()
        right_panel_style.configure(
            'Rightpanel.TLabelframe', 
            # font='helvetica 24', 
            background='green', 
            padding=10
        )
        self.right_panel = ttk.PanedWindow(self.mainframe, orient=VERTICAL)
        self.mainframe.add(self.right_panel, weight=2)

        self.view_panel= ttk.Labelframe(
                self.right_panel, 
                # borderwidth=5, 
                relief="ridge", 
                height=400,
                width=800,
                style='Rightpanel.TLabelframe',
                text='View'
            )
        self.edit_panel= ttk.Labelframe(
                self.right_panel, 
                # borderwidth=5, 
                relief="ridge", 
                heigh=500,
                style='Rightpanel.TLabelframe',
                text='Edit'
            )
        self.right_panel.add(self.view_panel, weight=1)
        self.right_panel.add(self.edit_panel, weight=1)
        # self.right_panel.grid(row=0, column=1, sticky=(E, N, S, W))

    def _initialize_filter_block(self):
        ttk.Label(self.left_panel, text="filter").grid(column=0, row=0, sticky=(N, W, E, S))
        
        self.check_buttons_frame = ttk.Frame(self.left_panel, borderwidth=5)
        self.check_buttons_frame.grid(column=1, row=0, sticky='news')

        cats = ['Definitions', 'Theorems', 'Proofs']
        for cat in cats:
            custom_var = StringVar(value='')
            self.filter_vars[cat] = custom_var
            custom_filter = partial(self.update_filter, cat, custom_var)
            self.filter_callbacks[cat] = custom_filter

        for colix, cat in enumerate(cats):
            ttk.Checkbutton(
                    self.check_buttons_frame, 
                    text=cat, 
                    variable=self.filter_vars[cat],
                    compound='text',
                    onvalue=cat,
                    command=self.filter_callbacks[cat],
                    offvalue=''
                ).grid(row=0, column=colix, sticky=(N, E, S, W))
        # check_buttons_frame.event_add('<<filter-update>>', )

    def _initialize_searchbar(self):
        ttk.Label(self.left_panel, text="search").grid(column=0, row=1, sticky='ens')
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
                style=searchbar_style_name,
            )
        searchbar.grid(row=1, column=1, sticky=(E, W, N, S))

        # entry_style = ttk.Style()
        # entry_style.configure('Searchbar.TEntry')

        # inspired from: https://tkdocs.com/tutorial/widgets.html#entry (Validation section)
        search_entry = ttk.Entry(
                searchbar, 
                textvariable=self.search_var,
                validate='key', 
                validatecommand=(root.register(self.validate_search), '%P'),
                font=('Century 9'),
                # style='Searchbar.TEntry',
                width=65
                # borderwidth=15
            )
        search_entry.grid(row=0, column=0, sticky='news', pady=2)
        search_entry.bind("<Return>", self.collect_search)

    def _initialize_search_results(self):
        self.search_results_str = StringVar(value='Initial State')
        self.search_results = ttk.Label(
                self.left_panel, 
                textvariable=self.search_results_str,
                wraplength=320,  # pixels
            )
        self.search_results.grid(row=2, column=0, columnspan=2, sticky='news', padx=15, pady=15)

        # self.search_results.bind('<<filter-update>>', lambda e: self.collect_search())

    def _initialize_left_panel(self):
        """Setup left panel in main frame."""
        #-----------------
        # LEFT PANEL STYLE
        #-----------------
        left_panel_style_name = 'Leftpanel.TLabelframe'
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
        self.left_panel = ttk.Labelframe(
                self.mainframe, 
                # borderwidth=5, 
                relief="ridge", 
                style=left_panel_style_name,
                text='Search'
            )
        # self.left_panel.event_add(
        #         '<<search-update>>', 
        #         '<<filter-update>>',
        #         '<<searchbar-update>>'
        #     )
        self.left_panel.bind('<<searchbar-update>>', self.collect_search)
        self.left_panel.bind('<<filter-update>>', self.collect_search)
        # self.left_panel.grid(row=0, column=0, sticky=(E, W, N, S))
        self.mainframe.add(self.left_panel, weight=1)

        self._initialize_filter_block()           
        self._initialize_searchbar()
        self._initialize_search_results()

    def validate_search(self, search_str: str):
        valid = all(map(str.isalnum, search_str.split()))
        if valid:
            self.left_panel.event_generate('<<searchbar-update>>')
        return valid
    
    def update_filter(self, ref, val_, *args):
        val = val_.get()
        if val:
            assert ref == val, f"{ref=}, {val=}"
            self.filters.append(val)
        else:
            self.filters = [v for v in self.filters if v != ref]
        self.left_panel.event_generate('<<filter-update>>')
    
    def collect_search(self, *args):
        vars = {}
        vars['filters'] = self.filters
        vars['search'] = self.search_var.get()
        self.search_results_str.set(str(vars))

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
