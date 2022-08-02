from tqdm import tqdm

from models.DatasetCleaner import DatasetCleaner
from service.MongoDB import MongoDB
from utils.ProjectConstants import SGD_DATASET_RES
from service.FilterDataset import TreeOfFilters


class CleanDataService:
    def __init__(self, config: dict):
        super().__init__()
        self.mongodb_service = MongoDB(
            config['dataset']['DB_name'],
            config['database'][0]['path']
        )
        self.filename = config['dataset']['filename']
        self.filters = TreeOfFilters()
        self.dataset_cleaner = DatasetCleaner()
        self.dataset_types = [
            f"{self.filename}_train",
            f"{self.filename}_validation",
            f"{self.filename}_test"
        ]

    def process(self):
        df_list = [self.mongodb_service.load(file) for file in self.dataset_types]
        final_df = self.dataset_cleaner.clean(df_list)
        self.mongodb_service.save(final_df, SGD_DATASET_RES)

        for domain_name, file in tqdm(self.filters.filter(final_df), desc="CleanDataService: Filtering dataset"):
            self.mongodb_service.save(file, f"{SGD_DATASET_RES}_{domain_name}")


