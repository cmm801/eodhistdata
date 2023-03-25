"""Definitions of important constants."""

from enum import Enum
from frozendict import frozendict


# A list of the exchange codes that use exchange_id == 'US'
US_EXCHANGES = [
    'AMEX', 'BATS', 'NASDAQ', 'NMFQS', 'NYSE', 'NYSE ARCA',
    'NYSE MKT', 'OTC', 'OTCBB', 'OTCCE', 'OTCGREY', 'OTCMKTS',
    'OTCQB', 'OTCQX', 'PINK']

# A list of exchanges we can ignore
EXCLUDED_EXCHANGES = ('NMFQS', 'PINK')

# Date from which we should download historical data (if available)
HISTORICAL_DATA_START_DATE = '1989-12-31'


class TimeSeriesNames(Enum):
    """Enum with names of some important time series."""
    ADJUSTED_CLOSE = 'adjusted_close'
    CLOSE = 'close'
    MARKET_CAP = 'market_cap'
    MONTHLY_RETURNS = 'monthly_returns'
    VOLUME = 'volume'


class FinancialStatementTypes(Enum):
    """An Enum class containing financial statement types."""
    INCOME_STATEMENT = 'Income_Statement'
    BALANCE_SHEET = 'Balance_Sheet'
    CASH_FLOW_STATEMENT = 'Cash_Flow'
    CALCULATED = 'Calculated'


class EODDataTypes(Enum):
    """An Enum class enumerating the various available data sets."""
    EXCHANGE_LIST = 'exchange_list'
    EXCHANGE_SYMBOLS = 'exchange_symbols'
    HISTORICAL_TIME_SERIES = 'historical_time_series'
    MARKET_CAP = 'market_cap'
    FUNDAMENTAL_EQUITY = 'fundamental_equity'
    FUNDAMENTAL_EQUITY_BULK = 'fundamental_equity_bulk'    


