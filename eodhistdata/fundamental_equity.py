"""This class offers methods to extract fundamental equity data from EOD's output.

Equity data is labeled by type "Common Stock" in EOD's universe. The fundamental
equity data for common stock seems to always have the following fields:
* General
* Highlights
* Valuation
* SharesStats
* Technicals
* SplitsDividends
* Holders
* InsiderTransactions
* outstandingShares
* Earnings
* Financials

Some stocks have the additional fields 'AnalystRatings' and 'ESGScores'.
"""

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from typing import Union

from eodhistdata.constants import FundamentalDataTypes, FinancialStatementTypes, FUNDAMENTAL_DATA_TYPE_MAP


class AbstractFinancialData(ABC):
    def __init__(self, eod_fund_data_dict: dict, as_of_date: str = '', 
                 frequency: str = 'q'):
        self._data = eod_fund_data_dict
        self.frequency = frequency
        self.as_of_date = as_of_date

    @property
    @abstractmethod
    def statement_type(self):
        pass

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, freq):
        if freq not in ('q', 'y'):
            raise ValueError('Frequency must be quarterly ("q") or yearly ("y").')
        else:
            self._frequency = freq

    @property
    def frequency_eod(self):
        return 'quarterly' if self.frequency == 'q' else 'yearly'

    @property
    def statement_dict(self):
        return self._data['Financials'][self.statement_type][self.frequency_eod]

    @property
    def statement(self):
        return self.statement_dict.get(self.as_of_date, dict())
            
    @property
    def available_dates(self):
        return sorted(list(self.statement_dict.keys()))
        
    @property
    def as_of_date(self):
        return self._as_of_date
    
    @as_of_date.setter
    def as_of_date(self, aod):
        if not aod:
            if self.available_dates:
                self._as_of_date = max(self.available_dates)
            else:
                self._as_of_date = ''
        else:
            self._as_of_date = aod


