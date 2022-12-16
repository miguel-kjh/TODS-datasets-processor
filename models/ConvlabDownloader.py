from convlab.util import load_dataset
from convlab.util import load_nlu_data, load_dst_data, load_policy_data

from view.Logger import Logger


class ConvlabDownloader:

    def __init__(self, path: str, data_split: str):
        self.path = path
        dataset = load_dataset(self.path)
        self.policy_data = load_policy_data(dataset, data_split=data_split, speaker='system')[data_split]
        Logger.info(f'Loaded {data_split} dataset from {path}')

