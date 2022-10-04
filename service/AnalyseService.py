import copy
import random

import pandas as pd

from tqdm import tqdm
from typing import List

from models.DialogueStory import DialogueStory
from service.CSVService import CSVService
from service.MongoDB import MongoDB
from utils.utils import get_set_dialogues


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

    def _get_dialogues(
            self,
            dataset: pd.DataFrame,
            column_actions='Action',
            column_intent='Intention',
            column_dialogue_id='Dialogue ID',
            column_domain='Domain',
    ) -> List[DialogueStory]:

        dialogues = []

        for dialogue_id, dialogue in dataset.groupby(column_dialogue_id):
            dialogue_story = DialogueStory(str(dialogue_id), dialogue[column_domain].iloc[0])
            for row in dialogue.to_records('dict'):
                dialogue_story.add_intentions_actions(row[column_intent], row[column_actions])
            dialogues.append(dialogue_story)
        return dialogues

    def _transform_dataset_into_dialogues(self) -> None:
        self.datasets = {
            name: self._get_dialogues(dataset)
            for name, dataset in self.datasets.items()
        }

    def _check_ambiguity(self, dialogue_a: DialogueStory, dialogue_b: DialogueStory) -> bool:
        """
        Check if two dialogues are ambiguous
        :param dialogue_a: first dialogue
        :param dialogue_b: second dialogue
        :return: True if the dialogues are ambiguous, False otherwise
        """

        """for interaction_a in dialogue_a.to_records('dict'):
            for interaction_b in dialogue_b.to_records('dict'):
                if interaction_a[self._column_intent] == interaction_b[self._column_intent]:
                    if interaction_a[self._column_actions] != interaction_b[self._column_actions]:
                        return True
                else:
                    return False"""

        min_length = min(len(dialogue_a), len(dialogue_b))
        for interaction_a, interaction_b in zip(
                dialogue_a.dialogue_story[:min_length],
                dialogue_b.dialogue_story[:min_length]
        ):
            if interaction_a.state.intentions == interaction_b.state.intentions:
                if interaction_a.actions != interaction_b.actions:
                    return True
            else:
                return False
        return False

    def _calculate_ambiguity(self, dataset: List[DialogueStory], sample: int = 1000) -> float:
        """
        Calculate the ambiguity of the dataset
        :param dataset: dataset to calculate the ambiguity
        :param sample: sample of the dataset to calculate the ambiguity
        :return: ambiguity of the dataset
        """

        def to_percentage(value: float, length: int, decimals: int = 2) -> float:
            return round(value * 100 / length, decimals)

        dataset = copy.deepcopy(dataset)
        dataset = get_set_dialogues(dataset)
        dataset_sample = random.sample(dataset, sample)
        dataset_sample = [
            (dialogue_a, dialogue_b)
            for idx, dialogue_a in enumerate(dataset_sample)
            for dialogue_b in dataset_sample[idx + 1:]

        ]

        count_ambiguity = 0
        for dialogue_a, dialogue_b in tqdm(dataset_sample):
            if self._check_ambiguity(dialogue_a, dialogue_b):
                count_ambiguity += 1

        return to_percentage(count_ambiguity, len(dataset_sample))

    def _calculate_dataset_of_ambiguity(self, samples: int = 1000) -> pd.DataFrame:
        df = {
            'Dataset': [],
            'Ambiguity': [],
            'Number of Dialogues': [samples] * len(self.datasets)
        }

        for name, dataset in self.datasets.items():
            df['Dataset'].append(name)
            df['Ambiguity'].append(
                self._calculate_ambiguity(dataset, samples)
            )
        return pd.DataFrame(df)

    def process(self) -> None:
        df = self._calculate_dataset_of_ambiguity()
        self.csv_service.save(df, 'ambiguity')
