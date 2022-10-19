from __future__ import annotations
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
    risk:int = 0
    impact:int = 0

    def __init__(self, id:str, description:str, type:NodeType, children:List[Node]=[]) -> None:
        self.id=id
        self.description=description
        self.children=children
        self.type=type

    def is_leaf(self):
        return self.children is None or len(self.children)==0
    
    def get_risk(self):
        if self.is_leaf():
            return self.risk
        (max_risk, _) = self._get_children_risk_and_impact()
        return max_risk

    def get_impact(self):
        if self.is_leaf():
            return self.impact
        (_, max_impact) = self._get_children_risk_and_impact()
        return max_impact

    def _get_children_risk_and_impact(self):
        max_risk = 0
        max_impact = 0
        for child in self.children:
            risk = child.get_risk()
            impact = child.get_impact()
            if risk*impact > max_risk*max_impact:
                max_risk = risk
                max_impact = impact
        return (max_risk, max_impact)

    def set_risk(self, risk:int):
        self.risk = risk
    
    def set_impact(self, impact:int):
        self.impact = impact

    def __str__(self) -> str:
        return "Node id={id} risk={risk} impact={impact}".format(
            id=self.id,
            risk=self.risk,
            impact=self.impact)

class AttackTree:
    G:Digraph = nx.DiGraph()
    all_nodes:List[str] = []
    all_labels:List[str] = []
    color_map:List[str] = []
    node_sizes:List[str] = []
    pos:dict = None

    figure:Figure = None

    def __init__(self, file:str, figure:Figure):
        self.figure = figure
        node_list = self._load_nodes(file)
        for node in node_list:
            self._add_node(node)
        self.pos=graphviz_layout(self.G,prog="dot")

    def draw(self):
        self.figure.clear()
        axes = self.figure.add_subplot()
        nx.draw_networkx_edges(self.G, ax=axes, pos=self.pos)
        #all shapes: so^>v<dph8
        nx.draw_networkx_nodes(self.G, ax=axes, pos=self.pos, node_color=self.color_map, node_shape='o', node_size=300)
        nx.draw_networkx_labels(self.G, ax=axes, pos=self.pos, font_size=10, font_family='sans-serif')

    def find_node(self, x:int, y:int) -> Node | None:
        for node in self.all_nodes:
            id = node.id
            distance = pow(x-self.pos[id][0],2)+pow(y-self.pos[id][1],2)
            if distance < 70:
                return node
        return None

    def _add_node(self, node:Node, father:Node = None):
        self.all_labels.append(node.id)
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
    
    def _print_info(self, node:Node):
        print(node)
        self.input_risk.delete(0,END)
        self.input_risk.insert(0,node.get_risk())
        self.input_impact.delete(0,END)
        self.input_impact.insert(0,node.get_impact())
        self.details_label.config(text = node.description)
        self._toggle_form(True if node.is_leaf() else False)

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
    
    popupManager = PopupManager(attack_tree, window)

    figure_canvas.mpl_connect('button_press_event', popupManager.onClick)
    window.mainloop()
