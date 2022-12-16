import numpy as np
from tqdm import tqdm
from typing import List

import pandas as pd

from models.ConvlabDownloader import ConvlabDownloader
from utils.ProjectConstants import list_actions


class DialogueParser:

    dataset_schema = [
        "Dialogue ID",
        "Domain",
        "User_Utterance",
        "Intention",
        "Entities",
        "Entities Value",
        "Slots",
        "Slots Value",
        "Bot_Utterance",
        "Action",
        "Type",
    ]

    def _get_id(self, dialogue_idx: int) -> str:
        return f'Dialogue_{dialogue_idx}'

    @staticmethod
    def _get_dataframe_schema() -> dict:
        return {key: [] for key in DialogueParser.dataset_schema}

    def _to_df(self, dialogues: ConvlabDownloader, split: str,  dataset_type: str) -> pd.DataFrame:
        df = DialogueParser._get_dataframe_schema()

        dialogue_idx = 0
        for dialogue in tqdm(dialogues.policy_data, desc=f'Parsing dialogues for {split} - {dataset_type}'):

            if dialogue['context'][0]['utt_idx'] == 0:
                dialogue_idx += 1
            df['Dialogue ID'].append(self._get_id(dialogue_idx))
            df['Bot_Utterance'].append(dialogue['utterance'])
            actions = []
            domain = set()
            for _, intents in dialogue['dialogue_acts'].items():
                for intent in intents:
                    actions.append(f'{intent["domain"]}_{intent["intent"]}_{intent["slot"]}')
                    domain.add(intent['domain'])
            df['Action'].append(actions)
            df['Domain'].append(list(domain))

            user_data = dialogue['context'][0]
            df['User_Utterance'].append(user_data['utterance'])
            entities = []
            entities_value = []
            intentions = []
            for intents in user_data['dialogue_acts'].values():
                for intent in intents:
                    intentions.append(intent["intent"])
                    if intent['slot'] != '':
                        entities.append(intent['slot'])
                        try:
                            entities_value.append(intent['value'])
                        except KeyError:
                            entities_value.append('')

            df['Intention'].append(intentions)
            df['Entities'].append(entities)
            df['Entities Value'].append(entities_value)

            slots = []
            slots_value = []
            for state in user_data['state'].values():
                for slot, value in state.items():
                    if value != '':
                        slots.append(slot)
                        slots_value.append(value)

            df['Slots'].append(slots)
            df['Slots Value'].append(slots_value)
            df['Type'].append(split)

        df = pd.DataFrame(df)
        #save csv
        if split == 'test':
            df.to_csv(f'{split}_{dataset_type}.csv', index=False, encoding='utf-8', sep=';')

        return df

    def transform(self, dialogues: ConvlabDownloader, split: str, dataset_type: str) -> pd.DataFrame:
        return self._to_df(dialogues, split, dataset_type)
