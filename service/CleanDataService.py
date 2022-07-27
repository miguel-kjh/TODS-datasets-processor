from models.DatasetCleaner import DatasetCleaner
from service.MongoDB import MongoDB
from utils.ProjectConstants import SGD_DATASET_RES


class CleanDataService:
    def __init__(self):
        super().__init__()
        self.mongodb_service = MongoDB()
        self.filename = 'SGD_dataset'
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
