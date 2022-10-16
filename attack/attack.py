from __future__ import annotations
from tokenize import Pointfloat
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

from typing import List
from enum import Enum

class NodeType(Enum):
    STATE = 0
    THREAT = 1
    MITIGATION = 2

node_colors = {
    NodeType.STATE: '#b8b8b8',
    NodeType.THREAT: '#ff4040',
    NodeType.MITIGATION: '#1f78b4'
}

class Node:
    id:str
    children:List[Node]
    type:str

    def __init__(self, id:str, children:List[Node]=[], type:NodeType=NodeType.STATE) -> None:
        self.id=id
        self.children=children
        self.type=type

def main():
    node_list = [
        Node("AAAAAA", 
            children=[
                Node("B", 
                    children=[
                        Node("C")
                    ],
                    type=NodeType.THREAT), 
                Node("D", 
                    children=[
                        Node("E", type=NodeType.MITIGATION),
                        Node("F")
                    ],
                    type=NodeType.THREAT),
                Node("G")])
    ]

    G = nx.DiGraph()

    all_nodes = []
    color_map = []
    node_sizes = []
    def add_node(G, node:Node, father:Node = None):
        G.add_node(node.id)
        all_nodes.append(node)
        node_sizes.append(500)
        color_map.append(node_colors[node.type])
        if father is not None:
            G.add_edge(father.id, node.id)
        for child in node.children:
            add_node(G, child, node)

    for node in node_list:
        add_node(G, node)

    plt.axis('off')

    #shape: so^>v<dph8
    pos=graphviz_layout(G,prog="dot")
    nx.draw_networkx_edges(G, pos=pos)
    nx.draw_networkx_nodes(G, node_color=color_map, node_shape='o', node_size=300, pos=pos)
    nx.draw_networkx_labels(G, pos=pos, font_size=10, font_family='sans-serif')

    def onClick(event):
        for node in all_nodes:
            id = node.id
            distance = pow(event.xdata-pos[id][0],2)+pow(event.ydata-pos[id][1],2)
            if distance < 70:
                popupmsg(id)

    fig = plt.gcf()
    fig.canvas.mpl_connect('button_press_event', onClick)

    plt.show()
    
    # pos=nx.get_node_attributes(G,'pos')

    # fig, ax = plt.subplots()
    # ax.set_title('click on points')
    # ax.set_axis_off()
    
    # cid = fig.canvas.mpl_connect('pick_event', onclick)

    # line, = ax.plot(G, 'o', picker=True, pickradius=5)  # 5 points tolerance

    # plt.show()

    # nx.draw(G, pos)

