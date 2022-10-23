"""FormManager"""
from tkinter import Label, HORIZONTAL, Scale, Tk
from .attack_tree import AttackTree
from .node import Node

class FormManager:
    """Class managing the user's input"""

    def __init__(self, attack_tree:AttackTree, window:Tk, on_update):
        """
        Creates the instance

        Parameters
        ----------
        attack_tree : AttackTree
            attack tree modeling with the vulneratbilies graph
        window : Tk
            Tk window
        on_update :
            function to be called on form update

        Returns
        -------
        None
        """
        self.attack_tree = attack_tree
        self.window = window
        self.on_update = on_update
        self.current_node = None

        # description
        Label(self.window, text = "node details").pack(pady = 10)
        self.details_label = Label(self.window, text = "", fg = "#bbbbbb")
        self.details_label.pack(pady = 10)

        # form
        Label(self.window, text="risk").pack(pady = 0)
        self.input_risk = Scale(self.window,
            from_=0,
            to=10,
            length=200,
            orient=HORIZONTAL,
            command=self._store_risk)
        self.input_risk.pack(pady = 0)
        Label(self.window, text="impact").pack(pady = 0)
        self.input_impact = Scale(self.window,
            from_=0,
            to=10,
            length=200,
            orient=HORIZONTAL,
            command=self._store_risk)
        self.input_impact.pack(pady = 0)

        # disable
        self._toggle_form(False)

    def on_click(self, event) -> None:
        """
        Callback reacting to clicks on the window

        Parameters
        ----------
        event :
            Tk click event

        Returns
        -------
        None
        """
        node:Node = self.attack_tree.find_node(event.xdata, event.ydata)
        if node is not None:
            self.current_node = node
            self._print_info(node)
        else:
            self._toggle_form(False)

    def _toggle_form(self, active:bool) -> None:
        """
        Activates/deactivates the form

        Parameters
        ----------
        activate : bool
            true to activate, false otherwise

        Returns
        -------
        None
        """
        self.input_risk.config(state=("normal" if active else "disabled"))
        self.input_impact.config(state=("normal" if active else "disabled"))

    def _store_risk(self, _) -> None:
        """
        Updates the node with a new risk

        Parameters
        ----------
        _ : event
            ignored

        Returns
        -------
        None
        """
        self.current_node.set_risk(int(self.input_risk.get()))
        self.current_node.set_impact(int(self.input_impact.get()))
        self.attack_tree.draw()
        self.on_update()

    def _print_info(self, node:Node) -> None:
        """
        Set up the form

        Parameters
        ----------
        node : Node
            selected node

        Returns
        -------
        None
        """
        self._toggle_form(True)
        self.input_risk.set(node.get_risk())
        self.input_impact.set(node.get_risk())
        self.details_label.config(text = node.get_description())
        self._toggle_form(node.is_leaf())
