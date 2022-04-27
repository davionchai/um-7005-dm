import argparse
import logging
import importlib
import json

from pathlib import Path
from requests.models import Response
from typing import List
from types import ModuleType

from models.arguments import ArgumentModel
from utils.logger import log_setup
from utils.request import AlphaVantageQuery


def main(source_args: argparse.Namespace):
    args: ArgumentModel = ArgumentModel(source_args=source_args)
    logger.info(f"Activating [{args.alpha_vantage_function}] function.")
    alpha_vantage_function_module: ModuleType = importlib.import_module(
        f"functions.{args.alpha_vantage_function}"
    )
    alpha_vantage_function = alpha_vantage_function_module.AlphaVantageFunction()

    query: AlphaVantageQuery = AlphaVantageQuery(
        api_key=args.api_key, alpha_vantage_function=args.alpha_vantage_function
    )
    response: Response = query.get_request(params=alpha_vantage_function.params)
    # To refactor
    data = response.json()
    with open("dummy.json", "w", encoding="utf-8") as dummy_file:
        json.dump(data, dummy_file, indent=4)


if __name__ == "__main__":
    # Setting up directory using pathlib module
    PARENT_DIR: Path = Path(__file__).resolve().parent
    # Logger setup
    logger: logging.Logger = log_setup(
        parent_dir=f"{PARENT_DIR}",
        log_filename=f"{PARENT_DIR.name}",
        logger_level="INFO",
    )
    # Get supported functions
    loaded_functions: List[Path] = Path(f"{PARENT_DIR}/functions").iterdir()
    functions_to_ignore: set = {"__pycache__", "__init__.py"}
    available_functions: List[str] = [
        str(functions.name).lower()
        for functions in loaded_functions
        if functions not in functions_to_ignore
    ]

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
        choices=available_functions,
        type=str,
        required=True,
        help="Specify the supported alpha vantage function.",
    )
    main(parser.parse_args())
