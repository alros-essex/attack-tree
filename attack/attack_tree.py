"""AttackTree"""
from __future__ import annotations
from cProfile import label
from tokenize import Pointfloat
from graphviz import Digraph
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib as mpl

from typing import List

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from .node import Node

class AttackTree:
    """Responsible to draw the attack tree on screen"""

    def __init__(self, root:Node, figure:Figure, figure_canvas:FigureCanvasTkAgg):
        """
        Builds the instance

        Parameters
        ----------
        root : Node
            Root node of the tree
        figure : Figure
            Tk Figure to draw the tree
        figure_canvas: FigureCanvasTkAgg
            Tk Canvas to draw the tree

        Returns
        -------
        None
        """
        self.figure:Figure = figure
        self.root:Node = root
        self.figure_canvas:FigureCanvasTkAgg = figure_canvas
        self.G:Digraph = nx.DiGraph()
        self.all_nodes:List[str] = []
        self.all_labels:dict = {}
        self.color_map:List[str] = []
        self.node_sizes:List[str] = []
        self.pos:dict = None

    def draw(self) -> None:
        """
        Draws or refreshes the tree

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._add_all_nodes()
        self.pos=graphviz_layout(self.G,prog="dot")
        self.figure.clf()
        axes = self.figure.add_subplot()

        nx.draw_networkx_edges(self.G, ax=axes, pos=self.pos)
        nx.draw_networkx_nodes(self.G,
            ax=axes,
            pos=self.pos,
            node_color=self.color_map,
            node_shape='o',#other shapes: so^>v<dph8 
            node_size=300)
        nx.draw_networkx_labels(self.G, 
            ax=axes,
            pos=self.pos,
            labels=self.all_labels,
            font_size=10,
            font_family='sans-serif')
        self.figure_canvas.draw()

    def find_node(self, x:int, y:int) -> Node | None:
        """
        Finds a node given it's position on screen

        Parameters
        ----------
        x : int
            coordinate
        y : int
            coordinate

        Returns
        -------
        Node, if found, or None
        """
        for node in self.all_nodes:
            id = node.id
            distance = pow(x-self.pos[id][0],2)+pow(y-self.pos[id][1],2)
            if distance < 70:
                return node
        return None

    def _add_all_nodes(self) -> None:
        """
        Convenience method to populate the tree

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._reset()
        self._add_node(self.root)
    
    def _reset(self) -> None:
        """
        Convenience method to clean the screen

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.G.clear()
        self.figure.clear()
        plt.clf()
        self.color_map.clear()

    def _add_node(self, node:Node, father:Node = None) -> None:
        """
        Recursively adds nodes to build the tree

        Parameters
        ----------
        node : Node
            current root
        father : Node
            optional father (None by default)

        Returns
        -------
        None
        """
        self.all_labels[node.id] = node.id
        self.G.add_node(node.id)
        self.all_nodes.append(node)
        self.node_sizes.append(500)
        self.color_map.append(self._calculate_color(node))
        if father is not None:
            self.G.add_edge(father.id, node.id)
        for child in node.children:
            self._add_node(child, node)

    def _calculate_color(self, node:Node) -> str:
        """
        Convenience method to determine the colour 

        Parameters
        ----------
        node : Node
            node to be examined

        Returns
        -------
        str representing the colour on a subset of the gist_ncar color scheme
        """
        # color maps https://matplotlib.org/stable/tutorials/colors/colormaps.html
        (red,green,blue,_) = mpl.colormaps['gist_ncar'](
            0.43+float(node.get_severity())/100*0.42)
        return "#{red:02x}{green:02x}{blue:02x}".format(
            red=int(red*255), green=int(green*255), blue=int(blue*255))
