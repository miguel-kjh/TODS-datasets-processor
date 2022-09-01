from copy import copy

import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from models.DatasetCleaner import DatasetCleaner
from service.MongoDB import MongoDB
from service.FilterDataset import TreeOfFilters
from utils.ProjectConstants import Domain
from view.Logger import Logger


class CleanDataService:
    def __init__(self, config: dict, train_test_split: float = 0.6, val_split: float = 0.2, test_split: float = 0.2):
        super().__init__()

        assert train_test_split + val_split + test_split == 1, "train_test_split + val_split + test_split must be 1"

        self.mongodb_service = MongoDB(
            config['dataset']['DB_name'],
            config['database'][0]['path']
        )
        self.filename = config['dataset']['filename']
        self.filters = TreeOfFilters(self.filename)
        self.dataset_cleaner = DatasetCleaner()
        self.dataset_types = [
            f"{self.filename}_train",
            f"{self.filename}_validation",
            f"{self.filename}_test"
        ]
        self.train_test_split = train_test_split
        self.val_split = val_split
        self.test_split = test_split

    @staticmethod
    def train_val_test_split(X, y, train_size, val_size, test_size):
        X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=test_size)
        relative_train_size = train_size / (val_size + train_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val,
            y_train_val,
            train_size=relative_train_size,
            test_size=1 - relative_train_size
        )
        return X_train, X_val, X_test, y_train, y_val, y_test

    def _changes_the_division_of_data(self, df: pd.DataFrame) -> pd.DataFrame:
        list_idx_stories = df["Dialogue ID"].unique().tolist()
        X_train, X_val, X_test, _, _, _ = self.train_val_test_split(
            list_idx_stories,
            list_idx_stories,
            self.train_test_split,
            self.val_split,
            self.test_split
        )
        new_distribution = []
        for idx, dialogue_id in enumerate(df["Dialogue ID"].tolist()):
            if dialogue_id in X_train:
                new_distribution.append("train")
            elif dialogue_id in X_val:
                new_distribution.append("dev")
            elif dialogue_id in X_test:
                new_distribution.append("test")

        df['Type'] = copy(new_distribution)
        return df

    def process(self):
        df_list = [self.mongodb_service.load(file) for file in self.dataset_types]
        Logger.info(f"clean data form {self.filename}")

        final_df = self.dataset_cleaner.clean(df_list)
        self.mongodb_service.save(final_df, self.filename)

        Logger.info(f"\nsave to {self.mongodb_service.dBName} database")
        for domain_name, file in tqdm(self.filters.filter(final_df), desc="CleanDataService: Filtering dataset"):
            Logger.info(f"save to {self.mongodb_service.dBName} database - {domain_name}")
            if domain_name != Domain.ALL.name:
                file = self._changes_the_division_of_data(file)
            self.mongodb_service.save(file, f"{self.filename}_{domain_name}")
