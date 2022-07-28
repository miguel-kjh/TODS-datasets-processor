from typing import Dict, Any

import pandas as pd
from tqdm import tqdm
from models.DialogueGraph import DialogueGraph
from service.MongoDB import MongoDB
from utils.ProjectConstants import SGD_DATASET_RES, SGD_DATASET_RES_SYN
from view.Logger import Logger


def create_dialogue_graph(pd_df: pd.DataFrame) -> dict[Any, dict]:
    graphs_by_dialogue = {}
    for id, pd_df in tqdm(pd_df.groupby('Dialogue Id'),
                          desc="DialogueGraphCreationService: Creating Dialogue Graph id"):

        graph = DialogueGraph()
        for record in pd_df.to_dict('records'):
            graph.add_node('-'.join(record['Intents']), record['Service'])

        nodes = list(graph.dialogue_graph.nodes())
        for idx, record in enumerate(pd_df.to_records('dict')):
            try:
                graph.add_edge(nodes[idx], nodes[idx + 1], record['Actions'], record['Slot'])
            except IndexError:
                pass

        graphs_by_dialogue[id] = graph.graph_2_dict()

    return graphs_by_dialogue


class DialogueGraphCreationService:

    def __init__(self, is_synthetic: bool = False):
        super().__init__()
        self.mongodb_service = MongoDB()
        self.filename = SGD_DATASET_RES if not is_synthetic \
            else SGD_DATASET_RES_SYN
        self.file_result = self.filename + "_dialogue_graph"
        self.is_synthetic = is_synthetic
        self.priority = 6

    def process(self):
        Logger.info("DialogueGraphCreationService: Processing file: " + self.filename)
        pd_df = self.mongodb_service.load(self.filename)
        list_graph = create_dialogue_graph(pd_df)
        assert len(list_graph) > 0, "DialogueGraphCreationService: Empty dataset"
        self.mongodb_service.save(list_graph, self.file_result)
