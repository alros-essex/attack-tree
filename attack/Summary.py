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
import numpy as np
import matplotlib as mpl

from typing import List
from enum import Enum
import json

import tkinter as tk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from .Node import Node, NodeType


class Summary:
    def __init__(self, node_list:List[Node], figure:Figure, figure_canvas:FigureCanvasTkAgg):
        self.figure:Figure = figure
        self.node_list:List[Node] = node_list
        self.figure_canvas:FigureCanvasTkAgg = figure_canvas
        self.G:Digraph = nx.DiGraph()
        self.all_nodes:List[str] = []
        self.all_labels:dict = {}
        self.color_map:List[str] = []
        self.node_sizes:List[str] = []
        self.pos:dict = None
        self.pos={}

    def draw(self):
        self.figure.clf()
        plot = self.figure.add_subplot()

        (x, y, z) = self._process_nodes()

        plot.set_xlabel('Impact')
        plot.set_ylabel('Risk')

        # use the scatter function
        plot.scatter(x, y, s=z**3*100, alpha=0.5)
        plot.axis([-1, 11, -1, 11])
        self.figure_canvas.draw()

    def _process_nodes(self):
        severity = {}
        x = []
        y = []
        z = []
        for node in self.node_list:
            key = (node.get_impact(),node.get_risk())
            current = severity.get(key, 0)
            severity[key] = current + 1
        for (impact, risk) in severity:
            x.append(impact)
            y.append(risk)
            z.append(severity.get((impact, risk)))
        return (np.array(x), np.array(y), np.array(z))
