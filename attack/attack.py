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
from tkinter import ttk
from .FileParser import FileParser

def main():
    node_list:List[Node] = FileParser.load_nodes(file='trees/unmitigated.yml')
    
    window = tk.Tk()
    tabControl = ttk.Notebook(window)

    for root in node_list:
        tab = ttk.Frame(tabControl)
        tabControl.add(tab, text=root.id)

        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, tab)
        figure_canvas.draw()

        toolbar=NavigationToolbar2Tk(figure_canvas, tab)
        toolbar.update()

        attack_tree = AttackTree(root=root, figure=figure,figure_canvas=figure_canvas)

        attack_tree.draw()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        formManager = FormManager(attack_tree, tab)

        figure_canvas.mpl_connect('button_press_event', formManager.onClick)
    
    tabControl.pack(expand=1, fill="both")

    window.mainloop()
