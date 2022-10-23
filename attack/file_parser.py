"""FileParser"""
from __future__ import annotations
import yaml

from typing import List

from .Node import Node, NodeType

class FileParser:
    """Utility to parse the attack trees"""

    @staticmethod
    def load_nodes(file:str) -> List[Node]:
        """
        Loads a file with an attack tree

        Parameters
        ----------
        file : filename
            The file containing the attack tree
        """
        with open(file, "r", encoding='UTF8') as stream:
            try:
                data = yaml.safe_load(stream)
                return FileParser._parse_nodes(data['issues'])
            except yaml.YAMLError as exc:
                print(exc)
                return None

    def _parse_nodes(issues) -> List[Node]:
        """
        Parses all the nodes

        Parameters
        ----------
        file : yml object
            object loaded with the yaml framework
        """
        nodes = []
        for issue in issues:
            nodes.append(Node(
                id=issue['id'],
                description=issue['description'],
                type=NodeType[issue['type']],
                children=FileParser._parse_nodes(issue['children']) if 'children' in issue else []))
        return nodes
