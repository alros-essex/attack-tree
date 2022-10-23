"""FileParser"""
from __future__ import annotations
from typing import List
import yaml
from .node import Node

class FileParser:
    """Utility to parse the attack trees"""

    def load_nodes(self, file:str) -> List[Node]:
        """
        Loads a file with an attack tree

        Parameters
        ----------
        file : str
            The file containing the attack tree

        Returns
        -------
        List[Node] :
            The loaded nodes
        """
        with open(file, "r", encoding='UTF8') as stream:
            try:
                data = yaml.safe_load(stream)
                return self._parse_nodes(data['issues'])
            except yaml.YAMLError as exc:
                print(exc)
                return None

    def _parse_nodes(self, issues) -> List[Node]:
        """
        Parses all the nodes

        Parameters
        ----------
        file : yml object
            object loaded with the yaml framework

        Returns
        -------
        List[Node] :
            The parsed nodes
        """
        nodes = []
        for issue in issues:
            children = self._parse_nodes(issue['children']) if 'children' in issue else []
            nodes.append(Node(
                id=issue['id'],
                description=issue['description'],
                children=children))
        return nodes
