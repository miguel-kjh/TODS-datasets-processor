from models.transformation.DialogueGraph import DialogueGraph
from service.Pipeline.Pipeline import Pipeline
from utils.ProjectConstants import SGD_DATASET_RES, SGD_DATASET_RES_SYN
from view.GraphView import GrapView
import networkx as nx

from view.Logger import Logger


class DialogueGraphViewService(Pipeline):

    def __init__(self, is_synthetic: bool = False):
        super().__init__()
        filename = SGD_DATASET_RES if not is_synthetic \
            else SGD_DATASET_RES_SYN
        self.filename = filename + "_dialogue_graph"
        self.is_synthetic = is_synthetic
        self.priority = 7

    def _deleted_unecessary_atributes(self, graph: dict) -> dict:
        return {
            key: value
            for key, value in graph.items()
            if key not in ['_id', 'Dialogue_id']
        }

    def process(self):
        list_dilogue_graph = self.mongodb_service.load(self.filename, to_pandas=False)
        assert len(list_dilogue_graph) > 0, "DialogueGraphViewService: Empty dataset"

        Logger.info("DialogueGraphViewService: Join all graphs into one")
        complete_graph = nx.compose_all(
            [
                nx.from_dict_of_dicts(
                    self._deleted_unecessary_atributes(graph)
                ) for graph in list_dilogue_graph[0:15]
            ]
        )

        GrapView.draw(complete_graph, 'dialogue_graph.html')
