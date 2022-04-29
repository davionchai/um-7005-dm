import argparse
import csv
import importlib
import logging
import pandas as pd

from pathlib import Path
from requests.models import Response
from typing import List
from types import ModuleType

from constants.datatype import DataType
from models.arguments import ArgumentModel
from utils.logger import log_setup
from utils.pathfinder import dir_builder, csv_path_builder
from utils.request import AlphaVantageQuery


def main(source_args: argparse.Namespace):
    args: ArgumentModel = ArgumentModel(source_args=source_args)
    logger.info(f"Activating [{args.alpha_vantage_function}] function.")
    alpha_vantage_function_module: ModuleType = importlib.import_module(
        f"functions.{args.alpha_vantage_function}"
    )
    alpha_vantage_function = alpha_vantage_function_module.AlphaVantageFunction(
        symbol=args.symbol, alpha_vantage_function=args.alpha_vantage_function
    )

    query: AlphaVantageQuery = AlphaVantageQuery(api_key=args.api_key)
    response: Response = query.get_request(params=alpha_vantage_function.params)

    csv_file_path: Path = csv_path_builder(
        output_dir=OUTPUT_DIR,
        alpha_vantage_function=args.alpha_vantage_function,
        symbol=args.symbol,
    )
    dir_builder(output_path=OUTPUT_DIR)

    if alpha_vantage_function.data_type == DataType.JSON:
        json_data: dict = response.json()
        # json.dump(json_data, csv_file, indent=4)
        df: pd.DataFrame = alpha_vantage_function.transform_json(json_data=json_data)
        alpha_vantage_function.export_df_to_csv(df=df, csv_file_path=csv_file_path)
    elif alpha_vantage_function.data_type == DataType.CSV:
        with open(csv_file_path, "w", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            for line in response.iter_lines():
                writer.writerow(line.decode("utf-8").split(","))


if __name__ == "__main__":
    # Setting up directory using pathlib module
    PARENT_DIR: Path = Path(__file__).resolve().parent
    OUTPUT_DIR: Path = Path(f"{PARENT_DIR}/output")
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
        f"{functions.stem}".lower()
        for functions in loaded_functions
        if functions.name not in functions_to_ignore
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
        "-s",
        "--symbol",
        type=str,
        required=True,
        help="Specify the target stock symbol name.",
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
