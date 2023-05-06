# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from functools import partial
from indiek.core.items import Item as CoreItem
from indiek.core.search import list_all_items
from indiek.gui.items import core_to_gui_item, GUIItem
from . import __version__

# initial_item below is just to simulate that DB is not empty
initial_item = CoreItem(
    name="dummy item", 
    content="dummy content"
    )
initial_item.save()

WRAP_1 = 380
ENTRY_DEFAULT_LENGTH = 54


class Orchestrator:
    def __init__(self, root, max_results: int = 100):
        self.max_results = max_results

        self.filters = []
        self.filter_callbacks = {}
        self.filter_buttons = {}
        self.filter_vars = {}

        self.view_callbacks = {}
        _default_str = 'No Item Selected'
        self.view_var = GUIItem(
            name_var=StringVar(value=_default_str),
            content_var=StringVar(value=_default_str),
            name=_default_str, 
            content=_default_str
            )

        self.text = {}

        self.search_var = StringVar()

        self.search_results_list = []
        self.ikid_to_result_slot = {}
        for result_ix, core_item in enumerate(list_all_items()):
            gui_item = core_to_gui_item(
                core_item,
                name_var=StringVar(value=core_item.name),
                content_var=StringVar(value=core_item.content),
                )
            self.search_results_list.append(gui_item)
            self.ikid_to_result_slot[gui_item._ikid] = result_ix

        self.root = root
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

    def initialize_item_view(self, frame, text_vars: GUIItem):
        local_frame = ttk.Frame(frame)
        local_frame.grid(row=0, column=0, sticky='news')
        local_frame.grid_rowconfigure(0, weight=1)
        local_frame.grid_rowconfigure(1, weight=1)
        local_frame.grid_columnconfigure(0, weight=1)
        local_frame.grid_columnconfigure(1, weight=1)
        
        item_name_descr = ttk.Label(local_frame, text='name')
        item_name_descr.grid(row=0, column=0, sticky='e')
        
        item_name = ttk.Label(local_frame, textvariable=text_vars.name_var)
        item_name.grid(row=0, column=1, sticky='w')

        item_content_descr = ttk.Label(local_frame, text='content')
        item_content_descr.grid(row=1, column=0, sticky='e')
        
        item_content = ttk.Label(local_frame, textvariable=text_vars.content_var)
        item_content.grid(row=1, column=1, sticky='w')


    def _initialize_right_panel(self):
        right_panel_style = ttk.Style()
        right_panel_style.configure(
            'Rightpanel.TLabelframe',
            background='green',
            padding=10,
            width=1000,
            height=650
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
        self.view_nb = ttk.Notebook(self.view_panel, width=800)
        self.view_nb.grid(row=0, column=0, sticky='news')

        # View tab
        view = ttk.Frame(self.view_nb)
        view.grid(row=0, column=0, sticky='news')
        view.grid_rowconfigure(0, weight=1)
        view.grid_columnconfigure(0, weight=1)

        item_frame = ttk.Frame(view, borderwidth=1, relief='groove')
        item_frame.grid(row=0, column=0, sticky='news')
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=0)
        item_frame.grid_rowconfigure(0, weight=1)

        self.initialize_item_view(
            item_frame,
            text_vars=self.view_var, 
            )
        # TODO: add scrollbar?

        btn_frame = ttk.Frame(view)
        btn_frame.grid(row=0, column=1, sticky='news')
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_rowconfigure(0, weight=0)
        btn_frame.grid_rowconfigure(1, weight=0)
        btn_frame.grid_rowconfigure(2, weight=0)

        self.new_item_button = ttk.Button(
            btn_frame,
            text='New Item',
            # command=self.switch_to_edit,
            state='disabled'
        )
        self.new_item_button.grid(row=0, column=0, sticky=(N,))

        self.edit_button = ttk.Button(
            btn_frame,
            text='Edit',
            command=self.switch_to_edit,
            state='disabled'
        )
        self.edit_button.grid(row=1, column=0, sticky=(N,))

        # Edit tab
        edit = ttk.Frame(self.view_nb)
        edit.grid(row=0, column=0, sticky='news')
        edit.grid_rowconfigure(0, weight=1)
        edit.grid_columnconfigure(0, weight=1)
        edit.grid_columnconfigure(1, weight=0)

        save_button = ttk.Button(
            edit, text='Save', command=self.switch_to_view)
        save_button.grid(row=0, column=1)

        self.initialize_item_edit(
            edit, 
            text_vars=self.view_var
        )

        self.view_nb.add(view, text='View')
        self.view_nb.add(edit, text='Edit', state='hidden')

    def initialize_item_edit(self, frame, text_vars: GUIItem):
        local_frame = ttk.Frame(frame)
        local_frame.grid(row=0, column=0, sticky='news')
        local_frame.grid_rowconfigure(0, weight=1)
        local_frame.grid_rowconfigure(1, weight=1)
        local_frame.grid_columnconfigure(0, weight=1)
        local_frame.grid_columnconfigure(1, weight=1)
        
        item_name_descr = ttk.Label(local_frame, text='name')
        item_name_descr.grid(row=0, column=0, sticky='e')

        self.text['name'] = Text(local_frame)
        self.text['name'].insert('1.0', text_vars.name)
        self.text['name'].grid(row=0, column=1, sticky='w')

        item_content_descr = ttk.Label(local_frame, text='content')
        item_content_descr.grid(row=1, column=0, sticky='e')
        
        self.text['content'] = Text(local_frame)
        self.text['content'].insert('1.0', text_vars.content)
        self.text['content'].grid(row=1, column=1, sticky='w')

    def switch_to_edit(self):
        edit_id = 1
        self.view_nb.tab(edit_id, state='normal')
        self.view_nb.select(edit_id)

    def switch_to_view(self):
        """When focus is on Edit tab; save and switch to View tab."""

        edit_id = 1
        view_id = 0

        # content attr
        content_str = self.text['content'].get('1.0', 'end')
        self.view_var.update_content(content_str)

        # name attr
        name_str = self.text['name'].get('1.0', 'end')
        self.view_var.update_name(name_str)

        # save to DB
        self.view_var.save()

        # and refresh search results
        result_ix = self.ikid_to_result_slot[self.view_var._ikid]
        self.search_results_str[result_ix].set(self.view_var.name)

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
        for result_ix, gui_item in enumerate(self.search_results_list):
            search_results = ttk.Label(
                self.results_canvas,
                textvariable=gui_item.name_var,
                wraplength=WRAP_1,  # pixels
            )
            self.view_callbacks[result_ix] = partial(
                self.populate_view_pane, gui_item, result_ix)

            search_results.bind('<Button-1>', self.view_callbacks[result_ix])

            _ = self.results_canvas.create_window(
                0,
                height * result_ix,
                anchor='nw',
                window=search_results,
                height=height,
                tags=('palette')
            )

    def populate_view_pane(self, gui_item: GUIItem, *args):
        """Populate View pane with GUIItem.

        This callback gets triggered when item from search results
        gets clicked upon.

        Args:
            gui_item (GUIItem): Item to use to populate data fields.
        """
        self.view_var = gui_item

        self.edit_button['state'] = 'normal'

        # update Text widgets for future edits
        for attr_name in ['name', 'content']:
            self.text[attr_name].delete('1.0', 'end')
            self.text[attr_name].insert('1.0', getattr(self.view_var, attr_name))

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


def main():
    """Launch main Tkinter event loop."""
    root = Tk()
    root.title(f"indiek-gui v{__version__}")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # for some reason width and height below have no effect
    root.configure(width=2000, height=1000)

    Orchestrator(root)

    root.bind('q', lambda e: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    main()
