import warnings
import random

import hydra
import numpy as np
from omegaconf import DictConfig

from service.AnalyseService import AnalyseService
from service.CleanDataService import CleanDataService
from service.TransformDialogueService import TransformDialogueService

warnings.filterwarnings("ignore", ".*")

operations = {
    'analyse': AnalyseService,
    'clean': CleanDataService,
    'download': TransformDialogueService
}


def reset_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    reset_seed(cfg.seed)
    operations[cfg.operation](cfg).process()


if __name__ == "__main__":
    main()
