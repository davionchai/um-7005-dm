from utils.strenum import StrEnum


class OutputSize(StrEnum):
    FULL = "full"  # Returns full length data
    COMPACT = "compact"  # Returns latest 100 entries


class DataType(StrEnum):
    JSON = "json"
    CSV = "csv"


class AlphaVantageFunction:
    def __init__(self, **kwargs) -> None:
        stock: str = kwargs.get("stock", None)
        self.params: dict = {
            "outputsize": OutputSize.FULL,
            "datatype": DataType.JSON,
            "symbol": stock,
        }
