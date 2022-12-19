import pandas as pd

from models.DialogueParser import DialogueParser
from service.MongoDB import MongoDB
from view.Logger import Logger
from models.ConvlabDownloader import ConvlabDownloader


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
        Logger.info("save to {}".format(file))