class FundamentalDataTypes(Enum):
    """A class enumerating the different types of fundamental data available."""
    accountsPayable = "accountsPayable"
    accumulatedAmortization = "accumulatedAmortization"
    accumulatedDepreciation = "accumulatedDepreciation"
    accumulatedOtherComprehensiveIncome = "accumulatedOtherComprehensiveIncome"
    additionalPaidInCapital = "additionalPaidInCapital"
    beginPeriodCashFlow = "beginPeriodCashFlow"
    capitalExpenditures = "capitalExpenditures"
    capitalLeaseObligations = "capitalLeaseObligations"
    capitalStock = "capitalStock"
    capitalSurpluse = "capitalSurpluse"
    cash = "cash"
    cashAndCashEquivalentsChanges = "cashAndCashEquivalentsChanges"
    cashAndEquivalents = "cashAndEquivalents"
    cashAndShortTermInvestments = "cashAndShortTermInvestments"
    cashFlowsOtherOperating = "cashFlowsOtherOperating"
    changeInCash = "changeInCash"
    changeInWorkingCapital = "changeInWorkingCapital"
    changeReceivables = "changeReceivables"
    changeToAccountReceivables = "changeToAccountReceivables"
    changeToInventory = "changeToInventory"
    changeToLiabilities = "changeToLiabilities"
    changeToNetincome = "changeToNetincome"
    changeToOperatingActivities = "changeToOperatingActivities"
    commonStock = "commonStock"
    commonStockSharesOutstanding = "commonStockSharesOutstanding"
    commonStockTotalEquity = "commonStockTotalEquity"
    costOfRevenue = "costOfRevenue"
    currentDeferredRevenue = "currentDeferredRevenue"
    deferredLongTermAssetCharges = "deferredLongTermAssetCharges"
    deferredLongTermLiab = "deferredLongTermLiab"
    depreciation = "depreciation"
    depreciationAndAmortization = "depreciationAndAmortization"
    discontinuedOperations = "discontinuedOperations"
    dividendsPaid = "dividendsPaid"
    earningAssets = "earningAssets"
    ebit = "ebit"
    ebitda = "ebitda"
    effectOfAccountingCharges = "effectOfAccountingCharges"
    endPeriodCashFlow = "endPeriodCashFlow"
    exchangeRateChanges = "exchangeRateChanges"
    extraordinaryItems = "extraordinaryItems"
    freeCashFlow = "freeCashFlow"
    goodWill = "goodWill"
    grossProfit = "grossProfit"
    incomeBeforeTax = "incomeBeforeTax"
    incomeTaxExpense = "incomeTaxExpense"
    intangibleAssets = "intangibleAssets"
    interestExpense = "interestExpense"
    interestIncome = "interestIncome"
    inventory = "inventory"
    investments = "investments"
    issuanceOfCapitalStock = "issuanceOfCapitalStock"
    liabilitiesAndStockholdersEquity = "liabilitiesAndStockholdersEquity"
    longTermDebt = "longTermDebt"
    longTermDebtTotal = "longTermDebtTotal"
    longTermInvestments = "longTermInvestments"
    minorityInterest = "minorityInterest"
    negativeGoodwill = "negativeGoodwill"
    netBorrowings = "netBorrowings"
    netDebt = "netDebt"
    netIncome = "netIncome"
    netIncomeApplicableToCommonShares = "netIncomeApplicableToCommonShares"
    netIncomeFromContinuingOps = "netIncomeFromContinuingOps"
    netInterestIncome = "netInterestIncome"
    netInvestedCapital = "netInvestedCapital"
    netPayout = 'netPayout'
    netReceivables = "netReceivables"
    netTangibleAssets = "netTangibleAssets"
    netWorkingCapital = "netWorkingCapital"
    nonCurrentAssetsTotal = "nonCurrentAssetsTotal"
    nonCurrentLiabilitiesOther = "nonCurrentLiabilitiesOther"
    nonCurrentLiabilitiesTotal = "nonCurrentLiabilitiesTotal"
    nonCurrrentAssetsOther = "nonCurrrentAssetsOther"
    nonOperatingIncomeNetOther = "nonOperatingIncomeNetOther"
    nonRecurring = "nonRecurring"
    noncontrollingInterestInConsolidatedEntity = "noncontrollingInterestInConsolidatedEntity"
    operatingIncome = "operatingIncome"
    otherAssets = "otherAssets"
    otherCashflowsFromFinancingActivities = "otherCashflowsFromFinancingActivities"
    otherCashflowsFromInvestingActivities = "otherCashflowsFromInvestingActivities"
    otherCurrentAssets = "otherCurrentAssets"
    otherCurrentLiab = "otherCurrentLiab"
    otherItems = "otherItems"
    otherLiab = "otherLiab"
    otherNonCashItems = "otherNonCashItems"
    otherOperatingExpenses = "otherOperatingExpenses"
    otherStockholderEquity = "otherStockholderEquity"
    preferredStockAndOtherAdjustments = "preferredStockAndOtherAdjustments"
    preferredStockRedeemable = "preferredStockRedeemable"
    preferredStockTotalEquity = "preferredStockTotalEquity"
    propertyPlantAndEquipmentGross = "propertyPlantAndEquipmentGross"
    propertyPlantAndEquipmentNet = "propertyPlantAndEquipmentNet"
    propertyPlantEquipment = "propertyPlantEquipment"
    reconciledDepreciation = "reconciledDepreciation"
    researchDevelopment = "researchDevelopment"
    retainedEarnings = "retainedEarnings"
    retainedEarningsTotalEquity = "retainedEarningsTotalEquity"
    salePurchaseOfStock = "salePurchaseOfStock"
    sellingAndMarketingExpenses = "sellingAndMarketingExpenses"
    sellingGeneralAdministrative = "sellingGeneralAdministrative"
    shortLongTermDebt = "shortLongTermDebt"
    shortLongTermDebtTotal = "shortLongTermDebtTotal"
    shortTermDebt = "shortTermDebt"
    shortTermInvestments = "shortTermInvestments"
    stockBasedCompensation = "stockBasedCompensation"
    taxProvision = "taxProvision"
    temporaryEquityRedeemableNoncontrollingInterests = "temporaryEquityRedeemableNoncontrollingInterests"
    totalAssets = "totalAssets"
    totalCashFromFinancingActivities = "totalCashFromFinancingActivities"
    totalCashFromOperatingActivities = "totalCashFromOperatingActivities"
    totalCashflowsFromInvestingActivities = "totalCashflowsFromInvestingActivities"
    totalCurrentAssets = "totalCurrentAssets"
    totalCurrentLiabilities = "totalCurrentLiabilities"
    totalLiab = "totalLiab"
    totalOperatingExpenses = "totalOperatingExpenses"
    totalOtherIncomeExpenseNet = "totalOtherIncomeExpenseNet"
    totalPermanentEquity = "totalPermanentEquity"
    totalRevenue = "totalRevenue"
    totalStockholderEquity = "totalStockholderEquity"
    treasuryStock = "treasuryStock"
    warrants = "warrants"


