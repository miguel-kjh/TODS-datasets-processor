from typing import List

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
