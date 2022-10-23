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

    # 1x1 = 1      00ff00
    # 6            40ff00
    # 12           7fff00
    # 5x5 = 25     ffff00
    # 50           ff7f00
    # 75           ff4000
    # 10x10 = 100  ff0000
    severity_colors:List[str] = []

    def __init__(self, file:str, figure:Figure, figure_canvas:FigureCanvasTkAgg):
        self.figure = figure
        self.node_list = self._load_nodes(file)
        self.figure_canvas = figure_canvas
        self.severity_colors = self._build_color_scale()

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

    def _build_color_scale(self) -> List[str]:
        severity_colors:List[str] = ['#7f7fff']
        red:int = 0
        green:int = 255
        for i in range(1, 101):
            if i > 25:
                red = 255
                green = green - int(255/75)
            else:
                green = 255
                red = red + int(255/25)
            severity_colors.append("#{red:02x}{green:02x}00".format(red=red, green=green))
        return severity_colors

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
        severity = node.get_risk() * node.get_impact()
        return  self.severity_colors[severity]

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