import copy
import random
from typing import List

import pandas as pd
from tqdm import tqdm

from models.DialogueStory import DialogueStory


def list2atomic_item(*kargs, sep="-") -> list:
    """
    Convert a list to an atom.
    """
    st = [
        sep.join(arg)
        for arg in kargs
    ]
    return [sep.join(st)]


def get_set_dialogues(dataset: List[DialogueStory]) -> List[DialogueStory]:
    set_dialogues = []
    for dialogue in tqdm(dataset, desc="Get set dialogues", unit="dialogues"):
        if dialogue not in set_dialogues:
            set_dialogues.append(dialogue)
    return set_dialogues


def get_dialogues(
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


def check_ambiguity(dialogue_a: DialogueStory, dialogue_b: DialogueStory) -> bool:
    """
    Check if two dialogues are ambiguous
    :param dialogue_a: first dialogue
    :param dialogue_b: second dialogue
    :return: True if the dialogues are ambiguous, False otherwise
    """

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


def calculate_ambiguity(dataset: List[DialogueStory], sample: int = 1000) -> float:
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
        if check_ambiguity(dialogue_a, dialogue_b):
            count_ambiguity += 1

    return to_percentage(count_ambiguity, len(dataset_sample))
