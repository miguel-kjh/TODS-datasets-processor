import os

from enum import Enum


class Domain(Enum):
    SINGLEDOMAIN = 1
    MULTIDOMAIN = 2
    ALL = 3
    TINY = 4
    CHANGE_IDEA = 5

list_actions = [
    'AFFIRM',
    'AFFIRM_INTENT',
    'CONFIRM',
    'GOODBYE',
    'INFORM',
    'INFORM_COUNT',
    'INFORM_INTENT',
    'NEGATE',
    'NEGATE_INTENT',
    'NOTIFY_FAILURE',
    'NOTIFY_SUCCESS',
    'OFFER',
    'OFFER_INTENT',
    'REQUEST',
    'REQUEST_ALTS',
    'REQ_MORE',
    'SELECT',
    'THANK_YOU',
]

# Paths

REPOSITORY_PATH = "schema_guided_dstc8"

HYPER_PARAMETERS_FOLDER = os.path.join(
    'configurations'
)
FOLDER_TO_SAVE_MODEL = os.path.join(
    'trained_models'
)

RES_DATA_FOLDER = os.path.join(
    'data',
    'res'
)
METRIC_FOLDER = os.path.join(
    "data",
    'metrics'
)

SGD_DATASET_INT: list = [
    'SGD_dataset_train'
    'SGD_dataset_validation',
    'SGD_dataset_test',
]

SGD_DATASET_RES: str = 'SGD_dataset'

SGD_DATASET_RES_SYN: str = 'SGD_dataset_syn'

SYSTEM_ACTIONS = [
    'NOTIFY_SUCCESS',
    'OFFER_INTENT',
    'REQ_MORE',
    'OFFER',
    'CONFIRM',
    'GOODBYE',
    'INFORM',
    'INFORM_COUNT',
    'NOTIFY_FAILURE',
    'REQUEST'
]

SYSTEM_ACTIONS.sort()

ENTITIES_SGD = []

