import ast
import os

import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List

from view.Logger import Logger

class DatasetCleaner:

    def __init__(self):
        self._dummy_mark = '_INTENT'
        self._id_name = 'Dialogue Id'
        self._intent_name = 'Intents'
        self._action_name = 'Actions'
        self._speaker_name = 'Speaker'
        self._type_name = 'Type'
        self._service_name = 'Service'

        self._user_speaker = 0
        self._system_speaker = 1

    def clean(self, datasets_sgd: List[pd.DataFrame]) -> pd.DataFrame:
        Logger.info('Reading datasets...')

        for df in datasets_sgd:
            index_row_system = df[df[self._speaker_name] == self._system_speaker].index
            action_values = df[self._action_name].values[index_row_system]
            df.drop(index_row_system, inplace=True)
            df[self._action_name] = action_values

        Logger.info('Merging datasets...')

        datasets_sgd[0][self._id_name] = datasets_sgd[0][self._id_name].apply(lambda x: x + '_train')
        datasets_sgd[1][self._id_name] = datasets_sgd[1][self._id_name].apply(lambda x: x + '_dev')
        datasets_sgd[2][self._id_name] = datasets_sgd[2][self._id_name].apply(lambda x: x + '_test')

        dataset = pd.concat(datasets_sgd)
        dataset[self._type_name] = np.concatenate(
            [
                ['train'] * len(datasets_sgd[0]), 
                ['dev'] * len(datasets_sgd[1]), 
                ['test'] * len(datasets_sgd[2])
            ]
        )

        Logger.info('Cleaning datasets...')

        dataset.drop(columns=[self._speaker_name], inplace=True)
        #dataset[self._action_name] = dataset[self._action_name].apply(lambda acts: list(set(acts)))
        #dataset[self._intent_name] = dataset[self._intent_name].apply(lambda x: [x[-1]])
        #dataset[self._action_name] = dataset[self._action_name].apply(lambda x: list(set(ast.literal_eval(x))))
        #dataset[self._intent_name] = dataset[self._intent_name].apply(
        #    lambda x: x.replace(self._dummy_mark, '') if self._dummy_mark in x else x)

        return dataset