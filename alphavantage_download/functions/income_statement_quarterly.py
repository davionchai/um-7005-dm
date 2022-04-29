import logging
import pandas as pd

from pathlib import Path
from typing import Dict, List

from constants.datatype import DataType

logger: logging.Logger = logging.getLogger(__name__)


class AlphaVantageFunction:
    def __init__(self, **kwargs) -> None:
        symbol: str = kwargs.get("symbol", None)
        alpha_vantage_function: str = "INCOME_STATEMENT"
        self.data_type: DataType = DataType.JSON
        self.params: dict = {
            "symbol": symbol,
            "function": alpha_vantage_function,
        }

    def transform_json(self, json_data: dict) -> pd.DataFrame:
        symbol: dict = json_data.get("symbol")
        json_annual_reports: Dict[str, list] = json_data.get("quarterlyReports")
        logger.info("Normalizing, flattening, json data.")
        fiscalDateEnding: str
        reportedCurrency: str
        grossProfit: str
        totalRevenue: str
        costOfRevenue: str
        costofGoodsAndServicesSold: str
        operatingIncome: str
        sellingGeneralAndAdministrative: str
        researchAndDevelopment: str
        operatingExpenses: str
        investmentIncomeNet: str
        netInterestIncome: str
        interestIncome: str
        interestExpense: str
        nonInterestIncome: str
        otherNonOperatingIncome: str
        depreciation: str
        depreciationAndAmortization: str
        incomeBeforeTax: str
        incomeTaxExpense: str
        interestAndDebtExpense: str
        netIncomeFromContinuingOperations: str
        comprehensiveIncomeNetOfTax: str
        ebit: str
        ebitda: str
        netIncome: str
        flatten_time_data: list = []

        for annual_report in json_annual_reports:
            fiscalDateEnding = annual_report.get("fiscalDateEnding")
            reportedCurrency = annual_report.get("reportedCurrency")
            grossProfit = annual_report.get("grossProfit")
            totalRevenue = annual_report.get("totalRevenue")
            costOfRevenue = annual_report.get("costOfRevenue")
            costofGoodsAndServicesSold = annual_report.get("costofGoodsAndServicesSold")
            operatingIncome = annual_report.get("operatingIncome")
            sellingGeneralAndAdministrative = annual_report.get(
                "sellingGeneralAndAdministrative"
            )
            researchAndDevelopment = annual_report.get("researchAndDevelopment")
            operatingExpenses = annual_report.get("operatingExpenses")
            investmentIncomeNet = annual_report.get("investmentIncomeNet")
            netInterestIncome = annual_report.get("netInterestIncome")
            interestIncome = annual_report.get("interestIncome")
            interestExpense = annual_report.get("interestExpense")
            nonInterestIncome = annual_report.get("nonInterestIncome")
            otherNonOperatingIncome = annual_report.get("otherNonOperatingIncome")
            depreciation = annual_report.get("depreciation")
            depreciationAndAmortization = annual_report.get(
                "depreciationAndAmortization"
            )
            incomeBeforeTax = annual_report.get("incomeBeforeTax")
            incomeTaxExpense = annual_report.get("incomeTaxExpense")
            interestAndDebtExpense = annual_report.get("interestAndDebtExpense")
            netIncomeFromContinuingOperations = annual_report.get(
                "netIncomeFromContinuingOperations"
            )
            comprehensiveIncomeNetOfTax = annual_report.get(
                "comprehensiveIncomeNetOfTax"
            )
            ebit = annual_report.get("ebit")
            ebitda = annual_report.get("ebitda")
            netIncome = annual_report.get("netIncome")

            flatten_time_data.append(
                [
                    symbol,
                    fiscalDateEnding,
                    reportedCurrency,
                    grossProfit,
                    totalRevenue,
                    costOfRevenue,
                    costofGoodsAndServicesSold,
                    operatingIncome,
                    sellingGeneralAndAdministrative,
                    researchAndDevelopment,
                    operatingExpenses,
                    investmentIncomeNet,
                    netInterestIncome,
                    interestIncome,
                    interestExpense,
                    nonInterestIncome,
                    otherNonOperatingIncome,
                    depreciation,
                    depreciationAndAmortization,
                    incomeBeforeTax,
                    incomeTaxExpense,
                    interestAndDebtExpense,
                    netIncomeFromContinuingOperations,
                    comprehensiveIncomeNetOfTax,
                    ebit,
                    ebitda,
                    netIncome,
                ]
            )

        columns_name: list = [
            "symbol",
            "fiscalDateEnding",
            "reportedCurrency",
            "grossProfit",
            "totalRevenue",
            "costOfRevenue",
            "costofGoodsAndServicesSold",
            "operatingIncome",
            "sellingGeneralAndAdministrative",
            "researchAndDevelopment",
            "operatingExpenses",
            "investmentIncomeNet",
            "netInterestIncome",
            "interestIncome",
            "interestExpense",
            "nonInterestIncome",
            "otherNonOperatingIncome",
            "depreciation",
            "depreciationAndAmortization",
            "incomeBeforeTax",
            "incomeTaxExpense",
            "interestAndDebtExpense",
            "netIncomeFromContinuingOperations",
            "comprehensiveIncomeNetOfTax",
            "ebit",
            "ebitda",
            "netIncome",
        ]
        return pd.DataFrame(flatten_time_data, columns=columns_name)

    def export_df_to_csv(self, df: pd.DataFrame, csv_file_path: Path):
        logger.info(f"Exporting json data to csv file to path - [{csv_file_path}].")
        df.to_csv(csv_file_path, index=False, header=True)
