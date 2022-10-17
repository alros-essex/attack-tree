from __future__ import annotations
from tokenize import Pointfloat
from graphviz import Digraph
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

class NodeType(Enum):
    state = 0
    threat = 1
    mitigation = 2


node_colors = {
    NodeType.state: '#b8b8b8',
    NodeType.threat: '#ff4040',
    NodeType.mitigation: '#1f78b4'
}

class Node:
    id:str
    description:str
    children:List[Node]
    type:str

    def __init__(self, id:str, description:str, type:NodeType, children:List[Node]=[]) -> None:
        self.id=id
        self.description=description
        self.children=children
        self.type=type

class AttackTree:
    G:Digraph = nx.DiGraph()
    all_nodes:List[str] = []
    color_map:List[str] = []
    node_sizes:List[str] = []
    pos:dict = None

    def __init__(self, file:str):
        node_list = self._load_nodes(file)
        for node in node_list:
            self._add_node(node)
        self.pos=graphviz_layout(self.G,prog="dot")

    def draw(self, axes):
        nx.draw_networkx_edges(self.G, ax=axes, pos=self.pos)
        #all shapes: so^>v<dph8
        nx.draw_networkx_nodes(self.G, ax=axes, pos=self.pos, node_color=self.color_map, node_shape='o', node_size=300)
        nx.draw_networkx_labels(self.G, ax=axes, pos=self.pos, font_size=10, font_family='sans-serif')

    def find_node(self, x:int, y:int):
        for node in self.all_nodes:
            id = node.id
            distance = pow(x-self.pos[id][0],2)+pow(y-self.pos[id][1],2)
            if distance < 70:
                return node

    def _add_node(self, node:Node, father:Node = None):
        self.G.add_node(node.id)
        self.all_nodes.append(node)
        self.node_sizes.append(500)
        self.color_map.append(node_colors[node.type])
        if father is not None:
            self.G.add_edge(father.id, node.id)
        for child in node.children:
            self._add_node(child, node)

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

class PopupManager:
    attack_tree:AttackTree
    def __init__(self, attack_tree:AttackTree) -> None:
        self.attack_tree = attack_tree

    def onClick(self, event):
        node = self.attack_tree.find_node(event.xdata, event.ydata)
        print(node.id) if node is not None else None
        if node is not None:
            popup = tk.Tk()
            label = Label(popup, text = "node details")
            label.pack(pady = 10)
            label = Label(popup, text = node.id)
            label.pack(pady = 10)

            def doStuff():
                print("stuff")

            btn = Button(popup,
                text ="Click to open a new window",
                command = doStuff)
            btn.pack(pady = 10)

def main():
    window = tk.Tk()
    figure = Figure(figsize=(6, 4), dpi=100)
    figure_canvas = FigureCanvasTkAgg(figure, window)
    figure_canvas.draw()

    toolbar=NavigationToolbar2Tk(figure_canvas, window)
    toolbar.update()

    attack_tree = AttackTree('trees/unmitigated.yml')

    attack_tree.draw(figure.add_subplot())

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    popupManager = PopupManager(attack_tree)

    figure_canvas.mpl_connect('button_press_event', popupManager.onClick)
    window.mainloop()
