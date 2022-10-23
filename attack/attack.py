from __future__ import annotations
from cProfile import label
import imp
from tokenize import Pointfloat
from graphviz import Digraph
from matplotlib.axes import Axes
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import yaml

from typing import List
from enum import Enum

import tkinter as tk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from .AttackTree import AttackTree
from .Node import Node, NodeType
from .FormManager import FormManager
from tkinter.ttk import Notebook,Frame
from .FileParser import FileParser
from .Summary import Summary

class Attack:

    @staticmethod
    def load_application():
        node_list:List[Node] = FileParser.load_nodes(file='trees/unmitigated.yml')
        Attack._start_gui(node_list)

    def _start_gui(node_list:List[Node]):
        window = tk.Tk()
        tab_control = Notebook(window)
        summary = Attack._add_summary_tab(node_list, tab_control)
        for root in node_list:
            Attack._create_tab_for_node(root, tab_control, summary)

        tab_control.pack(expand=1, fill="both")

        window.mainloop()

    def _add_summary_tab(node_list:List[Node], tabControl:Notebook) -> Summary:
        tab = Frame(tabControl)
        tabControl.add(tab, text='Summary')

        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, tab)
        figure_canvas.draw()

        toolbar=NavigationToolbar2Tk(figure_canvas, tab)
        toolbar.update()

        summary = Summary(node_list, figure=figure,figure_canvas=figure_canvas)
        summary.draw()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        return summary

    def _create_tab_for_node(root:Node, tabControl:Notebook, summary:Summary):
        tab = Frame(tabControl)
        tabControl.add(tab, text=root.id)

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
            
        formManager = FormManager(attack_tree, tab, on_update=on_update)

        figure_canvas.mpl_connect('button_press_event', formManager.onClick)

def main():
    Attack.load_application()


