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
        self._initialize_right_panel()

    def _initialize_right_panel(self):
        right_panel_style = ttk.Style()
        right_panel_style.configure(
            'Rightpanel.TLabelframe', 
            background='green', 
            padding=10
        )
        self.right_panel = ttk.PanedWindow(self.mainframe, orient=VERTICAL)
        self.mainframe.add(self.right_panel, weight=2)

        self.view_panel= ttk.Labelframe(
                self.right_panel, 
                relief="ridge", 
                height=400,
                width=800,
                style='Rightpanel.TLabelframe',
                text='View'
            )
        
        self.edit_panel= ttk.Labelframe(
                self.right_panel, 
                relief="ridge", 
                heigh=500,
                style='Rightpanel.TLabelframe',
                text='Edit'
            )
        
        self.right_panel.add(self.view_panel, weight=1)
        self.right_panel.add(self.edit_panel, weight=1)

    def _initialize_filter_block(self):
        (ttk
         .Label(self.left_search_pane, text="filter")
         .grid(column=0, row=0, sticky=(N, W, E, S)))
        
        self.check_buttons_frame = ttk.Frame(self.left_search_pane, borderwidth=5)
        self.check_buttons_frame.grid(column=1, row=0, sticky='news')

        # setup callbacks for filter's CheckButtons
        cats = ['Definitions', 'Theorems', 'Proofs']
        for cat in cats:
            custom_var = StringVar(value='')
            self.filter_vars[cat] = custom_var
            custom_filter = partial(self.update_filter, cat, custom_var)
            self.filter_callbacks[cat] = custom_filter
        # create the check buttons
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

    def _initialize_searchbar(self):
        ttk.Label(self.left_search_pane, text="search").grid(column=0, row=1, sticky='ens')
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
                self.left_search_pane, 
                style=searchbar_style_name,
            )
        searchbar.grid(row=1, column=1, sticky=(E, W, N, S))

        # inspired from: https://tkdocs.com/tutorial/widgets.html#entry (Validation section)
        search_entry = ttk.Entry(
                searchbar, 
                textvariable=self.search_var,
                validate='key', 
                validatecommand=(root.register(self.validate_search), '%P'),
                font=('Century 9'),
                # width=65
            )
        search_entry.grid(row=0, column=0, sticky='news', pady=2)
        search_entry.bind("<Return>", self.collect_search)
        search_entry.bind("<FocusOut>", self.collect_search)
        search_entry.bind("<KeyRelease>", self.collect_search)

    def _initialize_search_results(self):
        self.results_window = ttk.PanedWindow(self.left_panel, orient=VERTICAL)
        self.left_panel.add(self.results_window, weight=3)

        self.result_pane = ttk.Labelframe(self.results_window, text='Results')
        self.result_pane.grid()
        self.results_window.add(self.result_pane)

        self.search_results_str = StringVar(value='Initial State')
        self.search_results = ttk.Label(
                self.result_pane, 
                textvariable=self.search_results_str,
                wraplength=500,  # pixels
            )
        self.search_results.grid(row=0, column=0, sticky='news', padx=15, pady=15)

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

        #-------------------------
        # LEFT PANEL WINDOWED PANE
        #-------------------------
        self.left_panel = ttk.PanedWindow(self.mainframe, orient=VERTICAL)
        self.mainframe.add(self.left_panel, weight=1)

        self.left_search_pane = ttk.Labelframe(
                self.left_panel, 
                relief="ridge", 
                style=left_panel_style_name,
                text='Search'
            )
        self.left_search_pane.grid(column=0, row=0, sticky='news')
        self.left_search_pane.grid_rowconfigure(0, weight=1)
        self.left_search_pane.grid_columnconfigure(0, weight=1)
        self.left_search_pane.grid_rowconfigure(1, weight=1)
        self.left_search_pane.grid_columnconfigure(1, weight=1)

        self.left_panel.add(self.left_search_pane, weight=1)
        self.left_panel.bind('<<filter-update>>', self.collect_search)
        
        self._initialize_filter_block()           
        self._initialize_searchbar()
        self._initialize_search_results()

    def validate_search(self, search_str: str):
        valid = all(map(str.isalnum, search_str.split()))
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
