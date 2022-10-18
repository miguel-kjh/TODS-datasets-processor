from copy import copy

import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List

from models.schemaDatabases import SchemaDatabase
from view.Logger import Logger
from utils.utils import list2atomic_item


class DatasetCleaner:

    def __init__(self):
        self._id_name = 'Dialogue Id'
        self._intent_name = 'Intents'
        self._action_name = 'Actions'
        self._speaker_name = 'Speaker'
        self._type_name = 'Type'
        self._service_name = 'Service'
        self._task_name = 'Original_Intents'

        self.dummy_action = 'LISTEN'

        self._user_speaker = 0
        self._system_speaker = 1
        self.schemaDatabase = SchemaDatabase()

    def clean(self, datasets_sgd: List) -> pd.DataFrame:

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

        Logger.info(f'Number of dialogues: {len(dataset[self._id_name].unique())}')

        for id, df in tqdm(dataset.groupby(by="Dialogue Id"), desc="Cleaning datasets..."):

            if [] not in df[self._action_name].tolist() and "" not in df[self._action_name].tolist():
                for i in range(0, len(df), 2):
                    row_1 = df.iloc[i]
                    row_2 = df.iloc[i + 1]

                    actions = copy(row_2[self._action_name])
                    actions.append(self.dummy_action)
                    atomic_action = list2atomic_item(row_2[self._action_name])
                    atomic_action.append(self.dummy_action)

                    # TODO: stack this method in only one
                    self.schemaDatabase.add_dialogue_id(id)
                    self.schemaDatabase.add_domain(row_1[self._service_name])
                    self.schemaDatabase.add_task(row_1["State_Intents"])
                    self.schemaDatabase.add_user_utterance(row_1["Text"])
                    self.schemaDatabase.add_intention(row_1[self._intent_name])
                    self.schemaDatabase.add_atomic_intent(list2atomic_item(row_1[self._intent_name]))
                    self.schemaDatabase.add_slots(row_1["State_slot"])
                    self.schemaDatabase.add_slots_value(row_1["State_slot_values"])
                    self.schemaDatabase.add_bot_response(row_2["Text"])
                    self.schemaDatabase.add_action(actions)
                    self.schemaDatabase.add_atomic_action(atomic_action)
                    self.schemaDatabase.add_type(row_2[self._type_name])
                    self.schemaDatabase.add_mandatory_slots([])
                    self.schemaDatabase.add_mandatory_slots_value([])
                    self.schemaDatabase.add_optional_slots(row_1["State_slot"])
                    self.schemaDatabase.add_optional_slots_value(row_1["State_slot_values"])
                    self.schemaDatabase.add_entities(row_1["Slot"])
                    self.schemaDatabase.add_entities_value(row_1["Slot_values"])

        df_cleaned = pd.DataFrame(self.schemaDatabase.get_dataset_schema())
        Logger.info(f'Number of dialogues in the final datasets: {len(df_cleaned["Dialogue ID"].unique())}')
        return df_cleaned
