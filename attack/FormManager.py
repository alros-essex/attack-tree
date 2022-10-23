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

class FormManager:
    attack_tree:AttackTree
    window:Tk
    details_label:Label

    def __init__(self, attack_tree:AttackTree, window:Tk) -> None:
        self.attack_tree = attack_tree
        self.window = window

        # description
        Label(self.window, text = "node details").pack(pady = 10)
        self.details_label = Label(self.window, text = "", fg = "#bbbbbb")
        self.details_label.pack(pady = 10)
        
        # form
        Label(self.window, text="risk").pack(pady = 0)
        self.input_risk = tk.Entry(self.window)
        self.input_risk.pack(pady = 0)
        Label(self.window, text="impact").pack(pady = 0)
        self.input_impact = tk.Entry(self.window)
        self.input_impact.pack(pady = 0)

        # button
        self.save_button = Button(self.window, text ="save", command = self._store_risk)
        self.save_button.pack(pady = 0)

        # disable
        self._toggle_form(False)

    def onClick(self, event):
        node:Node = self.attack_tree.find_node(event.xdata, event.ydata)
        if node is not None:
            self.current_node = node
            self._print_info(node)
        else:
            self._toggle_form(False)

    def _toggle_form(self, active:bool):
        self.input_risk.config(state=("normal" if active else "readonly"))
        self.input_impact.config(state=("normal" if active else "readonly"))
        self.save_button.config(state=("normal" if active else "disabled"))

    def _store_risk(self):
        self.current_node.set_risk(int(self.input_risk.get()))
        self.current_node.set_impact(int(self.input_impact.get()))
        self.attack_tree.draw()
    
    def _print_info(self, node:Node):
        print(node)
        self._toggle_form(True)
        self.input_risk.delete(0,END)
        self.input_risk.insert(0,node.get_risk())
        self.input_impact.delete(0,END)
        self.input_impact.insert(0,node.get_impact())
        self.details_label.config(text = node.description)
        self._toggle_form(True if node.is_leaf() else False)