import numpy as np
from tqdm import tqdm
from typing import List

import pandas as pd
from utils.ProjectConstants import list_actions


class DialogueParser:

    @staticmethod
    def _get_dataframe_schema() -> dict:
        return {
            'Dialogue Id': [],
            'Service': [],
            'Speaker': [],
            'Text': [],
            'Intents': [],
            'Intentions_slots': [],
            'Actions': [],
            'Actions_slots': [],
            'Slot': [],
            'Slot_values': [],
            'State_Intents': [],
            'State_slot': [],
            'State_slot_values': [],
        }

    @staticmethod
    def __sgd_to_dataframes(dialogues: list, type_dataset: str) -> pd.DataFrame:

        df = DialogueParser._get_dataframe_schema()

        for dialogue in tqdm(dialogues, desc='Parsing dialogues for %s' % type_dataset):

            story_len = len(dialogue['turns']['speaker'])
            df['Dialogue Id'] += [dialogue['dialogue_id']] * story_len
            df['Service'] += [dialogue['services']] * story_len
            df['Speaker'] += dialogue['turns']['speaker']
            df['Text'] += dialogue['turns']['utterance']

            for idx, turn in enumerate(dialogue['turns']['frames']):

                df['Actions'].append([list_actions[int(act)] for act in turn['actions'][0]['act']])
                df['Actions_slots'].append([act_slot for act_slot in turn['actions'][0]['slot']])

                try:
                    intent = turn['state'][0]['active_intent']
                    df['Intents'].append([list_actions[act] for act in turn['actions'][0]['act']])
                    df['Intentions_slots'].append([act_slot for act_slot in turn['actions'][0]['slot']])
                    df['State_Intents'].append(intent)
                except KeyError:
                    df['Intents'].append(None)
                    df['Original_Intents'].append(None)

                name_slot = turn['slots'][0]['slot']
                value_slot = [
                    df['Text'][idx][start:end]
                    for start, end in zip(
                        turn['slots'][0]['start'],
                        turn['slots'][0]['exclusive_end']
                    )
                ]

                df['Slot'].append(name_slot)
                df['Slot_values'].append(value_slot)

                name_slot = turn['state'][0]['slot_values']['slot_name']
                value_slot = turn['state'][0]['slot_values']['slot_value_list']

                df['State_slot'].append(name_slot)
                df['State_slot_values'].append(value_slot)

        return pd.DataFrame(df)

    @staticmethod
    def __multiwoz_to_dataframes(dialogues: list, type_dataset: str) -> pd.DataFrame:

        df = DialogueParser._get_dataframe_schema()

        for dialogue in tqdm(dialogues, desc='Parsing dialogues for %s' % type_dataset):

            story_len = len(dialogue['turns']['speaker'])
            df['Dialogue Id'] += [dialogue['dialogue_id']] * story_len
            df['Service'] += [dialogue['services']] * story_len
            df['Speaker'] += dialogue['turns']['speaker']
            df['Text'] += dialogue['turns']['utterance']

            for turn, speaker, act, utt in zip(
                    dialogue['turns']['frames'],
                    dialogue['turns']['speaker'],
                    dialogue['turns']['dialogue_acts'],
                    dialogue['turns']['utterance']
            ):

                df['Actions'].append(act['dialog_act']['act_type'])
                if not speaker:
                    df['Intents'].append(act['dialog_act']['act_type'])
                    name_slot = [state['slots_values']['slots_values_name'] for state in turn['state']]
                    value_slot = [state['slots_values']['slots_values_list'] for state in turn['state']]
                    state_intents = [state['active_intent'] for state in turn['state']]
                    df['Slot'].append(name_slot[0] if name_slot else name_slot)
                    df['Slot_values'].append(value_slot[0] if value_slot else value_slot)
                    df['State_Intents'].append(state_intents)
                    df['State_slot'].append(name_slot[0] if name_slot else name_slot)
                    df['State_slot_values'].append(value_slot[0] if value_slot else value_slot)
                else:
                    df['Intents'].append(None)
                    df['Slot'].append(None)
                    df['Slot_values'].append(None)
                    df['State_Intents'].append(None)
                    df['State_slot'].append(None)
                    df['State_slot_values'].append(None)

                df['Intentions_slots'].append(None)
                df['Actions_slots'].append(None)

        return pd.DataFrame(df)

    def transform(self, dialogues: List[dict], split: str, dataset_type: str) -> pd.DataFrame:

        if dataset_type == 'SGD_dataset':
            return self.__sgd_to_dataframes(dialogues, split)
        elif dataset_type == 'multi_woz_dataset':
            return self.__multiwoz_to_dataframes(dialogues, split)

        raise ValueError(f"Dataset type {dataset_type} not supported")
