import logging
from datetime import datetime
from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)


def dir_builder(output_path: Path):
    try:
        if not output_path.exists():
            logger.info(
                f"Dir - [{output_path}] not found. Proceeding to create the dir."
            )
            output_path.mkdir(parents=True, exist_ok=True)
    except Exception as error:
        logger.exception(f"Error while cleaning [{output_path}] - [{error}].")


def csv_path_builder(output_dir: Path) -> Path:
    file_datetime: str = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    return Path(f"{output_dir}/{file_datetime}.csv")
