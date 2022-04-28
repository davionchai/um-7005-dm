import logging
import pandas as pd

from pathlib import Path
from typing import Dict

from constants.datatype import DataType
from utils.strenum import StrEnum

logger: logging.Logger = logging.getLogger(__name__)


class OutputSize(StrEnum):
    FULL = "full"  # Returns full length data
    COMPACT = "compact"  # Returns latest 100 entries


class AlphaVantageFunction:
    def __init__(self, **kwargs) -> None:
        symbol: str = kwargs.get("symbol", None)
        self.data_type: DataType = DataType.JSON
        self.params: dict = {
            "outputsize": OutputSize.FULL,
            "datatype": self.data_type,
            "symbol": symbol,
        }

    def transform_json(self, json_data: dict) -> pd.DataFrame:
        json_metadata: dict = json_data.get("Meta Data")
        json_time_data: Dict[str, dict] = json_data.get("Time Series (Daily)")
        logger.info("Normalizing, flattening, json data.")
        symbol: str = json_metadata.get("2. Symbol")
        last_refreshed: str = json_metadata.get("3. Last Refreshed")
        output_size: str = json_metadata.get("4. Output Size")
        timezone: str = json_metadata.get("5. Time Zone")
        open: str
        high: str
        low: str
        close: str
        volume: str
        flatten_time_data: list = []

        for timestamp, time_data in json_time_data.items():
            open = time_data.get("1. open")
            high = time_data.get("2. high")
            low = time_data.get("3. low")
            close = time_data.get("4. close")
            volume = time_data.get("5. volume")
            flatten_time_data.append(
                [
                    symbol,
                    last_refreshed,
                    output_size,
                    timezone,
                    timestamp,
                    open,
                    high,
                    low,
                    close,
                    volume,
                ]
            )

        columns_name: list = [
            "symbol",
            "last_refreshed",
            "output_size",
            "timezone",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
        return pd.DataFrame(flatten_time_data, columns=columns_name)

    def export_df_to_csv(self, df: pd.DataFrame, csv_file_path: Path):
        logger.info(f"Exporting json data to csv file to path - [{csv_file_path}].")
        df.to_csv(csv_file_path, index=False, header=True)
