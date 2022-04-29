import argparse
import logging
import pandas as pd
import time

from pathlib import Path
from requests.models import Response
from typing import List


from utils.logger import log_setup
from utils.pathfinder import dir_builder, csv_path_builder
from utils.request import AlphaVantageQuery

ROOT_URL = "https://www.alphavantage.co/query"


def main(args: argparse.Namespace):
    dir_builder(output_path=OUTPUT_DIR)
    csv_file_path: Path = csv_path_builder(
        output_dir=OUTPUT_DIR, alpha_vantage_function="OVERVIEW", symbol="COMBINED",
    )
    tech_companies_csv_path: Path = Path(
        f"{PARENT_DIR}/sample_data/nasdad_tech_companies.csv"
    )
    tech_companies_df: pd.DataFrame = pd.read_csv(tech_companies_csv_path)
    tech_companies_symbols: pd.Series = tech_companies_df["Symbol"]

    query: AlphaVantageQuery = AlphaVantageQuery(api_key=args.api_key)
    params: dict = {"function": "OVERVIEW"}
    combined_overview: List[str] = []
    counter: int = 1
    for symbol in tech_companies_symbols:
        if counter == 400:
            query.switch_key(api_key="4IDU6B77MSDP3P7P")
        params.update(
            {"symbol": symbol,}
        )
        time.sleep(15)
        logger.info(f"Extracting symbol {counter} - [{symbol}].")
        response: Response = query.get_request(params=params)
        combined_overview.append(transform_json_to_list(response.json()))
        counter += 1

    columns_name: list = [
        "Symbol",
        "AssetType",
        "Name",
        "Description",
        "CIK",
        "Exchange",
        "Currency",
        "Country",
        "Sector",
        "Industry",
        "Address",
        "FiscalYearEnd",
        "LatestQuarter",
        "MarketCapitalization",
        "EBITDA",
        "PERatio",
        "PEGRatio",
        "BookValue",
        "DividendPerShare",
        "DividendYield",
        "EPS",
        "RevenuePerShareTTM",
        "ProfitMargin",
        "OperatingMarginTTM",
        "ReturnOnAssetsTTM",
        "ReturnOnEquityTTM",
        "RevenueTTM",
        "GrossProfitTTM",
        "DilutedEPSTTM",
        "QuarterlyEarningsGrowthYOY",
        "QuarterlyRevenueGrowthYOY",
        "AnalystTargetPrice",
        "TrailingPE",
        "ForwardPE",
        "PriceToSalesRatioTTM",
        "PriceToBookRatio",
        "EVToRevenue",
        "EVToEBITDA",
        "Beta",
        "52WeekHigh",
        "52WeekLow",
        "50DayMovingAverage",
        "200DayMovingAverage",
        "SharesOutstanding",
        "DividendDate",
        "ExDividendDate",
    ]
    df_final: pd.DataFrame = pd.DataFrame(combined_overview, columns=columns_name)
    logger.info(f"Exporting json data to csv file to path - [{csv_file_path}].")
    df_final.to_csv(csv_file_path, index=False, header=True)


def transform_json_to_list(json_data: dict) -> pd.DataFrame:
    logger.info("Normalizing, flattening, json data.")
    Symbol: str = json_data.get("Symbol")
    AssetType: str = json_data.get("AssetType")
    Name: str = json_data.get("Name")
    Description: str = json_data.get("Description")
    CIK: str = json_data.get("CIK")
    Exchange: str = json_data.get("Exchange")
    Currency: str = json_data.get("Currency")
    Country: str = json_data.get("Country")
    Sector: str = json_data.get("Sector")
    Industry: str = json_data.get("Industry")
    Address: str = json_data.get("Address")
    FiscalYearEnd: str = json_data.get("FiscalYearEnd")
    LatestQuarter: str = json_data.get("LatestQuarter")
    MarketCapitalization: str = json_data.get("MarketCapitalization")
    EBITDA: str = json_data.get("EBITDA")
    PERatio: str = json_data.get("PERatio")
    PEGRatio: str = json_data.get("PEGRatio")
    BookValue: str = json_data.get("BookValue")
    DividendPerShare: str = json_data.get("DividendPerShare")
    DividendYield: str = json_data.get("DividendYield")
    EPS: str = json_data.get("EPS")
    RevenuePerShareTTM: str = json_data.get("RevenuePerShareTTM")
    ProfitMargin: str = json_data.get("ProfitMargin")
    OperatingMarginTTM: str = json_data.get("OperatingMarginTTM")
    ReturnOnAssetsTTM: str = json_data.get("ReturnOnAssetsTTM")
    ReturnOnEquityTTM: str = json_data.get("ReturnOnEquityTTM")
    RevenueTTM: str = json_data.get("RevenueTTM")
    GrossProfitTTM: str = json_data.get("GrossProfitTTM")
    DilutedEPSTTM: str = json_data.get("DilutedEPSTTM")
    QuarterlyEarningsGrowthYOY: str = json_data.get("QuarterlyEarningsGrowthYOY")
    QuarterlyRevenueGrowthYOY: str = json_data.get("QuarterlyRevenueGrowthYOY")
    AnalystTargetPrice: str = json_data.get("AnalystTargetPrice")
    TrailingPE: str = json_data.get("TrailingPE")
    ForwardPE: str = json_data.get("ForwardPE")
    PriceToSalesRatioTTM: str = json_data.get("PriceToSalesRatioTTM")
    PriceToBookRatio: str = json_data.get("PriceToBookRatio")
    EVToRevenue: str = json_data.get("EVToRevenue")
    EVToEBITDA: str = json_data.get("EVToEBITDA")
    Beta: str = json_data.get("Beta")
    FiftyTwoWeekHigh: str = json_data.get("52WeekHigh")
    FiftyTwoWeekLow: str = json_data.get("52WeekLow")
    FiftyDayMovingAverage: str = json_data.get("50DayMovingAverage")
    TwoHundredDayMovingAverage: str = json_data.get("200DayMovingAverage")
    SharesOutstanding: str = json_data.get("SharesOutstanding")
    DividendDate: str = json_data.get("DividendDate")
    ExDividendDate: str = json_data.get("ExDividendDate")

    return [
        Symbol,
        AssetType,
        Name,
        Description,
        CIK,
        Exchange,
        Currency,
        Country,
        Sector,
        Industry,
        Address,
        FiscalYearEnd,
        LatestQuarter,
        MarketCapitalization,
        EBITDA,
        PERatio,
        PEGRatio,
        BookValue,
        DividendPerShare,
        DividendYield,
        EPS,
        RevenuePerShareTTM,
        ProfitMargin,
        OperatingMarginTTM,
        ReturnOnAssetsTTM,
        ReturnOnEquityTTM,
        RevenueTTM,
        GrossProfitTTM,
        DilutedEPSTTM,
        QuarterlyEarningsGrowthYOY,
        QuarterlyRevenueGrowthYOY,
        AnalystTargetPrice,
        TrailingPE,
        ForwardPE,
        PriceToSalesRatioTTM,
        PriceToBookRatio,
        EVToRevenue,
        EVToEBITDA,
        Beta,
        FiftyTwoWeekHigh,
        FiftyTwoWeekLow,
        FiftyDayMovingAverage,
        TwoHundredDayMovingAverage,
        SharesOutstanding,
        DividendDate,
        ExDividendDate,
    ]


if __name__ == "__main__":
    # Setting up directory using pathlib module
    PARENT_DIR: Path = Path(__file__).resolve().parents[1]
    OUTPUT_DIR: Path = Path(f"{PARENT_DIR}/alphavantage_download/output")
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
    main(parser.parse_args())
