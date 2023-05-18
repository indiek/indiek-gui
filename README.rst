Tkinter app that acts as a GUI for IndieK software.

============
Installation
============

To install from PyPI: ``pip install indiek-gui``

To develop, use the [dev] dependency specification, e.g.:
``pip install indiek-gui[dev]``

Or from the cloned repo's top-level in editable mode:
``pip install -e .[dev]``

==========
Quickstart
==========
Call ``indiek-gui`` from your terminal to launch the GUI.

..  code-block:: bash

    indiek-gui

This GUI enables you to create definitions, theorems and proofs,
and store them on an mock Database. It offers you the possibility
to persist the mock database to your file system as a JSON file, 
and to reload it later on.

=====
Tests
=====
To run the full test suite, type the following from the top level of this repo:
``pytest``
