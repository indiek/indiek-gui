# -*- coding: utf-8 -*-
"""
Mind refresher:

What variable is shown in the Text widgets from the Edit notebook tab?
    -> self.view_var
"""
# TODO: set minimum width on labels or their containing columns
from typing import Optional, Mapping, Tuple, Iterator
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from functools import partial
from indiek.mockdb.persistence import persist, load_from_file
from indiek.core.search import list_all_items, filter_str
from indiek.gui.items import core_to_gui_item, Item as GUIItem, Definition, Theorem, Proof
from indiek.gui.styles import IndiekTheme, DEFAULT_FONT
from indiek.core.items import (Definition as CoreDefinition, 
                               Theorem as CoreTheorem, 
                               Proof as CoreProof)
from . import __version__


PairOfInt = Tuple[int, int]


DEFAULT_PERSISTENCE_DIR = '/home/adrian_admin/prog/indiek/indiek-gui/.data/'
"""Path where DB gets persisted and loaded from."""


ITEM_TYPES = [Definition, Theorem, Proof]
"""List of item types."""


FILTER_NAMES = ['Definitions', 'Theorems', 'Proofs']
"""Strings used in filter radio buttons for each Item type."""


NAME_TO_ITEM_TYPE = {
    'Definitions': CoreDefinition, 
    'Theorems': CoreTheorem, 
    'Proofs': CoreProof
}
assert set(NAME_TO_ITEM_TYPE.keys()) == set(FILTER_NAMES)


CANVAS_OPTIONS = {
    'search_results': dict(
        background='blue',
    ),
}

WRAP_1 = 380

ONE_LINE_HEIGHT = 1  # in units of lines


def grid_init(
        frame, 
        *,
        subcols: Iterator[PairOfInt] = ((0, 1),), 
        subrows: Iterator[PairOfInt] = ((0, 1),),
        init_row_col: PairOfInt = (0,0),
        sticky: str = 'news',
        ) -> None:
    frame.grid(row=init_row_col[0], column=init_row_col[1], sticky=sticky)
    for colix, colw in subcols:
        frame.grid_columnconfigure(colix, weight=colw)
    for rowix, roww in subrows:
        frame.grid_rowconfigure(rowix, weight=roww)


