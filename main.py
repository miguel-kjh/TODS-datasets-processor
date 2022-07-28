import argparse
import os

import warnings

import yaml

from service.CleanDataService import CleanDataService
from service.TransformDialogueService import TransformDialogueService
from utils.ProjectConstants import REPOSITORY_PATH
from view.Logger import Logger

warnings.filterwarnings("ignore", ".*")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action='count', help="parse the dialogues")
    parser.add_argument("--clean", action='count', help="clean the data")
    return parser.parse_args()


def main():
    args = parse_args()

    for action in args.__dict__:
        if args.__dict__[action]:
            if action == "download":
                TransformDialogueService().process()
            elif action == "clean":
                CleanDataService().process()


if __name__ == "__main__":
    main()
    """from datasets import load_dataset

    dataset = load_dataset("multi_woz_v22")
    example = dataset['test'].to_dict()['turns'][0]
    print(example.keys())
    print(example)
    print("FRAMES")
    print(yaml.dump(example['frames']))
    print("ACTS")
    print(yaml.dump(example['dialogue_acts']))"""
    """
     turns: los dialogos -> lista
     'turn_id', 'speaker', 'utterance', 'frames', 'dialogue_acts'
    """
