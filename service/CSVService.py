import os
from abc import ABC
import pandas as pd

from service.InputService import InputService
from service.OutputService import OutputService


class CSVService(InputService, OutputService, ABC):

    def __init__(self, folder: str = 'results', sep: str = ';'):
        self.folder = folder
        self.sep = sep

    def load(self, path: str) -> object:
        return pd.read_csv(path, sep=self.sep)

    def save(self, data: object, path: str) -> None:
        assert isinstance(data, pd.DataFrame), "Data must be a pandas DataFrame"

        file = os.path.join(self.folder, f"{path}.csv")
        data.to_csv(file, sep=self.sep, index=False)
