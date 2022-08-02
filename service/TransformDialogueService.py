from models.DialogueParser import DialogueParser
from service.MongoDB import MongoDB
from utils.ProjectConstants import REPOSITORY_PATH
from view.Logger import Logger

from datasets import load_dataset


class TransformDialogueService:

    def __init__(self, config: dict):
        super().__init__()
        self._dataset = load_dataset(config['dataset']['path'])
        self._dataset_schema = load_dataset(config['dataset']['path'], name='schema')
        self.parser = DialogueParser()
        self.mongodb_service = MongoDB(config['dataset']['DB_name'], config['database'][0]['path'])
        self.filename = config['dataset']['filename']

    @staticmethod
    def _get_is_categorical_slot(schema: dict) -> dict:

        is_categorical_slot = {}

        for slot in schema:
            for name, is_categorical in zip(slot['name'], slot['is_categorical']):
                is_categorical_slot[name] = is_categorical

        return is_categorical_slot

    def process(self):

        for split in self._dataset.keys():
            is_categorical_slots = self._get_is_categorical_slot(
                self._dataset_schema[split].to_dict()['slots']
            )
            df = self.parser.transform(self._dataset[split], split, is_categorical_slots)
            file = "{}_{}".format(self.filename, split)
            self.mongodb_service.save(
                df,
                file
            )
            Logger.info("save to {}".format(file))
