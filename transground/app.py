import logging
import pandas as pd

from pathlib import Path

from utils.logger import log_setup
from utils.pathfinder import dir_builder, csv_path_builder


def main():
    dir_builder(output_path=OUTPUT_DIR)
    csv_file_path: Path = csv_path_builder(output_dir=OUTPUT_DIR)
    data_to_clean: Path = Path(
        f"{PARENT_DIR}/sample_data/data_for_assignment_to_clean.csv"
    )
    target_df: pd.DataFrame = pd.read_csv(data_to_clean, na_values=["None", "-"])
    target_df["LatestQuarter"] = pd.to_datetime(
        target_df["LatestQuarter"], format="%Y/%m/%d", infer_datetime_format=True
    )
    target_df.to_csv(csv_file_path, index=False, header=True)


if __name__ == "__main__":
    # Setting up directory using pathlib module
    PARENT_DIR: Path = Path(__file__).resolve().parents[1]
    OUTPUT_DIR: Path = Path(f"{PARENT_DIR}/transground/output")
    # Logger setup
    logger: logging.Logger = log_setup(
        parent_dir=f"{PARENT_DIR}",
        log_filename=f"{PARENT_DIR.name}",
        logger_level="INFO",
    )
    main()
