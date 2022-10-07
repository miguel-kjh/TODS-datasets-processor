import pandas as pd
from typing import List, Tuple

from pandas import DataFrame

from models.DialogueStory import DialogueStory
from service.CSVService import CSVService
from service.MongoDB import MongoDB
from utils.utils import get_dialogues, calculate_ambiguity, get_ambiguity


class AnalyseService:

    def __init__(self, config: dict):

        self.datasets = None
        self.csv_service = CSVService()

        self._load_dataset(config)
        self._check_if_the_datasets_are_loaded_correctly()
        self._transform_dataset_into_dialogues()

    def _load_dataset(self, config: dict, names_datasets=None, sub_set: str = 'ALL') -> None:

        if names_datasets is None:
            names_datasets = {
                'multi_woz': f'multi_woz_dataset_{sub_set}',
                'SGD': f'SGD_dataset_{sub_set}',
            }

        self.datasets = {
            path: MongoDB(path, config['database']['path']).load(name)
            for path, name in names_datasets.items()
        }

    def _check_if_the_datasets_are_loaded_correctly(self) -> None:
        for name, dataset in self.datasets.items():
            assert len(dataset) > 0, f"Dataset {name} is empty"

    def _transform_dataset_into_dialogues(self) -> None:
        self.datasets = {
            name: get_dialogues(dataset)
            for name, dataset in self.datasets.items()
        }

    def _calculate_dataset_of_ambiguity(self, samples: int = 1000) -> pd.DataFrame:
        df = {
            'Dataset': [],
            'Ambiguity': [],
            'Number of Dialogues': [samples] * len(self.datasets)
        }

        for name, dataset in self.datasets.items():
            df['Dataset'].append(name)
            df['Ambiguity'].append(
                calculate_ambiguity(dataset, samples)
            )
        return pd.DataFrame(df)

    def _calculate_types_of_ambiguous_dialogues_for_dataset(
            self,
            dataset: List[DialogueStory]
    ) -> tuple[DataFrame, DataFrame]:

        df = {
            'Id_Ambiguous_Dialogue': [],
            'Id_A': [],
            'Id_B': [],
            'Domain': [],
            'Intention_A': [],
            'Intention_B': [],
            'Action_A': [],
            'Action_B': [],
        }

        df_freq = {
            'Id_Ambiguous_Dialogue': [],
            'Freq': [],
        }

        for idx, ((dialogue_a, dialogue_b), freq) in enumerate(get_ambiguity(dataset).items()):
            for intentions, actions in zip(
                    zip(dialogue_a.get_intentions(), dialogue_b.get_intentions()),
                    zip(dialogue_a.get_actions(), dialogue_b.get_actions())
            ):
                df['Id_Ambiguous_Dialogue'].append(idx)
                df['Id_A'].append(dialogue_a.id)
                df['Id_B'].append(dialogue_b.id)
                df['Domain'].append(dialogue_a.domain)
                df['Intention_A'].append(intentions[0])
                df['Intention_B'].append(intentions[1])
                df['Action_A'].append(actions[0])
                df['Action_B'].append(actions[1])
            df_freq['Id_Ambiguous_Dialogue'].append(idx)
            df_freq['Freq'].append(freq)
        return pd.DataFrame(df), pd.DataFrame(df_freq)

    def _calculate_types_of_ambiguous_dialogues(self) -> None:
        for name, dataset in self.datasets.items():
            df, df_freq = self._calculate_types_of_ambiguous_dialogues_for_dataset(dataset)
            self.csv_service.save(df, f'ambiguous_dialogues_{name}')
            self.csv_service.save(df_freq, f'ambiguous_dialogues_freq_{name}')

    def process(self) -> None:
        #df = self._calculate_dataset_of_ambiguity()
        #self.csv_service.save(df, 'ambiguity')
        self._calculate_types_of_ambiguous_dialogues()
