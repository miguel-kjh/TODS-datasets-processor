from typing import List
import networkx as nx
from networkx import DiGraph

class DialogueGraph:

    def __init__(self) -> None:
        self.dialogue_graph = DiGraph()
    
    def add_node(self, intentions: str, service: List[str]) -> None:
        self.dialogue_graph.add_node(intentions, service=service)

    def add_edge(self, node_id_1: str, node_id_2: str, actions: List[str], slots: List[str]) -> None:
        action = f"{'-'.join(actions)}({','.join(slots)})"
        self.dialogue_graph.add_edge(node_id_1, node_id_2, action=action)

    def graph_2_dict(self) -> dict:
        return nx.to_dict_of_dicts(self.dialogue_graph)

    def dict_2_graph(self, graph_dict: dict) -> None:
        self.dialogue_graph = nx.from_dict_of_dicts(graph_dict)

    def get_graph(self) -> DiGraph:
        return self.dialogue_graph
