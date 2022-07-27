import argparse
import os

import warnings

from service.CleanDataService import CleanDataService
from service.TransformDialogueService import TransformDialogueService
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
