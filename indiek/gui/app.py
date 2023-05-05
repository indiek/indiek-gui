# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from functools import partial
import random


WRAP_1 = 380
ENTRY_DEFAULT_LENGTH = 54


class Orchestrator:
    def __init__(self, root, max_results: int = 100):
        self.root = root
        self.max_results = max_results
        self.filters = []
        self.filter_callbacks = {}
        self.filter_buttons = {}
        self.filter_vars = {}
        self.view_callbacks = {}
        self.view_var = [StringVar(value='default view'), None]
        self.search_var = StringVar()
        self.search_results_str = [
            StringVar(value=f'{i}') for i in range(self.max_results)]

        self.mainframe = ttk.Panedwindow(
            self.root, orient=HORIZONTAL)  # ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky='news')
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=2)
        self.mainframe.rowconfigure(0, weight=1)

        self._initialize_right_panel()
        self._initialize_left_panel()

        self.mainframe.add(self.left_panel, weight=1)
        self.mainframe.add(self.right_panel, weight=2)

    def _initialize_right_panel(self):
        right_panel_style = ttk.Style()
        right_panel_style.configure(
            'Rightpanel.TLabelframe',
            background='green',
            padding=10,
        )
        self.right_panel = ttk.PanedWindow(self.mainframe, orient=VERTICAL)

        self.view_panel = ttk.Labelframe(
            self.right_panel,
            relief="ridge",
            style='Rightpanel.TLabelframe',
            text='View/Edit'
        )
        self.view_panel.grid(row=0, column=0, sticky='news')
        self.view_panel.grid_columnconfigure(0, weight=1)
        self.view_panel.grid_rowconfigure(0, weight=1)

        self._populate_view_notebook()

        self.project_panel = ttk.Labelframe(
            self.right_panel,
            relief="ridge",
            style='Rightpanel.TLabelframe',
            text='Project'
        )

        self.right_panel.add(self.view_panel, weight=1)
        self.right_panel.add(self.project_panel, weight=1)

    def _populate_view_notebook(self):
        self.view_nb = ttk.Notebook(self.view_panel)
        self.view_nb.grid(row=0, column=0, sticky='news')

        # View tab
        view = ttk.Frame(self.view_nb)
        view.grid(row=0, column=0, sticky='news')
        view.grid_rowconfigure(0, weight=1)
        view.grid_columnconfigure(0, weight=1)
        view.grid_columnconfigure(1, weight=0)

        view_label = ttk.Label(view, textvariable=self.view_var[0])
        view_label.grid(row=0, column=0, sticky='news')
        # TODO: add scrollbar?

        self.edit_button = ttk.Button(
            view,
            text='Edit',
            command=self.switch_to_edit,
            state='disabled'
        )
        self.edit_button.grid(row=0, column=1)

        # Edit tab
        edit = ttk.Frame(self.view_nb)
        edit.grid(row=0, column=0, sticky='news')
        edit.grid_rowconfigure(0, weight=1)
        edit.grid_columnconfigure(0, weight=1)
        edit.grid_columnconfigure(1, weight=0)

        save_button = ttk.Button(
            edit, text='Save', command=self.switch_to_view)
        save_button.grid(row=0, column=1)

        self.text = Text(edit, width=40, height=10)
        self.text.insert('1.0', self.view_var[0].get())
        self.text.grid(row=0, column=0, sticky='news')

        self.view_nb.add(view, text='View')
        self.view_nb.add(edit, text='Edit', state='hidden')

    def switch_to_edit(self):
        edit_id = 1
        self.view_nb.tab(edit_id, state='normal')
        self.view_nb.select(edit_id)

    def switch_to_view(self):
        """When focus is on Edit tab; save and switch to View tab."""
        edit_id = 1
        view_id = 0

        # save text
        self.view_var[0].set(self.text.get('1.0', 'end'))
        # and propagate to mock DB
        self.search_results_str[self.view_var[1]].set(self.view_var[0].get())

        # hide editor
        self.view_nb.tab(edit_id, state='hidden')

        # focus back on view
        self.view_nb.select(view_id)

    def _initialize_filter_block(self):
        (ttk
         .Label(self.left_search_pane, text="filter")
         .grid(column=0, row=0, sticky=(N, W, E, S)))

        self.check_buttons_frame = ttk.Frame(
            self.left_search_pane, borderwidth=5)
        self.check_buttons_frame.grid(column=1, row=0, sticky='w')

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
        ttk.Label(self.left_search_pane, text="search").grid(
            column=0, row=1, sticky='ens')

        searchbar_style_name = 'Searchbar.TFrame'
        self.searchbar_style = ttk.Style()
        self.searchbar_style.configure(
            searchbar_style_name,
            background='orange',
            foreground='black',
            padding=5
        )
        searchbar = ttk.Frame(
            self.left_search_pane,
            style=searchbar_style_name,
        )
        searchbar.grid(row=1, column=1, sticky=(E, W, N, S))
        searchbar.grid_columnconfigure(0, weight=1)
        searchbar.grid_rowconfigure(0, weight=1)

        # inspired from: https://tkdocs.com/tutorial/widgets.html#entry (Validation section)
        search_entry = ttk.Entry(
            searchbar,
            textvariable=self.search_var,
            validate='key',
            validatecommand=(self.root.register(self.validate_search), '%P'),
            font=('Century 9'),
            width=ENTRY_DEFAULT_LENGTH
        )
        search_entry.grid(row=0, column=0, sticky='news', pady=2)
        search_entry.bind("<Return>", self.collect_search)
        search_entry.bind("<FocusOut>", self.collect_search)
        search_entry.bind("<KeyRelease>", self.collect_search)

    def _initialize_search_results(self):
        # --------------
        # OVERALL FRAME
        # --------------
        self.results_frame = ttk.Labelframe(
            self.left_panel,
            text='Results',
        )
        self.results_frame.grid(row=0, column=0)
        self.results_frame.grid_columnconfigure(0, weight=0)
        self.results_frame.grid_columnconfigure(1, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.left_panel.add(self.results_frame, weight=3)

        # ------------------
        # SCROLLABLE CANVAS
        # ------------------
        height = 40
        scroll_height = self.max_results * height
        scroll_width = 300

        scr = ttk.Scrollbar(self.results_frame, orient=VERTICAL)
        self.results_canvas = Canvas(
            self.results_frame,
            scrollregion=(0, 0, scroll_width, scroll_height),
            yscrollcommand=scr.set,
            background='blue'
        )
        scr['command'] = self.results_canvas.yview
        self.results_canvas.grid(column=1, row=0, sticky=(N, W, E, S))
        scr.grid(column=0, row=0, sticky=(N, S))

        # -------------------
        # DUMMY RESULT PANES
        # -------------------
        for result_ix in range(self.max_results):
            result_style = ttk.Style()

            random_number = random.randint(0, 16777215)
            hex_number = str(hex(random_number))
            hex_number = '#' + hex_number[2:]

            # print(hex_color, type(hex_color))
            result_style.configure(
                f'Result{result_ix}.TLabel',
                background=hex_number,
                foreground='white',
                padding=4,
                # height=10
            )

            search_results = ttk.Label(
                self.results_canvas,
                textvariable=self.search_results_str[result_ix],
                wraplength=WRAP_1,  # pixels
                style=f'Result{result_ix}.TLabel'
            )
            self.view_callbacks[result_ix] = partial(
                self.populate_view_pane, result_ix)
            # wasclicked = lambda e: self.populate_view_pane(result_ix)
            search_results.bind('<Button-1>', self.view_callbacks[result_ix])

            _ = self.results_canvas.create_window(
                0,
                height * result_ix,
                anchor='nw',
                window=search_results,
                height=height,
                tags=('palette')
            )

    def populate_view_pane(self, result_id, *args):
        pop_str = self.search_results_str[result_id].get()
        self.view_var[0].set(pop_str)
        self.view_var[1] = result_id
        self.edit_button['state'] = 'normal'

        self.text.delete('1.0', 'end')
        self.text.insert('1.0', self.view_var[0].get())

    def _initialize_left_panel(self):
        """Setup left panel in main frame."""
        # -----------------
        # LEFT PANEL STYLE
        # -----------------
        left_panel_style_name = 'Leftpanel.TLabelframe'
        left_panel_style = ttk.Style()
        left_panel_style.configure(
            left_panel_style_name,
            background='yellow',
            foreground='black',
            padding=10
        )

        # -------------------------
        # LEFT PANEL WINDOWED PANE
        # -------------------------
        self.left_panel = ttk.PanedWindow(self.mainframe, orient=VERTICAL)

        self.left_search_pane = ttk.Labelframe(
            self.left_panel,
            relief="ridge",
            style=left_panel_style_name,
            text='Search'
        )
        self.left_search_pane.grid(column=0, row=0, sticky='news')
        self.left_search_pane.grid_rowconfigure(0, weight=0)
        self.left_search_pane.grid_columnconfigure(0, weight=0)
        self.left_search_pane.grid_rowconfigure(1, weight=1)
        self.left_search_pane.grid_columnconfigure(1, weight=1)

        self.left_panel.add(self.left_search_pane, weight=0)
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
        for ix, string_var in enumerate(self.search_results_str):
            string_var.set(str(ix) + str(vars))


def main():
    root = Tk()
    root.title("IndieK v0.0.1")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.configure(width=1600, height=1000)

    Orchestrator(root)

    root.bind('q', lambda e: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    main()
