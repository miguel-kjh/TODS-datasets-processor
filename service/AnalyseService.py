
import pandas as pd


from service.CSVService import CSVService
from service.MongoDB import MongoDB
from utils.utils import get_dialogues, calculate_ambiguity


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
            path: MongoDB(path, config['database'][0]['path']).load(name)
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

    def process(self) -> None:
        df = self._calculate_dataset_of_ambiguity()
        self.csv_service.save(df, 'ambiguity')
