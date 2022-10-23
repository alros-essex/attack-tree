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
import matplotlib as mpl

from typing import List
from enum import Enum

import tkinter as tk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from .Node import Node, NodeType


node_colors = {
    NodeType.state: '#b8b8b8',
    NodeType.threat: '#ff4040',
    NodeType.mitigation: '#1f78b4'
}

class AttackTree:
    G:Digraph = nx.DiGraph()
    all_nodes:List[str] = []
    all_labels:dict = {}
    color_map:List[str] = []
    node_sizes:List[str] = []
    pos:dict = None

    figure:Figure = None
    figure_canvas:FigureCanvasTkAgg = None

    def __init__(self, file:str, figure:Figure, figure_canvas:FigureCanvasTkAgg):
        self.figure = figure
        self.node_list = self._load_nodes(file)
        self.figure_canvas = figure_canvas

    def draw(self):
        self._add_all_nodes()
        self.pos=graphviz_layout(self.G,prog="dot")
        self.figure.clf()
        axes = self.figure.add_subplot()
        nx.draw_networkx_edges(self.G, ax=axes, pos=self.pos)
        nx.draw_networkx_nodes(self.G, ax=axes, pos=self.pos, node_color=self.color_map, node_shape='o', node_size=300) #other shapes: so^>v<dph8
        nx.draw_networkx_labels(self.G, ax=axes, pos=self.pos, labels=self.all_labels, font_size=10, font_family='sans-serif')
        self.figure_canvas.draw()

    def find_node(self, x:int, y:int) -> Node | None:
        for node in self.all_nodes:
            id = node.id
            distance = pow(x-self.pos[id][0],2)+pow(y-self.pos[id][1],2)
            if distance < 70:
                return node
        return None

    def _add_all_nodes(self):
        self._reset()
        for node in self.node_list:
            self._add_node(node)
    
    def _reset(self):
        self.G.clear()
        self.figure.clear()
        plt.clf()
        self.color_map.clear()

    def _add_node(self, node:Node, father:Node = None):
        self.all_labels[node.id] = node.id
        self.G.add_node(node.id)
        self.all_nodes.append(node)
        self.node_sizes.append(500)
        self.color_map.append(self._calculate_color(node))
        if father is not None:
            self.G.add_edge(father.id, node.id)
        for child in node.children:
            self._add_node(child, node)

    def _calculate_color(self, node:Node):
        # color maps https://matplotlib.org/stable/tutorials/colors/colormaps.html
        (red,green,blue,_) = mpl.colormaps['gist_ncar'](0.43+float(node.get_severity())/100*0.42)
        return "#{red:02x}{green:02x}{blue:02x}".format(red=int(red*255), green=int(green*255), blue=int(blue*255))

    def _load_nodes(self, file:str) -> List[Node]:
        def parse_nodes(issues) -> List[Node]:
            nodes = []
            for issue in issues:
                nodes.append(Node(
                    id=issue['id'], 
                    description=issue['description'], 
                    type=NodeType[issue['type']],
                    children=parse_nodes(issue['children']) if 'children' in issue else []))
            return nodes

        with open(file, "r") as stream:
            try:
                data = yaml.safe_load(stream)
                return parse_nodes(data['issues'])
            except yaml.YAMLError as exc:
                print(exc)
                return None