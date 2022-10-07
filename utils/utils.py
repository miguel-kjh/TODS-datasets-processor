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
        column_slot='Slots',
) -> List[DialogueStory]:
    dialogues = []

    for dialogue_id, dialogue in dataset.groupby(column_dialogue_id):
        dialogue_story = DialogueStory(str(dialogue_id), dialogue[column_domain].iloc[0])
        for row in dialogue.to_records('dict'):
            intentions = [intent.split('-')[-1] for intent in row[column_intent]]
            actions = [action.split('-')[-1] for action in row[column_actions]]
            slots = row[column_slot]
            dialogue_story.add_intentions_actions(intentions, actions, slots)
        dialogues.append(dialogue_story)
    return dialogues


def check_ambiguity(dialogue_a: DialogueStory, dialogue_b: DialogueStory) -> bool:
    """
    Check if two dialogues are ambiguous
    :param dialogue_a: first dialogue
    :param dialogue_b: second dialogue
    :return: True if the dialogues are ambiguous, False otherwise
    """

    if dialogue_a.domain != dialogue_b.domain:
        return False

    min_length = min(len(dialogue_a), len(dialogue_b))
    for interaction_a, interaction_b in zip(
            dialogue_a.dialogue_story[:min_length],
            dialogue_b.dialogue_story[:min_length]
    ):
        if interaction_a.state == interaction_b.state:
            if interaction_a.actions != interaction_b.actions:
                return True
        else:
            return False
    return False


def index_ambiguity(dialogue_a: DialogueStory, dialogue_b: DialogueStory) -> int:
    min_length = min(len(dialogue_a), len(dialogue_b))
    for idx, (interaction_a, interaction_b) in enumerate(zip(
            dialogue_a.dialogue_story[:min_length],
            dialogue_b.dialogue_story[:min_length]
    )):
        if interaction_a.state == interaction_b.state:
            if interaction_a.actions != interaction_b.actions:
                return idx
        else:
            return None
    return None


def calculate_ambiguity(dataset: List[DialogueStory], sample: int = 1000) -> float:
    """
    Calculate the ambiguity of the dataset
    :param dataset: dataset to calculate the ambiguity
    :param sample: sample of the dataset to calculate the ambiguity
    :return: ambiguity of the dataset
    """

    def to_percentage(value: float, length: int, decimals: int = 2) -> float:
        return round(value * 100 / length, decimals)

    dataset_sample = get_all_combinations(dataset, sample)

    count_ambiguity = 0
    for dialogue_a, dialogue_b in tqdm(dataset_sample):
        if check_ambiguity(dialogue_a, dialogue_b):
            count_ambiguity += 1

    return to_percentage(count_ambiguity, len(dataset_sample))


def get_ambiguity(dataset: List[DialogueStory], sample: int = 1000) -> List[tuple]:

    dataset_sample = get_all_combinations(dataset, sample)

    ambiguities = set()
    for dialogue_a, dialogue_b in tqdm(dataset_sample, desc="Get ambiguity", unit="dialogues"):
        if check_ambiguity(dialogue_a, dialogue_b):
            ambiguities.add((dialogue_a, dialogue_b))

    return list(ambiguities)


def get_all_combinations(dataset, sample):
    dataset_sample = random.sample(dataset, sample)
    dataset_sample = [
        (first_dialogue, last_dialogue)
        for idx, first_dialogue in enumerate(dataset_sample)
        for last_dialogue in dataset_sample[idx + 1:]
    ]
    return dataset_sample


def get_ambiguity_combinations(dataset: List[DialogueStory], sample=1000) -> List[tuple]:
    dataset_sample = get_all_combinations(dataset, sample)
    ambiguity = []
    for dialogue_a, dialogue_b in tqdm(dataset_sample):
        if check_ambiguity(dialogue_a, dialogue_b):
            ambiguity.append((dialogue_a, dialogue_b))

    return ambiguity


if __name__ == '__main__':
    dialogue_a = DialogueStory('id0', 'd1')
    dialogue_a.add_intentions_actions(
        ['I_I', 'I'],
        ['REQ_MORE']
    )
    dialogue_a.add_intentions_actions(
        ['I'],
        ['CONFIRM']
    )
    dialogue_a.add_intentions_actions(
        ['I'],
        ['REQ_MORE']
    )
    dialogue_b = DialogueStory('id1', 'd1')
    dialogue_b.add_intentions_actions(
        ['I_I', 'I'],
        ['REQ_MORE']
    )
    dialogue_b.add_intentions_actions(
        ['I'],
        ['REQ_MORE']
    )
    print(check_ambiguity(dialogue_a, dialogue_b))
    print(
        get_ambiguity_combinations([dialogue_a, dialogue_b], sample=2)
    )
