"""Summary"""
from __future__ import annotations
from typing import List

from graphviz import Digraph
import networkx as nx
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from .node import Node

class Summary:
    """Manages the summary tab"""

    def __init__(self, node_list:List[Node], figure:Figure, figure_canvas:FigureCanvasTkAgg):
        """
        Creates a new instance

        Parameters
        ----------
        node_list : List[Node]
            all the root nodes
        figure : Figure
            Tk figure to plot the chart
        figure_canvas : FigureCanvasTkAgg
            Tk canvas to pliot the chart

        Returns
        -------
        None
        """
        self.figure:Figure = figure
        self.node_list:List[Node] = node_list
        self.figure_canvas:FigureCanvasTkAgg = figure_canvas

    def draw(self) -> None:
        """
        Draws the tab

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.figure.clf()
        plot = self.figure.add_subplot()

        (pos_x, pos_y, sizes) = self._process_nodes()

        plot.set_xlabel('Impact')
        plot.set_ylabel('Risk')

        # use the scatter function
        plot.scatter(pos_x, pos_y, s=sizes**3*100, alpha=0.5)
        plot.axis([-1, 11, -1, 11])
        self.figure_canvas.draw()

    def _process_nodes(self):
        """
        Calculates the data for the chart

        Parameters
        ----------
        None

        Returns
        -------
        Tuple with the x, y and z arrays
        """
        severity = {}
        pos_x = []
        pos_y = []
        sizes = []
        for node in self.node_list:
            key = (node.get_impact(),node.get_risk())
            current = severity.get(key, 0)
            severity[key] = current + 1
        for (impact, risk) in severity:
            pos_x.append(impact)
            pos_y.append(risk)
            sizes.append(severity.get((impact, risk)))
        return (np.array(pos_x), np.array(pos_y), np.array(sizes))
