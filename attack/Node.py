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

class NodeType(Enum):
    state = 0
    threat = 1
    mitigation = 2


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

    def get_severity(self):
        return self.get_impact() * self.get_risk()

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