# A map from different types of fundamental data to their location
FUNDAMENTAL_DATA_TYPE_MAP = frozendict({
    FundamentalDataTypes.accountsPayable.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.accumulatedAmortization.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.accumulatedDepreciation.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.accumulatedOtherComprehensiveIncome.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.additionalPaidInCapital.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.beginPeriodCashFlow.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.capitalExpenditures.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.capitalLeaseObligations.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.capitalStock.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.capitalSurpluse.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.cash.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.cashAndCashEquivalentsChanges.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.cashAndEquivalents.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.cashAndShortTermInvestments.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.cashFlowsOtherOperating.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.changeInCash.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.changeInWorkingCapital.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.changeReceivables.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.changeToAccountReceivables.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.changeToInventory.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.changeToLiabilities.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.changeToNetincome.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.changeToOperatingActivities.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.commonStock.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.commonStockSharesOutstanding.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.commonStockTotalEquity.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.costOfRevenue.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.currentDeferredRevenue.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.deferredLongTermAssetCharges.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.deferredLongTermLiab.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.depreciation.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.depreciationAndAmortization.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.discontinuedOperations.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.dividendsPaid.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.earningAssets.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.ebit.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.ebitda.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.effectOfAccountingCharges.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.endPeriodCashFlow.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.exchangeRateChanges.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.extraordinaryItems.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.freeCashFlow.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.goodWill.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.grossProfit.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.incomeBeforeTax.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.incomeTaxExpense.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.intangibleAssets.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.interestExpense.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.interestIncome.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.inventory.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.investments.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.issuanceOfCapitalStock.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.liabilitiesAndStockholdersEquity.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.longTermDebt.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.longTermDebtTotal.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.longTermInvestments.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.minorityInterest.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.negativeGoodwill.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.netBorrowings.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.netDebt.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.netIncome.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.netIncomeApplicableToCommonShares.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.netIncomeFromContinuingOps.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.netInterestIncome.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.netInvestedCapital.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.netReceivables.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.netTangibleAssets.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.netWorkingCapital.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.nonCurrentAssetsTotal.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.nonCurrentLiabilitiesOther.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.nonCurrentLiabilitiesTotal.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.nonCurrrentAssetsOther.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.nonOperatingIncomeNetOther.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.nonRecurring.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.noncontrollingInterestInConsolidatedEntity.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.operatingIncome.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.otherAssets.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.otherCashflowsFromFinancingActivities.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.otherCashflowsFromInvestingActivities.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.otherCurrentAssets.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.otherCurrentLiab.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.otherItems.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.otherLiab.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.otherNonCashItems.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.otherOperatingExpenses.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.otherStockholderEquity.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.preferredStockAndOtherAdjustments.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.preferredStockRedeemable.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.preferredStockTotalEquity.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.propertyPlantAndEquipmentGross.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.propertyPlantAndEquipmentNet.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.propertyPlantEquipment.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.reconciledDepreciation.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.researchDevelopment.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.retainedEarnings.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.retainedEarningsTotalEquity.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.salePurchaseOfStock.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.sellingAndMarketingExpenses.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.sellingGeneralAdministrative.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.shortLongTermDebt.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.shortLongTermDebtTotal.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.shortTermDebt.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.shortTermInvestments.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.stockBasedCompensation.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.taxProvision.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.temporaryEquityRedeemableNoncontrollingInterests.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.totalAssets.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.totalCashFromFinancingActivities.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.totalCashFromOperatingActivities.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.totalCashflowsFromInvestingActivities.value: FinancialStatementTypes.CASH_FLOW_STATEMENT.value,
    FundamentalDataTypes.totalCurrentAssets.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.totalCurrentLiabilities.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.totalLiab.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.totalOperatingExpenses.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.totalOtherIncomeExpenseNet.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.totalPermanentEquity.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.totalRevenue.value: FinancialStatementTypes.INCOME_STATEMENT.value,
    FundamentalDataTypes.totalStockholderEquity.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.treasuryStock.value: FinancialStatementTypes.BALANCE_SHEET.value,
    FundamentalDataTypes.warrants.value: FinancialStatementTypes.BALANCE_SHEET.value,
})