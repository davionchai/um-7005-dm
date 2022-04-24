import argparse
import logging

from pathlib import Path

from models.arguments import ArgumentModel
from utils.logger import log_setup


def main(source_args: argparse.Namespace):
    args: ArgumentModel = ArgumentModel(source_args=source_args)


if __name__ == "__main__":
    # Setting up directory using pathlib module
    PARENT_DIR: Path = Path(__file__).resolve().parent
    # Logger setup
    logger: logging.Logger = log_setup(
        parent_dir=f"{PARENT_DIR}",
        log_filename=f"{PARENT_DIR.name}",
        logger_level="INFO",
    )
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-key",
        "--api-key",
        type=str,
        required=True,
        help="API Key given from alpha vantage.",
    )
    parser.add_argument(
        "-s", "--stock", type=str, required=True, help="Specify the target stock name.",
    )
    parser.add_argument(
        "-func",
        "--function",
        type=str,
        required=True,
        help="Specify the alpha vantage function.",
    )
    main(parser.parse_args())