class BalanceSheetData(AbstractFinancialData):
    # Implement abstract method
    @property    
    def statement_type(self):
        return 'Balance_Sheet'

    @property
    def accountsPayable(self) -> float:
        val = self.statement.get('accountsPayable', 0)
        return float(val) if val is not None else np.nan

    @property
    def accumulatedAmortization(self) -> float:
        val = self.statement.get('accumulatedAmortization', 0)
        return float(val) if val is not None else np.nan

    @property
    def accumulatedDepreciation(self) -> float:
        val = self.statement.get('accumulatedDepreciation', 0)
        return float(val) if val is not None else np.nan

    @property
    def accumulatedOtherComprehensiveIncome(self) -> float:
        val = self.statement.get('accumulatedOtherComprehensiveIncome', 0)
        return float(val) if val is not None else np.nan

    @property
    def additionalPaidInCapital(self) -> float:
        val = self.statement.get('additionalPaidInCapital', 0)
        return float(val) if val is not None else np.nan

    @property
    def capitalLeaseObligations(self) -> float:
        val = self.statement.get('capitalLeaseObligations', 0)
        return float(val) if val is not None else np.nan

    @property
    def capitalStock(self) -> float:
        val = self.statement.get('capitalStock', 0)
        return float(val) if val is not None else np.nan

    @property
    def capitalSurpluse(self) -> float:
        val = self.statement.get('capitalSurpluse', 0)
        return float(val) if val is not None else np.nan

    @property
    def cash(self) -> float:
        val = self.statement.get('cash', 0)
        return float(val) if val is not None else np.nan

    @property
    def cashAndEquivalents(self) -> float:
        val = self.statement.get('cashAndEquivalents', 0)
        return float(val) if val is not None else np.nan

    @property
    def cashAndShortTermInvestments(self) -> float:
        val = self.statement.get('cashAndShortTermInvestments', 0)
        return float(val) if val is not None else np.nan

    @property
    def commonStock(self) -> float:
        val = self.statement.get('commonStock', 0)
        return float(val) if val is not None else np.nan

    @property
    def commonStockSharesOutstanding(self) -> float:
        val = self.statement.get('commonStockSharesOutstanding', 0)
        return float(val) if val is not None else np.nan

    @property
    def commonStockTotalEquity(self) -> float:
        val = self.statement.get('commonStockTotalEquity', 0)
        return float(val) if val is not None else np.nan

    @property
    def currency_symbol(self) -> str:
        val = self.statement.get('currency_symbol', '')
        return val if val is not None else ''        

    @property
    def currentDeferredRevenue(self) -> float:
        val = self.statement.get('currentDeferredRevenue', 0)
        return float(val) if val is not None else np.nan

    @property
    def date(self) -> str:
        val = self.statement.get('date', '')
        return val if val is not None else ''        

    @property
    def deferredLongTermAssetCharges(self) -> float:
        val = self.statement.get('deferredLongTermAssetCharges', 0)
        return float(val) if val is not None else np.nan

    @property
    def deferredLongTermLiab(self) -> float:
        val = self.statement.get('deferredLongTermLiab', 0)
        return float(val) if val is not None else np.nan

    @property
    def earningAssets(self) -> float:
        val = self.statement.get('earningAssets', 0)
        return float(val) if val is not None else np.nan

    @property
    def filing_date(self) -> str:
        val = self.statement.get('filing_date', '')
        return val if val is not None else ''

    @property
    def goodWill(self) -> float:
        val = self.statement.get('goodWill', 0)
        return float(val) if val is not None else np.nan

    @property
    def intangibleAssets(self) -> float:
        val = self.statement.get('intangibleAssets', 0)
        return float(val) if val is not None else np.nan

    @property
    def inventory(self) -> float:
        val = self.statement.get('inventory', 0)
        return float(val) if val is not None else np.nan

    @property
    def liabilitiesAndStockholdersEquity(self) -> float:
        val = self.statement.get('liabilitiesAndStockholdersEquity', 0)
        return float(val) if val is not None else np.nan

    @property
    def longTermDebt(self) -> float:
        val = self.statement.get('longTermDebt', 0)
        return float(val) if val is not None else np.nan

    @property
    def longTermDebtTotal(self) -> float:
        val = self.statement.get('longTermDebtTotal', 0)
        return float(val) if val is not None else np.nan

    @property
    def longTermInvestments(self) -> float:
        val = self.statement.get('longTermInvestments', 0)
        return float(val) if val is not None else np.nan

    @property
    def negativeGoodwill(self) -> float:
        val = self.statement.get('negativeGoodwill', 0)
        return float(val) if val is not None else np.nan

    @property
    def netDebt(self) -> float:
        val = self.statement.get('netDebt', 0)
        return float(val) if val is not None else np.nan

    @property
    def netInvestedCapital(self) -> float:
        val = self.statement.get('netInvestedCapital', 0)
        return float(val) if val is not None else np.nan

    @property
    def netReceivables(self) -> float:
        val = self.statement.get('netReceivables', 0)
        return float(val) if val is not None else np.nan

    @property
    def netTangibleAssets(self) -> float:
        val = self.statement.get('netTangibleAssets', 0)
        return float(val) if val is not None else np.nan

    @property
    def netWorkingCapital(self) -> float:
        val = self.statement.get('netWorkingCapital', 0)
        return float(val) if val is not None else np.nan

    @property
    def nonCurrentAssetsTotal(self) -> float:
        val = self.statement.get('nonCurrentAssetsTotal', 0)
        return float(val) if val is not None else np.nan

    @property
    def nonCurrentLiabilitiesOther(self) -> float:
        val = self.statement.get('nonCurrentLiabilitiesOther', 0)
        return float(val) if val is not None else np.nan

    @property
    def nonCurrentLiabilitiesTotal(self) -> float:
        val = self.statement.get('nonCurrentLiabilitiesTotal', 0)
        return float(val) if val is not None else np.nan

    @property
    def nonCurrrentAssetsOther(self) -> float:
        val = self.statement.get('nonCurrrentAssetsOther', 0)
        return float(val) if val is not None else np.nan

    @property
    def noncontrollingInterestInConsolidatedEntity(self) -> float:
        val = self.statement.get('noncontrollingInterestInConsolidatedEntity', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherAssets(self) -> float:
        val = self.statement.get('otherAssets', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherCurrentAssets(self) -> float:
        val = self.statement.get('otherCurrentAssets', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherCurrentLiab(self) -> float:
        val = self.statement.get('otherCurrentLiab', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherLiab(self) -> float:
        val = self.statement.get('otherLiab', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherStockholderEquity(self) -> float:
        val = self.statement.get('otherStockholderEquity', 0)
        return float(val) if val is not None else np.nan

    @property
    def preferredStockRedeemable(self) -> float:
        val = self.statement.get('preferredStockRedeemable', 0)
        return float(val) if val is not None else np.nan

    @property
    def preferredStockTotalEquity(self) -> float:
        val = self.statement.get('preferredStockTotalEquity', 0)
        return float(val) if val is not None else np.nan

    @property
    def propertyPlantAndEquipmentGross(self) -> float:
        val = self.statement.get('propertyPlantAndEquipmentGross', 0)
        return float(val) if val is not None else np.nan

    @property
    def propertyPlantAndEquipmentNet(self) -> float:
        val = self.statement.get('propertyPlantAndEquipmentNet', 0)
        return float(val) if val is not None else np.nan

    @property
    def propertyPlantEquipment(self) -> float:
        val = self.statement.get('propertyPlantEquipment', 0)
        return float(val) if val is not None else np.nan

    @property
    def retainedEarnings(self) -> float:
        val = self.statement.get('retainedEarnings', 0)
        return float(val) if val is not None else np.nan

    @property
    def retainedEarningsTotalEquity(self) -> float:
        val = self.statement.get('retainedEarningsTotalEquity', 0)
        return float(val) if val is not None else np.nan

    @property
    def shortLongTermDebt(self) -> float:
        val = self.statement.get('shortLongTermDebt', 0)
        return float(val) if val is not None else np.nan

    @property
    def shortLongTermDebtTotal(self) -> float:
        val = self.statement.get('shortLongTermDebtTotal', 0)
        return float(val) if val is not None else np.nan

    @property
    def shortTermDebt(self) -> float:
        val = self.statement.get('shortTermDebt', 0)
        return float(val) if val is not None else np.nan

    @property
    def shortTermInvestments(self) -> float:
        val = self.statement.get('shortTermInvestments', 0)
        return float(val) if val is not None else np.nan

    @property
    def temporaryEquityRedeemableNoncontrollingInterests(self) -> float:
        val = self.statement.get('temporaryEquityRedeemableNoncontrollingInterests', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalAssets(self) -> float:
        val = self.statement.get('totalAssets', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalCurrentAssets(self) -> float:
        val = self.statement.get('totalCurrentAssets', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalCurrentLiabilities(self) -> float:
        val = self.statement.get('totalCurrentLiabilities', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalLiab(self) -> float:
        val = self.statement.get('totalLiab', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalPermanentEquity(self) -> float:
        val = self.statement.get('totalPermanentEquity', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalStockholderEquity(self) -> float:
        val = self.statement.get('totalStockholderEquity', 0)
        return float(val) if val is not None else np.nan

    @property
    def treasuryStock(self) -> float:
        val = self.statement.get('treasuryStock', 0)
        return float(val) if val is not None else np.nan

    @property
    def warrants(self) -> float:
        val = self.statement.get('warrants', 0)
        return float(val) if val is not None else np.nan


class IncomeStatementData(AbstractFinancialData):
    # Implement abstract method
    @property    
    def statement_type(self):
        return 'Income_Statement'

    @property
    def NOPAT(self) -> float:
        return self.ebit * (1 - self.tax_rate)

    @property
    def tax_rate(self):
        return self.incomeTaxExpense / (1e-10 + self.incomeBeforeTax)

    @property
    def costOfRevenue(self) -> float:
        val = self.statement.get('costOfRevenue', 0)
        return float(val) if val is not None else np.nan

    @property
    def currency_symbol(self) -> str:
        val = self.statement.get('currency_symbol', '')
        return val if val is not None else ''        

    @property
    def date(self) -> str:
        val = self.statement.get('date', '')
        return val if val is not None else ''        

    @property
    def depreciationAndAmortization(self) -> float:
        val = self.statement.get('depreciationAndAmortization', 0)
        return float(val) if val is not None else np.nan

    @property
    def discontinuedOperations(self) -> float:
        val = self.statement.get('discontinuedOperations', 0)
        return float(val) if val is not None else np.nan

    @property
    def ebit(self) -> float:
        val = self.statement.get('ebit', 0)
        return float(val) if val is not None else np.nan

    @property
    def ebitda(self) -> float:
        val = self.statement.get('ebitda', 0)
        return float(val) if val is not None else np.nan

    @property
    def effectOfAccountingCharges(self) -> float:
        val = self.statement.get('effectOfAccountingCharges', 0)
        return float(val) if val is not None else np.nan

    @property
    def extraordinaryItems(self) -> float:
        val = self.statement.get('extraordinaryItems', 0)
        return float(val) if val is not None else np.nan

    @property
    def filing_date(self) -> str:
        val = self.statement.get('filing_date', '')
        return val if val is not None else ''        

    @property
    def grossProfit(self) -> float:
        val = self.statement.get('grossProfit', 0)
        return float(val) if val is not None else np.nan

    @property
    def incomeBeforeTax(self) -> float:
        val = self.statement.get('incomeBeforeTax', 0)
        return float(val) if val is not None else np.nan

    @property
    def incomeTaxExpense(self) -> float:
        val = self.statement.get('incomeTaxExpense', 0)
        return float(val) if val is not None else np.nan

    @property
    def interestExpense(self) -> float:
        val = self.statement.get('interestExpense', 0)
        return float(val) if val is not None else np.nan

    @property
    def interestIncome(self) -> float:
        val = self.statement.get('interestIncome', 0)
        return float(val) if val is not None else np.nan

    @property
    def minorityInterest(self) -> float:
        val = self.statement.get('minorityInterest', 0)
        return float(val) if val is not None else np.nan

    @property
    def netIncome(self) -> float:
        val = self.statement.get('netIncome', 0)
        return float(val) if val is not None else np.nan

    @property
    def netIncomeApplicableToCommonShares(self) -> float:
        val = self.statement.get('netIncomeApplicableToCommonShares', 0)
        return float(val) if val is not None else np.nan

    @property
    def netIncomeFromContinuingOps(self) -> float:
        val = self.statement.get('netIncomeFromContinuingOps', 0)
        return float(val) if val is not None else np.nan

    @property
    def netInterestIncome(self) -> float:
        val = self.statement.get('netInterestIncome', 0)
        return float(val) if val is not None else np.nan

    @property
    def nonOperatingIncomeNetOther(self) -> float:
        val = self.statement.get('nonOperatingIncomeNetOther', 0)
        return float(val) if val is not None else np.nan

    @property
    def nonRecurring(self) -> float:
        val = self.statement.get('nonRecurring', 0)
        return float(val) if val is not None else np.nan

    @property
    def operatingIncome(self) -> float:
        val = self.statement.get('operatingIncome', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherItems(self) -> float:
        val = self.statement.get('otherItems', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherOperatingExpenses(self) -> float:
        val = self.statement.get('otherOperatingExpenses', 0)
        return float(val) if val is not None else np.nan

    @property
    def preferredStockAndOtherAdjustments(self) -> float:
        val = self.statement.get('preferredStockAndOtherAdjustments', 0)
        return float(val) if val is not None else np.nan

    @property
    def reconciledDepreciation(self) -> float:
        val = self.statement.get('reconciledDepreciation', 0)
        return float(val) if val is not None else np.nan

    @property
    def researchDevelopment(self) -> float:
        val = self.statement.get('researchDevelopment', 0)
        return float(val) if val is not None else np.nan

    @property
    def sellingAndMarketingExpenses(self) -> float:
        val = self.statement.get('sellingAndMarketingExpenses', 0)
        return float(val) if val is not None else np.nan

    @property
    def sellingGeneralAdministrative(self) -> float:
        val = self.statement.get('sellingGeneralAdministrative', 0)
        return float(val) if val is not None else np.nan

    @property
    def taxProvision(self) -> float:
        val = self.statement.get('taxProvision', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalOperatingExpenses(self) -> float:
        val = self.statement.get('totalOperatingExpenses', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalOtherIncomeExpenseNet(self) -> float:
        val = self.statement.get('totalOtherIncomeExpenseNet', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalRevenue(self) -> float:
        val = self.statement.get('totalRevenue', 0)
        return float(val) if val is not None else np.nan    


class CashFlowStatementData(AbstractFinancialData):
    # Implement abstract method
    @property    
    def statement_type(self):
        return 'Cash_Flow'

    @property
    def beginPeriodCashFlow(self) -> float:
        val = self.statement.get('beginPeriodCashFlow', 0)
        return float(val) if val is not None else np.nan

    @property
    def capitalExpenditures(self) -> float:
        val = self.statement.get('capitalExpenditures', 0)
        return float(val) if val is not None else np.nan

    @property
    def cashAndCashEquivalentsChanges(self) -> float:
        val = self.statement.get('cashAndCashEquivalentsChanges', 0)
        return float(val) if val is not None else np.nan

    @property
    def cashFlowsOtherOperating(self) -> float:
        val = self.statement.get('cashFlowsOtherOperating', 0)
        return float(val) if val is not None else np.nan

    @property
    def changeInCash(self) -> float:
        val = self.statement.get('changeInCash', 0)
        return float(val) if val is not None else np.nan

    @property
    def changeInWorkingCapital(self) -> float:
        val = self.statement.get('changeInWorkingCapital', 0)
        return float(val) if val is not None else np.nan

    @property
    def changeReceivables(self) -> float:
        val = self.statement.get('changeReceivables', 0)
        return float(val) if val is not None else np.nan

    @property
    def changeToAccountReceivables(self) -> float:
        val = self.statement.get('changeToAccountReceivables', 0)
        return float(val) if val is not None else np.nan

    @property
    def changeToInventory(self) -> float:
        val = self.statement.get('changeToInventory', 0)
        return float(val) if val is not None else np.nan

    @property
    def changeToLiabilities(self) -> float:
        val = self.statement.get('changeToLiabilities', 0)
        return float(val) if val is not None else np.nan

    @property
    def changeToNetincome(self) -> float:
        val = self.statement.get('changeToNetincome', 0)
        return float(val) if val is not None else np.nan

    @property
    def changeToOperatingActivities(self) -> float:
        val = self.statement.get('changeToOperatingActivities', 0)
        return float(val) if val is not None else np.nan

    @property
    def currency_symbol(self) -> str:
        val = self.statement.get('currency_symbol', '')
        return val if val is not None else ''        

    @property
    def date(self) -> str:
        val = self.statement.get('date', '')
        return val if val is not None else ''        

    @property
    def depreciation(self) -> float:
        val = self.statement.get('depreciation', 0)
        return float(val) if val is not None else np.nan

    @property
    def dividendsPaid(self) -> float:
        val = self.statement.get('dividendsPaid', 0)
        return float(val) if val is not None else np.nan

    @property
    def endPeriodCashFlow(self) -> float:
        val = self.statement.get('endPeriodCashFlow', 0)
        return float(val) if val is not None else np.nan

    @property
    def exchangeRateChanges(self) -> float:
        val = self.statement.get('exchangeRateChanges', 0)
        return float(val) if val is not None else np.nan

    @property
    def filing_date(self) -> str:
        val = self.statement.get('filing_date', '')
        return val if val is not None else ''        

    @property
    def freeCashFlow(self) -> float:
        val = self.statement.get('freeCashFlow', 0)
        return float(val) if val is not None else np.nan

    @property
    def investments(self) -> float:
        val = self.statement.get('investments', 0)
        return float(val) if val is not None else np.nan

    @property
    def issuanceOfCapitalStock(self) -> float:
        val = self.statement.get('issuanceOfCapitalStock', 0)
        return float(val) if val is not None else np.nan

    @property
    def netBorrowings(self) -> float:
        val = self.statement.get('netBorrowings', 0)
        return float(val) if val is not None else np.nan

    @property
    def netIncome(self) -> float:
        val = self.statement.get('netIncome', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherCashflowsFromFinancingActivities(self) -> float:
        val = self.statement.get('otherCashflowsFromFinancingActivities', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherCashflowsFromInvestingActivities(self) -> float:
        val = self.statement.get('otherCashflowsFromInvestingActivities', 0)
        return float(val) if val is not None else np.nan

    @property
    def otherNonCashItems(self) -> float:
        val = self.statement.get('otherNonCashItems', 0)
        return float(val) if val is not None else np.nan

    @property
    def salePurchaseOfStock(self) -> float:
        val = self.statement.get('salePurchaseOfStock', 0)
        return float(val) if val is not None else np.nan

    @property
    def stockBasedCompensation(self) -> float:
        val = self.statement.get('stockBasedCompensation', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalCashFromFinancingActivities(self) -> float:
        val = self.statement.get('totalCashFromFinancingActivities', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalCashFromOperatingActivities(self) -> float:
        val = self.statement.get('totalCashFromOperatingActivities', 0)
        return float(val) if val is not None else np.nan

    @property
    def totalCashflowsFromInvestingActivities(self) -> float:
        val = self.statement.get('totalCashflowsFromInvestingActivities', 0)
        return float(val) if val is not None else np.nan



class FundamentalEquityGeneral(object):
    def __init__(self, eod_fund_data_dict: dict):
        self._data = eod_fund_data_dict

    @property
    def Code(self):
        return self._data['General']['Code']

    @property
    def Type(self):
        return self._data['General']['Type']

    @property
    def Name(self):
        return self._data['General']['Name']

    @property
    def Exchange(self):
        return self._data['General']['Exchange']

    @property
    def CurrencyCode(self):
        return self._data['General']['CurrencyCode']

    @property
    def CurrencyName(self):
        return self._data['General']['CurrencyName']

    @property
    def CurrencySymbol(self):
        return self._data['General']['CurrencySymbol']

    @property
    def CountryName(self):
        return self._data['General']['CountryName']

    @property
    def CountryISO(self):
        return self._data['General']['CountryISO']

    @property
    def ISIN(self):
        return self._data['General']['ISIN']

    @property
    def LEI(self):
        return self._data['General']['LEI']

    @property
    def PrimaryTicker(self):
        return self._data['General']['PrimaryTicker']

    @property
    def CUSIP(self):
        return self._data['General']['CUSIP']

    @property
    def CIK(self):
        return self._data['General']['CIK']

    @property
    def EmployerIdNumber(self):
        return self._data['General']['EmployerIdNumber']

    @property
    def FiscalYearEnd(self):
        return self._data['General']['FiscalYearEnd']

    @property
    def IPODate(self):
        return self._data['General']['IPODate']

    @property
    def InternationalDomestic(self):
        return self._data['General']['InternationalDomestic']

    @property
    def Sector(self):
        return self._data['General']['Sector']

    @property
    def Industry(self):
        return self._data['General']['Industry']

    @property
    def GicSector(self):
        return self._data['General']['GicSector']

    @property
    def GicGroup(self):
        return self._data['General']['GicGroup']

    @property
    def GicIndustry(self):
        return self._data['General']['GicIndustry']

    @property
    def GicSubIndustry(self):
        return self._data['General']['GicSubIndustry']

    @property
    def HomeCategory(self):
        return self._data['General']['HomeCategory']

    @property
    def IsDelisted(self):
        return self._data['General']['IsDelisted']

    @property
    def Description(self):
        return self._data['General']['Description']

    @property
    def Address(self):
        return self._data['General']['Address']

    @property
    def AddressData(self):
        return self._data['General']['AddressData']

    @property
    def Listings(self):
        return self._data['General']['Listings']

    @property
    def Officers(self):
        return self._data['General']['Officers']

    @property
    def Phone(self):
        return self._data['General']['Phone']

    @property
    def WebURL(self):
        return self._data['General']['WebURL']

    @property
    def LogoURL(self):
        return self._data['General']['LogoURL']

    @property
    def FullTimeEmployees(self):
        return self._data['General']['FullTimeEmployees']

    @property
    def UpdatedAt(self):
        return self._data['General']['UpdatedAt']


class FundamentalEquitySnapshot(FundamentalEquityGeneral):
    def __init__(self, eod_fund_data_dict: dict, as_of_date: str = '', frequency: str = 'q'):
        super(FundamentalEquitySnapshot, self).__init__(eod_fund_data_dict)
            
        self._frequency = frequency
        self.balance_sheet = BalanceSheetData(eod_fund_data_dict, as_of_date=as_of_date,
                                              frequency=frequency)
        self.income_statement = IncomeStatementData(eod_fund_data_dict, as_of_date=as_of_date,
                                                    frequency=frequency)
        self.cash_flow_statement = CashFlowStatementData(eod_fund_data_dict, as_of_date=as_of_date,
                                                         frequency=frequency)

        self._earnings_ts = None
        self._shares_ts = None

        if not as_of_date:
            if self.common_financial_dates:
                self.as_of_date = max(self.common_financial_dates)
            else:
                self.as_of_date = ''
        else:
            self.as_of_date = as_of_date

    @property
    def as_of_date(self):
        return self._as_of_date
    
    @as_of_date.setter
    def as_of_date(self, aod):
        if not aod:
            if self.common_financial_dates:
                self._as_of_date = max(self.common_financial_dates)
            else:
                self._as_of_date = ''
        else:
            self._as_of_date = aod

        self.balance_sheet.as_of_date = self.as_of_date
        self.income_statement.as_of_date = self.as_of_date
        self.cash_flow_statement.as_of_date = self.as_of_date

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, freq):
        self._frequency = freq
        self.balance_sheet.frequency = freq
        self.income_statement.frequency = freq
        self.cash_flow_statement.frequency = freq
        self._shares_ts = None

    @property
    def frequency_eod(self):
        return 'quarterly' if self.frequency == 'q' else 'yearly'

    @property
    def common_financial_dates(self):
        bal_dates = set(self.balance_sheet.available_dates)
        inc_dates = set(self.income_statement.available_dates)
        return sorted(list(bal_dates.intersection(inc_dates)))
    
    @property
    def filing_date(self) -> str:
        return max(self.income_statement.filing_date, 
                   self.balance_sheet.filing_date)
    
    @property
    def MarketCap(self) -> float:
        raise NotImplementedError()
        
    @property
    def ReturnOnEquity(self) -> float:
        net_income = self.income_statement.netIncome
        total_equity = self.balance_sheet.totalStockholderEquity
        return net_income / (1e-10 + total_equity)

    @property
    def ReturnOnAssets(self) -> float:
        net_income = self.income_statement.netIncome
        total_assets = self.balance_sheet.totalAssets
        return net_income / (1e-10 + total_assets)

    @property
    def ROIC(self) -> float:
        return  self.income_statement.NOPAT / (1e-10 + self.balance_sheet.netInvestedCapital)

    @property
    def earnings_ts(self):
        if self._earnings_ts is None:
            df = pd.DataFrame(self._data['Earnings']['History']).T
            df.index = pd.DatetimeIndex(df.index)
            if not df.empty:
                df.drop('date', axis=1, inplace=True)
                df.index.name = 'date'
                df.sort_index(inplace=True)
            self._earnings_ts = df
        return self._earnings_ts  

    @property
    def eps_actual_ts(self):
        if self.earnings_ts.empty:
            return pd.Series([], dtype=np.float32)
        else:
            return self.earnings_ts['epsActual']

    @property
    def eps_estimate_ts(self):
        if self.earnings_ts.empty:
            return pd.Series([], dtype=np.float32)
        else:
            return self.earnings_ts['epsEstimate']

    @property
    def shares_ts(self):
        max_change = 0.05
        if self._shares_ts is None:
            if self.frequency == 'q':
                freq_str = 'quarterly'
            else:
                freq_str = 'annual'

            df = pd.DataFrame(self._data['outstandingShares'][freq_str].values())
            if df.empty:
                self._shares_ts = pd.DataFrame()
            else:
                # Clean up the raw data, and sort by date
                df.drop(['date', 'sharesMln'], axis=1, inplace=True)
                df.set_index('dateFormatted', inplace=True)
                df.index = pd.DatetimeIndex(df.index)
                df.index.name = 'date'
                df.sort_index(inplace=True)

                ##################################
                # Prepare to remove any bad points
                shares = df['shares'].copy()
                idx_zero = np.isclose(shares.values, 0)
                tol = 1
                log_arg = shares / (tol + shares.shift(1))
                log_arg[idx_zero] = np.nan
                rtns = np.log(log_arg)
                
                # Find jumps
                rtn_abs_avg = (np.abs(rtns) + np.abs(rtns.shift(-1))) / 2
                rtn_abs_sum = np.abs(rtns + rtns.shift(-1))
                idx_bad = rtn_abs_sum < rtn_abs_avg / 2

                # Remove bad points and interpolate to replace them
                shares.loc[idx_bad] = np.nan
                self._shares_ts = shares.interpolate()                
        return self._shares_ts


class FundamentalEquityTS(FundamentalEquityGeneral):
    def __init__(self, eod_fund_data_dict: dict, frequency: str = 'q'):
        super(FundamentalEquityTS, self).__init__(eod_fund_data_dict)
        self.frequency = frequency

    @property
    def frequency_eod(self):
        return 'quarterly' if self.frequency == 'q' else 'yearly'

    def get_time_series(self, data_types: Union[list, str]) -> pd.DataFrame:
        if isinstance(data_types, str):
            data_types = [data_types]

        # Create a map from the financial statement type to a list of corresponding data types
        statement_type_map = {st: [] for st in FinancialStatementTypes._value2member_map_.keys()}
        for data_type in data_types:
            statement_type = FUNDAMENTAL_DATA_TYPE_MAP[data_type]
            statement_type_map[statement_type].append(data_type)

        # For each calculated data type, ensure its dependent series are included
        calc_data_types = statement_type_map[FinancialStatementTypes.CALCULATED.value]
        statement_type_map = self._add_dependent_data_types(statement_type_map, calc_data_types)

        ts_list = []
        for statement_type, sub_data_types in statement_type_map.items():
            if statement_type == FinancialStatementTypes.CALCULATED.value:
                continue  # Save the calculated series for last

            raw_ts = dict()
            for values in self._data['Financials'][statement_type][self.frequency_eod].values():
                raw_ts[values['date']] = {dt: values[dt] for dt in sub_data_types}

            if raw_ts:
                ts_list.append(pd.DataFrame(raw_ts, dtype=np.float32).T)

        if not ts_list:
            underlying_ts = pd.DataFrame([], dtype=np.float32)
        else:
            underlying_ts = pd.concat(ts_list, axis=1).astype(np.float32).sort_index()

        # Perform any calculations if necessary
        return self._add_calculated_time_series(underlying_ts, calc_data_types)

    def _add_dependent_data_types(self, statement_type_map, calc_data_types):
        if not calc_data_types:
            return statement_type_map
        else:
            raise NotImplementedError()

    def _add_calculated_time_series(self, underlying_ts, calc_data_types):
        if not calc_data_types:
            return underlying_ts
        else:
            raise NotImplementedError()
