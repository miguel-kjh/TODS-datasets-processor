import pandas as pd
import networkx as nx
import pydot
from matplotlib import pyplot as plt
from tqdm import tqdm

from service.MongoDB import MongoDB

import os

current_path = os.environ.get("PATH")
os.environ["PATH"] = current_path + ";C:\\Program Files (x86)\\Graphviz\\bin"


def get_data(
        db_name: str = 'SGD',
        filename: str = 'SGD_dataset_TINY',
        path: str = 'mongodb://localhost:27017'
) -> pd.DataFrame:
    mongodb_service = MongoDB(db_name, path)
    return mongodb_service.load(filename)


def get_routes(df: pd.DataFrame) -> dict:
    routes = {}
    reduce_list = lambda x: '_'.join(list(set(x)))
    for id_, df_group in tqdm(df.groupby(by='Dialogue ID'), desc='Creating routes'):
        actions = [f'BOT {reduce_list(action)}' for action in df_group['Action'].values]
        intentions = [f'USER {reduce_list(intent)}' for intent in df_group['Intention'].values]
        route = list(zip(intentions, actions))
        if route not in routes.values():
            routes[id_] = route
    return routes


def create_graph_from_routes(routes: dict) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_node('start')
    for id, route in tqdm(routes.items(), desc='Creating graph'):
        for idx, (intent, action) in enumerate(route):
            if idx == 0:
                graph.add_edge('start', intent)
                graph.add_edge(intent, action)
            else:
                graph.add_edge(route[idx - 1][1], intent)
                graph.add_edge(intent, action)
    return graph


def visualize_graph(graph: nx.DiGraph):
    # view the graph with the labels asn node start as initial node
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, nodelist=['start'], node_color='r', node_size=500, alpha=0.8)
    nx.draw_networkx_nodes(graph, pos, nodelist=[node for node in graph.nodes if node != 'start'], node_color='b',
                           node_size=500, alpha=0.8)
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family='sans-serif')
    labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.axis('off')
    plt.show()


def visualize_graph_as_tree(graph: nx.DiGraph):
    # view graph as a tree
    #tree = nx.bfs_tree(graph, 'start')
    # pos = graphviz_layout(tree, prog='dot')
    """nx.draw_networkx_nodes(graph, pos, nodelist=['start'], node_color='r', node_size=500, alpha=0.8)
    nx.draw_networkx_nodes(graph, pos, nodelist=[node for node in graph.nodes if node != 'start'], node_color='b',
                           node_size=500, alpha=0.8)
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family='sans-serif')
    labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.axis('off')
    plt.show()"""
    # save the graph as a png with pydot
    nx.drawing.nx_pydot.write_dot(graph, 'tree.dot')
    (graph,) = pydot.graph_from_dot_file('tree.dot')
    graph.write_png('tree.png')


def main():
    df = get_data()
    routes = get_routes(df)
    print(f'Number of routes: {len(routes)}')
    graph = create_graph_from_routes(routes)
    visualize_graph_as_tree(graph)


if __name__ == '__main__':
    main()
