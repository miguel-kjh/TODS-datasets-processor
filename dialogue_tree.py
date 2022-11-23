import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt

from service.MongoDB import MongoDB


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
    for id_, df_group in df.groupby(by='Dialogue ID'):
        actions = [reduce_list(action) for action in df_group['Action'].values]
        intentions = [reduce_list(intent) for intent in df_group['Intention'].values]
        routes[id_] = list(zip(intentions, actions))
    return routes


def create_graph_from_routes(routes: dict) -> nx.DiGraph:
    # create a graph with all the routes, when the node are the intentions and the link are the actions
    graph = nx.DiGraph()
    for route in routes.values():
        for idx, (intent, action) in enumerate(route):
            if idx == 0:
                graph.add_node(intent)
            else:
                graph.add_edge(route[idx - 1][0], intent)
                graph.add_edge(intent, action)
    return graph


def visualize_graph_as_tree(graph: nx.DiGraph):
    import os
    os.environ["PATH"] += os.pathsep + "/usr/bin/dot"
    # create a tree from the graph
    tree = nx.bfs_tree(graph, 'INFORM')
    # visualize the tree
    pos = nx.nx_pydot.graphviz_layout(tree, prog='dot')
    nx.draw(tree, pos, with_labels=True, arrows=True)
    plt.show()



def main():
    df = get_data()
    routes = get_routes(df)
    graph = create_graph_from_routes(routes)
    visualize_graph_as_tree(graph)


if __name__ == '__main__':
    main()
