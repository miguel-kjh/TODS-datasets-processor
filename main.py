import warnings
import hydra
from omegaconf import DictConfig

from service.CleanDataService import CleanDataService
from service.TransformDialogueService import TransformDialogueService

warnings.filterwarnings("ignore", ".*")


@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    if cfg.operation == "download":
        TransformDialogueService(cfg).process()
    elif cfg.operation == "clean":
        CleanDataService(cfg).process()

if __name__ == "__main__":
    main()