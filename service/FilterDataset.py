# Criteria pattern for filtering dataset
from abc import abstractmethod, ABCMeta

import pandas as pd

from utils.ProjectConstants import Domain

DOMAIN_FOR_TINY_DATASET_SGD = ['Restaurants_1', 'Movies_1', 'Events_1', 'Hotels_1']
DOMAIN_FOR_TINY_DATASET_MULTI_WOZ = ['restaurants', 'train', 'hotel']


class FilterDataset(metaclass=ABCMeta):

    @abstractmethod
    def filter(self, dataset: pd.DataFrame) -> pd.DataFrame:
        pass


class FilterByColumn(FilterDataset):
    def __init__(self, column: str, condition: callable):
        self.column = column
        self.condition = condition

    def filter(self, dataset: pd.DataFrame) -> pd.DataFrame:
        if self.column is None or self.condition is None:
            return dataset

        return dataset[dataset[self.column].apply(
            lambda x: self.condition(x)
        )]


class TreeOfFilters(FilterDataset):
    def __init__(self, dataset: str, column_name: str = 'Domain'):
        subset_of_domains = DOMAIN_FOR_TINY_DATASET_SGD if dataset == 'SGD_dataset' \
            else DOMAIN_FOR_TINY_DATASET_MULTI_WOZ
        self.filters = {
            Domain.TINY: [FilterByColumn(column_name, lambda x: not x or x[0] in subset_of_domains and len(x) == 1)],
            Domain.SINGLEDOMAIN: [FilterByColumn(column_name, lambda x: len(x) == 1)],
            Domain.MULTIDOMAIN: [FilterByColumn(column_name, lambda x: len(x) > 1)],
            Domain.ALL: [FilterByColumn(None, None)],
        }

    def filter(self, dataset: pd.DataFrame):
        for domain, list_of_filters in self.filters.items():
            df_filtered = dataset.copy()
            for filter_ in list_of_filters:
                df_filtered = filter_.filter(df_filtered)
            yield domain.name, df_filtered
