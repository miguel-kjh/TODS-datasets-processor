import pandas as pd
from typing import Tuple, List

from models.DialogueParser import DialogueParser
from service.MongoDB import MongoDB
from view.Logger import Logger
from models.ConvlabDownloader import ConvlabDownloader
import numpy as np


class State:

    def __init__(self, intention: List[str], slots: List[str], action: str):
        self.intention = intention
        self.slots = slots
        self.action = action


class TransformDialogueService:

    def __init__(self, config: dict):
        super().__init__()
        # self._dataset = load_dataset(config['dataset']['path'])
        # self._dataset_schema = load_dataset(config['dataset']['path'], name=config['dataset']['name_'])
        self._dataset = {  # TODO: change convlabDownloader to load_dataset even the data_split
            'train': ConvlabDownloader(config['dataset']['path'], 'train'),
            'dev': ConvlabDownloader(config['dataset']['path'], 'validation'),
            'test': ConvlabDownloader(config['dataset']['path'], 'test')
        }
        self.parser = DialogueParser()
        self.mongodb_service = MongoDB(config['dataset']['DB_name'], config['database']['path'])
        self.filename = config['dataset']['filename']

    @staticmethod
    def _get_is_categorical_slot(schema: dict) -> dict:

        is_categorical_slot = {}

        for slot in schema:
            for name, is_categorical in zip(slot['name'], slot['is_categorical']):
                is_categorical_slot[name] = is_categorical

        return is_categorical_slot

    @staticmethod
    def _std_dataset(dataset: pd.DataFrame) -> dict:
        return {
            'Amount Dialogues': len(dataset['Dialogue ID'].unique()),
            'Amount Utterances': len(dataset),
            'Mean Utterances per Dialogue': round(len(dataset) / len(dataset['Dialogue ID'].unique())),
            'Incomplete Dialogues': len(
                dataset[dataset['Action'].apply(lambda x: len(x)) == 0]['Dialogue ID'].unique()),
        }

    @staticmethod
    def _clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
        dialogues_id_are_incomplete = df[df['Action'].apply(lambda x: len(x)) == 0]['Dialogue ID'].unique()
        return df[~df['Dialogue ID'].isin(dialogues_id_are_incomplete)]

    @staticmethod
    def _delete_ambiguous_dialogues(df: pd.DataFrame) -> pd.DataFrame:
        df_without_ambiguous_dialogues = df.copy()
        map_actions = {
            'inform': 'inform',
            'request': 'inform',
            'select': 'inform',
            'recommend': 'inform',
            'reqmore': 'inform',
            'select': 'inform',

        }
        actions = []
        for acts in df_without_ambiguous_dialogues['Action']:
            list_actions = []
            for act in acts:
                for key, value in map_actions.items():
                    if key in act:
                        act = act.replace(key, value)
                list_actions.append(act)
            actions.append(list_actions)
        df_without_ambiguous_dialogues['Action'] = actions
        return df_without_ambiguous_dialogues

    def process(self):

        df = pd.DataFrame()
        for split in self._dataset.keys():
            df_split = self.parser.transform(self._dataset[split], split, self.filename)
            df = pd.concat([df, df_split], ignore_index=True)

        df_std = self._std_dataset(df)
        Logger.print_dict(df_std)
        df = self._clean_dataset(df)
        file = "{}_{}".format(self.filename, 'ALL')
        df.to_csv('{}.csv'.format(file), index=False, encoding='utf-8', sep=';')
        self.mongodb_service.save(
            df,
            file
        )
        self.mongodb_service.save(
            pd.DataFrame(df_std, index=[0]),
            '{}_{}'.format(self.filename, 'STD')
        )
        df_without_ambiguous_dialogues = self._delete_ambiguous_dialogues(df)
        self.mongodb_service.save(
            df_without_ambiguous_dialogues,
            '{}_{}'.format(self.filename, 'NO_AMBIGUOUS')
        )
        df_without_ambiguous_dialogues.to_csv('{}_{}.csv'.format(self.filename, 'NO_AMBIGUOUS'), index=False,
                                              encoding='utf-8', sep=';')
        Logger.info("save to {}".format(file))
