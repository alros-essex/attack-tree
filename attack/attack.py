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

def main():
    window = tk.Tk()
    figure = Figure(figsize=(6, 4), dpi=100)
    figure_canvas = FigureCanvasTkAgg(figure, window)
    figure_canvas.draw()

    toolbar=NavigationToolbar2Tk(figure_canvas, window)
    toolbar.update()

    attack_tree = AttackTree('trees/unmitigated.yml', figure)

    attack_tree.draw()

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    formManager = FormManager(attack_tree, window)

    figure_canvas.mpl_connect('button_press_event', formManager.onClick)
    window.mainloop()
