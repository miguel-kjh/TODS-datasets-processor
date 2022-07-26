from tqdm import tqdm
from typing import List

import pandas as pd
from utils.datasetUtils import list_actions

class DialogueParser:

    @staticmethod
    def _dialogues_to_dataframes(dialogues: list, type_dataset: str, is_categorical_slots: dict) -> pd.DataFrame:

        df = {
            'Dialogue Id': [],
            'Service': [],
            'Speaker': [],
            'Text': [],
            'Actions': [],
            'Intents': [],
            'Original_Intents': [],
            'Slot': [],
            'Slot_values': [],
            'Entity': [],
            'Entity_values': []
        }

        for dialogue in tqdm(dialogues, desc='Parsing dialogues for %s' % type_dataset):

            story_len = len(dialogue['turns']['speaker'])
            df['Dialogue Id'] += [dialogue['dialogue_id']] * story_len
            df['Service'] += [dialogue['services']] * story_len
            df['Speaker'] += dialogue['turns']['speaker']
            df['Text'] += dialogue['turns']['utterance']

            for turn in dialogue['turns']['frames']:

                df['Actions'].append([list_actions[int(act)] for act in turn['actions'][0]['act']])

                try:
                    intent = turn['state'][0]['active_intent']
                    df['Intents'].append([list_actions[act] for act in turn['actions'][0]['act']])
                    df['Original_Intents'].append(intent)
                except KeyError:
                    df['Intents'].append(None)
                    df['Original_Intents'].append(None)

                name_slot = turn['state'][0]['slot_values']['slot_name']
                value_slot = turn['state'][0]['slot_values']['slot_value_list']

                slots_and_entities = {
                    'Slot': {
                        'name': [],
                        'value': []
                    },
                    'Entity': {
                        'name': [],
                        'value': []
                    }
                }

                for name, value in zip(name_slot, value_slot):

                    if is_categorical_slots[name]:
                        slots_and_entities['Slot']['name'].append(name)
                        slots_and_entities['Slot']['value'].append(value)
                    else:
                        if len(df['Entity']) == 0 or df['Entity'][-1] != name:
                            slots_and_entities['Entity']['name'].append(name)
                            slots_and_entities['Entity']['value'].append(value)

                df['Slot'].append(slots_and_entities['Slot']['name'])
                df['Slot_values'].append(slots_and_entities['Slot']['value'])
                df['Entity'].append(slots_and_entities['Entity']['name'])
                df['Entity_values'].append(slots_and_entities['Entity']['value'])

        return pd.DataFrame(df)

    def transform(self, dialogues: List[dict], split: str, is_categorical_slot: dict) -> pd.DataFrame:
        return self._dialogues_to_dataframes(dialogues, split, is_categorical_slot)
