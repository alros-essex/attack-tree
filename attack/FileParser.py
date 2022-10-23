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

class FileParser:

    @staticmethod
    def load_nodes(file:str) -> List[Node]:
        with open(file, "r") as stream:
            try:
                data = yaml.safe_load(stream)
                return FileParser._parse_nodes(data['issues'])
            except yaml.YAMLError as exc:
                print(exc)
                return None

    def _parse_nodes(issues) -> List[Node]:
        nodes = []
        for issue in issues:
            nodes.append(Node(
                id=issue['id'], 
                description=issue['description'], 
                type=NodeType[issue['type']],
                children=FileParser._parse_nodes(issue['children']) if 'children' in issue else []))
        return nodes