class Orchestrator:
    item_result_height = 40
    """Height of Label in results to be displayed."""

    view_id = 0
    """ID of view tab in Notebook."""

    edit_id = 1
    """ID of edit tab in Notebook."""

    filters = []
    filter_callbacks = {}
    """Callbacks for filter."""

    filter_vars = {}

    view_callbacks = {}
    """Callbacks for View pane."""

    text = {}
    """Text widgets for Editing arranged as Dict."""
    
    _default_str = 'No Item Selected'
    
    search_results_list = []
    """List of GUIItems to be displayed as search results."""

    ikid_to_result_slot = {}
    
    def __init__(
            self, 
            root, 
            max_results: int = 100, 
            indiek_theme: type = IndiekTheme,
            debug: bool = False
            ):
        self.debug = debug
        self.theme = indiek_theme(debug=self.debug)
        self.search_var = StringVar()

        self.view_var = self._initialize_view_var()

        self.max_results = max_results

        self.root = root

        self.create_main_menu()

        self.mainframe = ttk.Panedwindow(self.root, orient=HORIZONTAL)
        self.mainframe.grid(column=0, row=0, sticky='news')
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=2)
        self.mainframe.rowconfigure(0, weight=1)

        self._initialize_right_panel()
        self._initialize_left_panel()

        self.mainframe.add(self.left_panel, weight=1)
        self.mainframe.add(self.right_panel, weight=2)

    def initialize_item_view(self, frame, gui_item: GUIItem):
        local_frame = ttk.Frame(frame)
        grid_init(
            local_frame,
            subcols=[(0, 0), (1, 1)],
            subrows=[(0, 0), (1, 0), (2, 1)]
            )
        
        self.item_type = ttk.Label(
            local_frame, 
            text=gui_item.__class__.__name__,
            style=self.theme.generic_label.ik_name
            )
        if self.debug:
            self.item_type['text'] += ' ikid:' + str(gui_item._ikid)
        self.item_type.grid(row=0, column=0, sticky='news')
        gen_label = partial(ttk.Label, local_frame, style=self.theme.generic_label.ik_name)
        item_name_descr = gen_label(text='name')
        item_name_descr.grid(row=1, column=0, sticky='new')

        item_name = gen_label(textvariable=gui_item.name_var)
        item_name.grid(row=1, column=1, sticky='new')
        self.item_view_name_label = item_name

        item_content_descr = gen_label(text='content')
        item_content_descr.grid(row=2, column=0, sticky='new')
        
        item_content = gen_label(textvariable=gui_item.content_var)
        item_content.grid(row=2, column=1, sticky='new')
        self.item_view_content_label = item_content

    def _initialize_right_panel(self):
        self.right_panel = ttk.PanedWindow(self.mainframe, orient=VERTICAL)

        self.view_panel = ttk.Labelframe(
            self.right_panel,
            style=self.theme.right_panel.ik_name,
            text='View/Edit'
        )
        grid_init(self.view_panel)

        self._initialize_view_notebook()

        self.project_panel = ttk.Labelframe(
            self.right_panel,
            style=self.theme.right_panel.ik_name,
            text='Project'
        )

        self.right_panel.add(self.view_panel, weight=1)
        self.right_panel.add(self.project_panel, weight=1)

    def _initialize_view_notebook(self):
        self.view_nb = ttk.Notebook(self.view_panel)
        self.view_nb.grid(row=0, column=0, sticky='news')

        # View tab
        view = ttk.Frame(self.view_nb)
        grid_init(view)

        item_frame = ttk.Frame(view, style=self.theme.item_view.ik_name)
        grid_init(item_frame, subcols=[(0, 1), (1, 0)])

        self.initialize_item_view(
            item_frame,
            gui_item=self.view_var, 
            )
        # TODO: add scrollbar?

        btn_frame = ttk.Frame(view)
        grid_init(
            btn_frame,
            init_row_col=(0, 1),
            subrows=[(i, 0) for i in range(5)]
        )

        # BUTTONS WHILE ON VIEW MODE
        self.new_item_buttons = {}
        for row_ix, item_type in enumerate(ITEM_TYPES):
            # btn_frame.grid_rowconfigure(row_ix, weight=0)
            self.new_item_buttons[item_type] = ttk.Button(
                btn_frame,
                text=f'New {item_type.__name__}',
                command=partial(self.switch_to_edit_new, item_type),
                state='normal'
            )
            self.new_item_buttons[item_type].grid(row=row_ix, column=0, sticky=(N, W, E))

        self.edit_button = ttk.Button(
            btn_frame,
            text='Edit',
            command=self.switch_to_edit,
            state='disabled',
            style=self.theme.button.ik_name
        )
        self.edit_button.grid(row=row_ix + 1, column=0, sticky=(N, W, E))
        self.delete_button = ttk.Button(
            btn_frame,
            text='Delete',
            command=self.delete,
            state='disabled'
        )
        self.delete_button.grid(row=row_ix + 2, column=0, sticky=(N, W, E))

        # Edit tab
        edit = ttk.Frame(self.view_nb)
        grid_init(edit, subcols=[(0, 1), (1, 0)])

        item_edit_frame = ttk.Frame(edit, style=self.theme.item_view.ik_name)
        grid_init(item_edit_frame)

        self.initialize_item_edit(item_edit_frame)

        # Buttons while on EDIT mode
        edit_btn_frame = ttk.Frame(edit)
        grid_init(
            edit_btn_frame, 
            init_row_col=(0, 1), 
            subrows=[(i, 0) for i in range(2)]
            )

        save_button = ttk.Button(
            edit_btn_frame, text='Save', command=self.switch_to_view)
        save_button.grid(row=0, column=1, sticky=(N, W, E))
        
        self.cancel_button = ttk.Button(
            edit_btn_frame,
            text='Cancel',
            command=self.cancel,
        )
        self.cancel_button.grid(row=1, column=1, sticky=(N, W, E))

        self.view_nb.add(view, text='View')
        self.view_nb.add(edit, text='Edit', state='hidden')

    def cancel(self):
        self.populate_edit_pane()
        self.switch_to_view(save=False, update_view_var=False)

    def initialize_item_edit(self, frame):
        """Create frames and labels for single item edition."""
        local_frame = ttk.Frame(frame)
        grid_init(
            local_frame,
            subrows=[(0, 0), (1, 0), (2, 1)],
            subcols=[(0, 0), (1, 1)]
        )
        
        self.item_type_edit = ttk.Label(
            local_frame, 
            text='',
            style=self.theme.generic_label.ik_name
            )
        self.item_type_edit.grid(row=0, column=0, sticky='news')

        item_name_descr = ttk.Label(local_frame, text='name')
        item_name_descr.grid(row=1, column=0, sticky='wen')

        self.text['name'] = Text(
            local_frame, 
            height=ONE_LINE_HEIGHT, 
            font=DEFAULT_FONT
            )
        self.text['name'].grid(row=1, column=1, sticky='w')

        item_content_descr = ttk.Label(local_frame, text='content')
        item_content_descr.grid(row=2, column=0, sticky='wen')
        
        self.text['content'] = Text(local_frame, font=DEFAULT_FONT)
        self.text['content'].grid(row=2, column=1, sticky='nwe')

    def switch_to_edit(self):
        """Switch focus from item view to item edition."""
        self.populate_edit_pane()
        self.view_nb.tab(self.edit_id, state='normal')
        self.view_nb.select(self.edit_id)
    
    def switch_to_edit_new(self, item_cls: GUIItem):
        """Switch to edit tab for new item creation."""
        new_item = item_cls(name_var=StringVar(), content_var=StringVar())
        self.populate_view_pane(new_item)
        self.populate_edit_pane()
        self.view_nb.tab(self.edit_id, state='normal')
        self.view_nb.select(self.edit_id)

    def delete(self):
        self.view_var.delete()
        self.delete_button['state'] = 'disabled'
        self.collect_search()
        self.populate_edit_pane()

    def switch_to_view(self, save: bool = True, update_view_var: bool = True):
        """When focus is on Edit tab; save and switch to View tab."""

        if update_view_var:
            # content attr
            content_str = self.text['content'].get('1.0', 'end')
            self.view_var.update_str_var('content_var', content_str, set_core_attr=True)

            # name attr
            name_str = self.text['name'].get('1.0', 'end')
            self.view_var.update_str_var('name_var', name_str, set_core_attr=True)

        if save:
            # save to DB
            ikid = self.view_var.save()

            if self.debug:
                itype = self.view_var.__class__.__name__
                self.item_type['text'] = itype + ' ikid:' + str(ikid)

            # refresh search results
            self.collect_search()

        # hide editor
        self.view_nb.tab(self.edit_id, state='hidden')

        # focus back on view
        self.delete_button['state'] = 'normal'

        self.view_nb.select(self.view_id)

    def _initialize_filter_block(self):
        (ttk
         .Label(self.left_search_pane, text="filter")
         .grid(column=0, row=0, sticky=(N, W, E, S)))

        self.check_buttons_frame = ttk.Frame(
            self.left_search_pane, borderwidth=5)
        self.check_buttons_frame.grid(column=1, row=0, sticky='w')

        # setup callbacks for filter's CheckButtons
        cats = FILTER_NAMES
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

        searchbar = ttk.Frame(
            self.left_search_pane,
            style=self.theme.searchbar.ik_name,
        )
        grid_init(searchbar, init_row_col=(1, 1))

        # inspired from: https://tkdocs.com/tutorial/widgets.html#entry (Validation section)
        search_entry = ttk.Entry(
            searchbar,
            textvariable=self.search_var,
            validate='key',
            validatecommand=(self.root.register(self.validate_search), '%P'),
            style=self.theme.generic_entry.ik_name,
            font=DEFAULT_FONT
        )
        search_entry.grid(row=0, column=0, sticky='news')  #, pady=2)
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
        grid_init(self.results_frame, subcols=[(0, 0), (1, 1)])
        self.left_panel.add(self.results_frame, weight=3)

        # ------------------
        # SCROLLABLE CANVAS
        # ------------------
        scroll_height = self.max_results * self.item_result_height
        scroll_width = 300

        scr = ttk.Scrollbar(self.results_frame, orient=VERTICAL)
        self.results_canvas = Canvas(
            self.results_frame,
            scrollregion=(0, 0, scroll_width, scroll_height),
            yscrollcommand=scr.set,
            background=CANVAS_OPTIONS['search_results']['background']
        )
        scr['command'] = self.results_canvas.yview
        self.results_canvas.grid(column=1, row=0, sticky=(N, W, E, S))
        scr.grid(column=0, row=0, sticky=(N, S))

        # -------------------
        # DUMMY RESULT PANES
        # -------------------
        self.populate_search_results_canvas(self.search_results_list)

    def populate_search_results_canvas(self, results_list):
        # clear canvas
        result_tag = 'result_item'
        self.results_canvas.delete(result_tag)
        # self.result_buttons = []
        self.result_bools = []
        for result_ix, gui_item in enumerate(results_list):
            mini_item_frame = ttk.Labelframe(
                self.results_canvas,
                text=gui_item.__class__.__name__,
                style=self.theme.item_snippet.ik_name
            )
            
            grid_init(mini_item_frame)

            self.view_callbacks[result_ix] = partial(
                self.populate_view_pane, gui_item, source_ix=result_ix)
            
            result_bool = BooleanVar(value=gui_item == self.view_var)
            search_result = ttk.Checkbutton(
                mini_item_frame,
                textvariable=gui_item.name_var,
                command=self.view_callbacks[result_ix],
                style=self.theme.item_button.ik_name,
                variable=result_bool
            )
            self.result_bools.append(result_bool)
            # self.result_buttons.append(search_result)
            search_result.grid(row=0, column=0, sticky='news')

            mini_item_frame.bind('<Button-1>', self.view_callbacks[result_ix])

            _ = self.results_canvas.create_window(
                0,
                self.item_result_height * result_ix,
                anchor='nw',
                window=mini_item_frame,
                height=self.item_result_height,
                tags=(result_tag,)
            )

    def populate_view_pane(self, gui_item: GUIItem, *args, source_ix = None):
        """Populate View & Edit tabs with GUIItem data.

        This callback gets triggered when:
         - item from search results gets clicked upon, or,
         - user clicks on create new <Item>

        Args:
            gui_item (GUIItem): Item to use to populate data fields.
        """
        self.view_var = gui_item
        self.item_type['text'] = self.view_var.__class__.__name__
        if self.debug:
            self.item_type['text'] += ' ikid:' + str(self.view_var._ikid)

        # TODO: think about improving below logic
        self.item_view_name_label['textvariable'] = self.view_var.name_var
        self.item_view_content_label['textvariable'] = self.view_var.content_var

        # enable delete button if gui_item exists in DB
        if gui_item.exists_in_db:
            self.delete_button['state'] = 'normal'

        # enable editing
        self.edit_button['state'] = 'normal'
        self.cancel_button['state'] = 'normal'  # acts as "reload" button

        # deselect all other result buttons
        if source_ix is not None:
            for ix, bool_ in enumerate(self.result_bools):
                if ix != source_ix:
                    bool_.set(False)

    def populate_edit_pane(self, gui_item: Optional[GUIItem] = None):
        """Populate text widget with self.view_var or provided GUIItem."""
        if gui_item is None:
            gui_item = self.view_var
        
        # display which Item type is being edited
        self.item_type_edit['text'] = gui_item.__class__.__name__
        if self.debug:
            self.item_type_edit['text'] += ' ikid:' + str(gui_item._ikid)

        # populate Text widgets for edition
        for attr_name in gui_item.displayable:
            self.text[attr_name].delete('1.0', 'end')
            to_insert = getattr(gui_item, attr_name)
            if to_insert:
                self.text[attr_name].insert('1.0', to_insert)

    def _initialize_left_panel(self):
        """Setup left panel in main frame."""
        # -------------------------
        # LEFT PANEL WINDOWED PANE
        # -------------------------
        self.left_panel = ttk.PanedWindow(self.mainframe, orient=VERTICAL)

        self.left_search_pane = ttk.Labelframe(
            self.left_panel,
            relief="ridge",
            style=self.theme.left_panel.ik_name,
            text='Search'
        )
        grid_init(
            self.left_search_pane,
            subrows=[(0, 0), (1, 1)],
            subcols=[(0, 0), (1, 1)]
        )

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
        """Collect search parameters and triggers search.

        This callback gets called when:
        - a <<filter-update>> event happens
        - a change happens in search bar entry
        - user clicks "Save" on edit tab
        - user loads persisted DB

        This method calls refresh_results method to update
        results list.
        """
        vars = {}
        vars['filters'] = self.filters
        vars['search'] = self.search_var.get()

        self.refresh_results(vars)

    def clear_all_search(self):
        self.filters = []

        # deselect all radio buttons
        for var in self.filter_vars.values():
            var.set('')

        self.search_var.set('')

    def refresh_results(self, search_params: Optional[Mapping] = None):
        """Trigger backend search using search parameters.

        This method also updates results on GUI.

        Args:
            search_params (Optional[Mapping], optional): Search parameters. Defaults to None.

        Raises:
            NotImplementedError: If search_params is not None.
        """
        self.search_results_list = []
        # TODO: setup logging instead of print() below

        if search_params is not None:
            item_type_filter = [NAME_TO_ITEM_TYPE[f] for f in search_params['filters']]
            search_str = search_params['search']
            if search_str:
                item_buckets = filter_str(search_str, item_type_filter)
            else:
                item_buckets = list_all_items(item_type_filter)
        else:
            item_buckets = list_all_items()

        # TODO: keep item types separate below
        item_list = []
        for ll in item_buckets.values():
            item_list += ll
        for result_ix, core_item in enumerate(item_list):
            gui_item = core_to_gui_item(
                core_item,
                name_var=StringVar(value=core_item.name),
                content_var=StringVar(value=core_item.content),
                )
            self.search_results_list.append(gui_item)
            self.ikid_to_result_slot[gui_item._ikid] = result_ix
        self.populate_search_results_canvas(self.search_results_list)

    def _initialize_view_var(self):
        return GUIItem(
                name_var=StringVar(value=self._default_str),
                content_var=StringVar(value=self._default_str),
                name=self._default_str, 
                content=self._default_str
                )

    def persist_box(self):
        filename = filedialog.asksaveasfilename(initialdir=DEFAULT_PERSISTENCE_DIR)
        persist(filename)

    def load_box(self):
        filename = filedialog.askopenfilename(initialdir=DEFAULT_PERSISTENCE_DIR)
        load_from_file(filename)
        self.clear_all_search()
        self.collect_search()
        neutral_item = self._initialize_view_var()
        self.populate_view_pane(neutral_item)

    def create_main_menu(self):
        win = self.root
        menubar = Menu(win)
        menu_file = Menu(menubar)
        menu_file.add_command(label='Persist Session', command=self.persist_box)
        menu_file.add_command(label='Load Session', command=self.load_box)
        menubar.add_cascade(menu=menu_file, label='File')
        win['menu'] = menubar
        return win


def main(debug: bool = False):
    """Launch main Tkinter event loop."""
    root = Tk()
    root.option_add('*tearOff', FALSE)
    root.title(f"indiek-gui v{__version__}")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    Orchestrator(root, debug=debug)

    root.mainloop()


if __name__ == '__main__':
    main(True)
