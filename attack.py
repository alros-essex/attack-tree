"""Attack"""
from __future__ import annotations

import sys
from typing import List

import tkinter as tk
from tkinter.ttk import Notebook,Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

from attack_tree import AttackTree, NonUniqueLabelException
from node import Node
from form_manager import FormManager
from file_parser import EmptyFileException, FileParser, ParseException
from summary import Summary

class Attack:
    """Class with the application's core"""

    def load_application(self, file:str):
        """
        Loads the input file and starts the application

        Parameters
        ----------
        file : str
            path to the attack tree

        Returns
        -------
        None
        """
        node_list:List[Node] = FileParser().load_nodes(file=file)
        if node_list is not None:
            self.start_gui(node_list)

    def start_gui(self, node_list:List[Node]) -> None:
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
        # create the window
        window = tk.Tk()
        # add the tabs
        tab_control = Notebook(window)
        # the first tab is the summary
        summary = self._add_summary_tab(node_list, tab_control)
        # add the one tab per root node
        for root in node_list:
            self._create_tab_for_node(root, tab_control, summary)
        # pack and display
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
        (figure, figure_canvas, _) = self._create_basic_tab(tab_control, 'Summary')
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
        (figure, figure_canvas, tab) = self._create_basic_tab(tab_control, root.get_id())
        def on_update():
            summary.draw()
        attack_tree = AttackTree(root=root, figure=figure,figure_canvas=figure_canvas)
        attack_tree.draw()
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        form_manager = FormManager(attack_tree, tab, on_update=on_update)
        figure_canvas.mpl_connect('button_press_event', form_manager.on_click)

    def _create_basic_tab(self, tab_control:Notebook, title:str):
        """
        Creates the figure and the figure canvas

        Parameters
        ----------
        tab_control : Notebook
            tab controller
        title : str
            tab title

        Returns
        -------
        Figure, FigureCanvasTkAgg, Frame
        """
        tab = Frame(tab_control)
        tab_control.add(tab, text=title)
        figure = Figure(figsize=(10, 7), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, tab)
        figure_canvas.draw()
        toolbar=NavigationToolbar2Tk(figure_canvas, tab)
        toolbar.update()
        return (figure, figure_canvas, tab)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("specify a file containing an attack tree")
    else:
        try:
            Attack().load_application(sys.argv[1])
        except NonUniqueLabelException:
            print("ERROR: the node IDs must be unique")
        except ParseException:
            print(f'ERROR: parse error reading {sys.argv[1]}')
        except EmptyFileException:
            print(f'ERROR: {sys.argv[1]} is empty')
