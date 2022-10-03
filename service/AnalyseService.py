import copy
import random

import pandas as pd

from tqdm import tqdm

from service.CSVService import CSVService
from service.MongoDB import MongoDB


class AnalyseService:

    def __init__(self, config: dict):
        names_datasets = \
            {
                'multi_woz': 'multi_woz_dataset_ALL',
                'SGD': 'SGD_dataset_ALL',
            }
        self.datasets = {
            name: MongoDB(path, config['database'][0]['path']).load(name)
            for path, name in names_datasets.items()
        }

        self._column_actions = 'Action'
        self._column_intent = 'Intent'
        self._column_dialogue_id = 'Dialogue ID'

        self.csv_service = CSVService()

        # check if the datasets are loaded correctly
        for name, dataset in self.datasets.items():
            assert len(dataset) > 0, f"Dataset {name} is empty"

    def _check_ambiguity(self, dialogue_a: pd.Series, dialogue_b: pd.Series) -> bool:
        """
        Check if two dialogues are ambiguous
        :param dialogue_a: first dialogue
        :param dialogue_b: second dialogue
        :return: True if the dialogues are ambiguous, False otherwise
        """

        for interaction_a in dialogue_a.to_records('dict'):
            for interaction_b in dialogue_b.to_records('dict'):
                if interaction_a[self._column_intent] == interaction_b[self._column_intent]:
                    if interaction_a[self._column_actions] != interaction_b[self._column_actions]:
                        return True
                else:
                    return False

        return False

    def _calculate_ambiguity(self, dataset: pd.DataFrame, sample: int = 1000) -> float:
        """
        Calculate the ambiguity of the dataset
        :param dataset: dataset to calculate the ambiguity
        :param sample: sample of the dataset to calculate the ambiguity
        :return: ambiguity of the dataset
        """

        def to_portion(ambiguity: int, length: int, multiplier: int = 100, to_round: int = 2) -> float:
            return round(ambiguity * multiplier / length, to_round)

        dataset_sample = copy.deepcopy(dataset)
        columns = [self._column_dialogue_id, self._column_intent, self._column_actions]
        dataset_sample = dataset_sample[columns]
        dataset_sample = list(dataset_sample.groupby(self._column_dialogue_id))
        dataset_sample = random.sample(dataset_sample, sample)
        dataset_sample = [
            (dialogue_a, dialogue_b)
            for idx, dialogue_a in enumerate(dataset_sample)
            for dialogue_b in dataset_sample[idx + 1:]

        ]

        count_ambiguity = 0
        for dialogue_a, dialogue_b in tqdm(dataset_sample):
            if self._check_ambiguity(dialogue_a[1], dialogue_b[1]):
                count_ambiguity += 1

        return to_portion(count_ambiguity, len(dataset_sample))

    def _create_dataset_of_ambiguity(self, sample: int = 1000) -> pd.DataFrame:
        """
        Create a dataset of ambiguity
        :param sample:
        :return dataset of ambiguity:
        """
        df = {
            'dataset': [],
            'ambiguity(%)': [],
            'sample': [sample] * len(self.datasets),
        }
        for name, dataset in self.datasets.items():
            df['dataset'].append(name)
            df['ambiguity(%)'].append(
                self._calculate_ambiguity(dataset, sample=sample)
            )

        return pd.DataFrame(df)

    def process(self) -> None:
        """
        Process the ambiguity of the datasets
        :return:
        """

        df = self._create_dataset_of_ambiguity()
        self.csv_service.save(df, 'ambiguity')
