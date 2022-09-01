import warnings
import random

import hydra
import numpy as np
from omegaconf import DictConfig

from service.CleanDataService import CleanDataService
from service.TransformDialogueService import TransformDialogueService

warnings.filterwarnings("ignore", ".*")


def reset_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    reset_seed(cfg.seed)
    if cfg.operation == "download":
        TransformDialogueService(cfg).process()
    elif cfg.operation == "clean":
        CleanDataService(cfg).process()


if __name__ == "__main__":
    main()
