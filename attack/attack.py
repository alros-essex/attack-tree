"""attack"""
from __future__ import annotations

from typing import List

import tkinter as tk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from .attack_tree import AttackTree
from .node import Node
from .form_manager import FormManager
from tkinter.ttk import Notebook,Frame
from .file_parser import FileParser
from .summary import Summary

class Attack:
    """Class with the application's core"""

    def load_application(self):
        """
        Loads the input file and starts the application

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        node_list:List[Node] = FileParser.load_nodes(file='trees/unmitigated.yml')
        self._start_gui(node_list)

    def _start_gui(self, node_list:List[Node]) -> None:
        """
        Creates the application's GUI

        Parameters
        ----------
        node_list : List[Node]
            all the nodes trees

        Returns
        -------
        None
        """
        window = tk.Tk()
        tab_control = Notebook(window)
        summary = self._add_summary_tab(node_list, tab_control)
        for root in node_list:
            self._create_tab_for_node(root, tab_control, summary)

        tab_control.pack(expand=1, fill="both")

        window.mainloop()

    def _add_summary_tab(self, node_list:List[Node], tab_control:Notebook) -> Summary:
        """
        Creates the tab dedicated to the summary

        Parameters
        ----------
        node_list : List[Node]
            all the nodes trees
        tab_control : Notebook
            tab controller

        Returns
        -------
        Summary :
            tab with the summary of the vulnerabilities
        """
        tab = Frame(tab_control)
        tab_control.add(tab, text='Summary')

        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, tab)
        figure_canvas.draw()

        toolbar=NavigationToolbar2Tk(figure_canvas, tab)
        toolbar.update()

        summary = Summary(node_list, figure=figure,figure_canvas=figure_canvas)
        summary.draw()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        return summary

    def _create_tab_for_node(self, root:Node, tab_control:Notebook, summary:Summary) -> None:
        """
        Creates the tab dedicated to a specific node

        Parameters
        ----------
        root : Node
            root node
        tab_control : Notebook
            tab controller
        summary : Summary
            tab with the summary of the vulnerabilities

        Returns
        -------
        None
        """
        tab = Frame(tab_control)
        tab_control.add(tab, text=root.id)

        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, tab)
        figure_canvas.draw()

        toolbar=NavigationToolbar2Tk(figure_canvas, tab)
        toolbar.update()

        def on_update():
            summary.draw()

        attack_tree = AttackTree(root=root, figure=figure,figure_canvas=figure_canvas)

        attack_tree.draw()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        form_manager = FormManager(attack_tree, tab, on_update=on_update)

        figure_canvas.mpl_connect('button_press_event', form_manager.onClick)

def main():
    """Start the application"""
    Attack().load_application()
