"""Node"""
from __future__ import annotations
from typing import List

class Node:
    """Represents a node in the attack tree"""

    def __init__(self, node_id:str, description:str, children:List[Node]=None):
        """
        Builds an instance

        Parameters
        ----------
        node_id : str
            node id
        description : str
            detailed description
        children : List[Node]
            optional list of children

        Returns
        -------
        None
        """
        self._node_id = node_id
        self._description=description
        self._children=children if not None else []
        self._risk = 0
        self._impact = 0

    def get_id(self):
        """
        Returns the node's id

        Parameters
        ----------
        None

        Returns
        -------
        str:
            node's id
        """
        return self._node_id

    def get_description(self) -> str:
        """
        Returns the node's description

        Parameters
        ----------
        None

        Returns
        -------
        str:
            node's description
        """
        return self._description

    def is_leaf(self) -> bool:
        """
        Returns True if the node is a leaf

        Parameters
        ----------
        None

        Returns
        -------
        bool:
            True if it's a leaf
        """
        return self._children is None or len(self._children)==0

    def get_risk(self) -> int:
        """
        Returns the risk of the node

        Parameters
        ----------
        None

        Returns
        -------
        int:
            Risk associated with the node
        """
        if self.is_leaf():
            return self._risk
        (max_risk, _) = self._get_children_risk_and_impact()
        return max_risk

    def get_impact(self):
        """
        Returns the impact of the node

        Parameters
        ----------
        None

        Returns
        -------
        int:
            Impact associated with the node
        """
        if self.is_leaf():
            return self._impact
        (_, max_impact) = self._get_children_risk_and_impact()
        return max_impact

    def get_severity(self):
        """
        Returns the severity of the node

        Parameters
        ----------
        None

        Returns
        -------
        int:
            Severity associated with the node
        """
        return self.get_impact() * self.get_risk()

    def get_children(self) -> List[Node]:
        """
        Returns the children of the node

        Parameters
        ----------
        None

        Returns
        -------
        List[Node]:
            node's children
        """
        return self._children


    def _get_children_risk_and_impact(self):
        """
        Returns a tuple with the maximum risk and impact among the children

        Parameters
        ----------
        None

        Returns
        -------
        (int, int):
            Risk and impact associated with the children
        """
        max_risk = 0
        max_impact = 0
        for child in self._children:
            risk = child.get_risk()
            impact = child.get_impact()
            if risk*impact > max_risk*max_impact:
                max_risk = risk
                max_impact = impact
        return (max_risk, max_impact)

    def set_risk(self, risk:int) -> None:
        """
        Sets the risk for the node

        Parameters
        ----------
        int:
            risk level between 0 and 10

        Returns
        -------
        None
        """
        self._risk = risk

    def set_impact(self, impact:int):
        """
        Sets the impact for the node

        Parameters
        ----------
        int:
            impact level between 0 and 10

        Returns
        -------
        None
        """
        self._impact = impact
