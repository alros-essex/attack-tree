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
        colors = []
        for node in self.node_list:
            key = (node.get_impact(),node.get_risk())
            current = severity.get(key, 0)
            severity[key] = current + 1
        for (impact, risk) in severity:
            x.append(impact)
            y.append(risk)
            z.append(severity.get((impact, risk)))
        return (np.array(x), np.array(y), np.array(z))

    def _add_all_nodes(self):
        self._reset()
        for node in self.node_list:
            self._add_node(node)

    def _add_node(self, node:Node):
        self.all_labels[node.id] = node.id
        self.G.add_node(node.id)
        self.pos[node.id]=(node.get_impact(), node.get_risk())
        self.all_nodes.append(node)
        self.node_sizes.append(5*node.get_severity())
        self.color_map.append(self._calculate_color(node))

    def _calculate_color(self, node:Node):
        # color maps https://matplotlib.org/stable/tutorials/colors/colormaps.html
        (red,green,blue,_) = mpl.colormaps['gist_ncar'](0.43+float(node.get_severity())/100*0.42)
        return "#{red:02x}{green:02x}{blue:02x}".format(red=int(red*255), green=int(green*255), blue=int(blue*255))

    def _reset(self):
        self.pos={}
        self.G.clear()
        self.figure.clear()
        plt.clf()
        self.color_map.clear()