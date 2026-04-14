"""
BTG Pactual Position API Client

A typed Python client for the BTG Pactual Position API.
Each endpoint is exposed as an individual function that can be imported separately.

Configuration via environment variables:
    BTG_CLIENT_ID: OAuth2 client ID (required)
    BTG_CLIENT_SECRET: OAuth2 client secret (required)

Usage:
    from btg_api_position import get_position_by_account
    position = get_position_by_account("001234567")
"""

from __future__ import annotations

from typing import TypedDict, NotRequired

import httpx

from btg_api_utils import build_headers, handle_response
from _response import validate_response

# =============================================================================
# Configuration
# =============================================================================

BASE_URL = "https://api.btgpactual.com/iaas-api-position"
DEFAULT_TIMEOUT = 30.0


# =============================================================================
# Type Definitions - Request Types
# =============================================================================

class PositionDateRequest(TypedDict):
    """Request body for position by date query."""
    date: str  # Format: "YYYY-MM-DD"


class PositionPURequest(TypedDict):
    """Request body for unit price by period query."""
    startDate: NotRequired[str]  # Format: "YYYY-MM-DD"
    endDate: NotRequired[str]  # Format: "YYYY-MM-DD"


class PositionPeriodFilter(TypedDict):
    """Request body for V2 unit price by period query."""
    startDate: str  # Format: "YYYY-MM-DD"
    endDate: str  # Format: "YYYY-MM-DD"


class FixedIncomeHistoryRequest(TypedDict):
    """Request body for fixed income history by accounts."""
    accounts: list[str]


# =============================================================================
# Type Definitions - Nested Types (alphabetically organized)
# =============================================================================

class ACCACE(TypedDict):
    campo: NotRequired[str]


class AccountingGroup(TypedDict):
    Code: NotRequired[str]
    Name: NotRequired[str]
    Quantity: NotRequired[str]
    KnockIn: NotRequired[str]
    KnockOut: NotRequired[str]
    StrikePrice: NotRequired[str]
    MarketValue: NotRequired[str]
    TypeGroup: NotRequired[str]
    ReferencePremium: NotRequired[str]
    BarrierType: NotRequired[str]
    ReferenceProductSymbol: NotRequired[str]


class Acquisition(TypedDict):
    """Acquisition details for investment funds."""
    CostPrice: NotRequired[str]
    IncomeTax: NotRequired[str]
    VirtualIOF: NotRequired[str]
    NetAssetValue: NotRequired[str]
    GrossAssetValue: NotRequired[str]
    AcquisitionDate: NotRequired[str]
    NumberOfShares: NotRequired[str]
    AcquisitionNumber: NotRequired[str]
    OrigemAmortizacao: NotRequired[str]
    CostValue: NotRequired[str]
    CotaCetipada: NotRequired[str]


class Prices(TypedDict):
    PriceType: NotRequired[str]
    Price: NotRequired[str]
    IncomeTax: NotRequired[str]
    IOFTax: NotRequired[str]


class Acquisitions(TypedDict):
    """Acquisition details for fixed income."""
    AcquisitionQuantity: NotRequired[str]
    SecurityCode: NotRequired[str]
    YieldToMaturity: NotRequired[str]
    AcquisitionDate: NotRequired[str]
    CostPrice: NotRequired[str]
    InitialInvestmentValue: NotRequired[str]
    InitialInvestmentQuantity: NotRequired[str]
    NetValue: NotRequired[str]
    GrossValue: NotRequired[str]
    IncomeTax: NotRequired[str]
    IOFTax: NotRequired[str]
    Yield: NotRequired[str]
    ComplementYield: NotRequired[str]
    IndexYieldRate: NotRequired[str]
    TransferId: NotRequired[str]
    FTSId: NotRequired[str]
    InterfaceDate: NotRequired[str]
    PriceIncomeTax: NotRequired[str]
    PriceVirtualIOF: NotRequired[str]
    DateTimeUpdate: NotRequired[str]
    PriceType: NotRequired[str]
    Price: NotRequired[str]
    Prices: NotRequired[list[Prices]]
    IsVirtual: NotRequired[str]


class ValuesPerCurrency(TypedDict):
    currency: NotRequired[str]
    amount: NotRequired[str]
    notionalValue: NotRequired[str]


class ValuesPerCurrencySBCLC(TypedDict):
    currency: NotRequired[str]
    amount: NotRequired[str]
    dealPrice: NotRequired[str]
    disbursedAmount: NotRequired[str]
    interest: NotRequired[str]
    iofTax: NotRequired[str]
    totalValue: NotRequired[str]


class ValuesPerCurrencyACC(TypedDict):
    ActualAmount: NotRequired[str]
    Currency: NotRequired[str]
    PrincipalAmount: NotRequired[str]


class ACCs(TypedDict):
    operationCode: NotRequired[str]
    Accrual: NotRequired[str]
    actualAmount: NotRequired[str]
    AnnualInterestRate: NotRequired[str]
    Basis: NotRequired[str]
    ContractCode: NotRequired[str]
    Currency: NotRequired[str]
    PositionDate: NotRequired[str]
    InterfaceDate: NotRequired[str]
    InceptionDate: NotRequired[str]
    MaturityDate: NotRequired[str]
    PercentIndex: NotRequired[str]
    PrincipalAmount: NotRequired[str]
    ReferenceIndexValue: NotRequired[str]
    TypeOfCredit: NotRequired[str]
    ValuesPerCurrency: NotRequired[list[ValuesPerCurrencyACC]]


class AveragePrice(TypedDict):
    Price: NotRequired[str]
    Adjustable: NotRequired[str]
    Proceeds: NotRequired[str]
    AccumulatedProceeds: NotRequired[str]
    TotalProceeds: NotRequired[str]


class BMFFuturePosition(TypedDict):
    Description: NotRequired[str]
    BuySell: NotRequired[str]
    Quantity: NotRequired[str]
    MarketPrice: NotRequired[str]
    MarketValue: NotRequired[str]
    MaturityDate: NotRequired[str]
    SecurityCode: NotRequired[str]
    Ticker: NotRequired[str]


class BMFOptionPosition(TypedDict):
    Ticker: NotRequired[str]
    BuySell: NotRequired[str]
    Quantity: NotRequired[str]
    MarketPremiumValue: NotRequired[str]
    MarketValue: NotRequired[str]
    MaturityDate: NotRequired[str]
    StrikePrice: NotRequired[str]
    OptionType: NotRequired[str]
    GrossValue: NotRequired[str]
    PremiumValue: NotRequired[str]
    SecurityCode: NotRequired[str]
    SecurityDescription: NotRequired[str]


class CashCollateral(TypedDict):
    CollateralDescription: NotRequired[str]
    FinancialValue: NotRequired[str]
    Custodian: NotRequired[str]
    CustodianCode: NotRequired[str]


class CashInvestedName(TypedDict):
    CodAtivo: NotRequired[str]
    Nome: NotRequired[str]
    Indexador: NotRequired[str]


class CashInvested(TypedDict):
    MovementID: NotRequired[str]
    Name: NotRequired[CashInvestedName]
    CostPrice: NotRequired[str]
    AcquisitionDate: NotRequired[str]
    Quantity: NotRequired[str]
    IncomeTax: NotRequired[str]
    IofTax: NotRequired[str]
    NetValue: NotRequired[str]
    GrossValue: NotRequired[str]
    Yield: NotRequired[str]
    IssueDate: NotRequired[str]
    MaturityDate: NotRequired[str]


class CetipOptionPosition(TypedDict):
    Underlying: NotRequired[str]
    BuySell: NotRequired[str]
    Quantity: NotRequired[str]
    MarketPremiumValue: NotRequired[str]
    MarketValue: NotRequired[str]
    QuotingFactor: NotRequired[str]
    MaturityDate: NotRequired[str]
    StrikePrice: NotRequired[str]
    OptionType: NotRequired[str]
    PortfolioPercentage: NotRequired[str]
    DealPrice: NotRequired[str]
    GrossValue: NotRequired[str]
    PremiumValue: NotRequired[str]
    KnockIn: NotRequired[str]
    KnockOut: NotRequired[str]
    SecurityCode: NotRequired[str]
    InterfaceDate: NotRequired[str]
    CodAsset: NotRequired[str]
    ReferencePremium: NotRequired[str]
    BarrierType: NotRequired[str]
    RebatePremium: NotRequired[str]
    FixingDate: NotRequired[str]
    AccountingGroup: NotRequired[list[AccountingGroup]]


class CollateralPositions(TypedDict):
    CollateralDescription: NotRequired[str]
    Description: NotRequired[str]
    MarketPrice: NotRequired[str]
    Quantity: NotRequired[str]
    Ticker: NotRequired[str]
    TotalValue: NotRequired[str]
    SecurityCode: NotRequired[str]


class Commitments(TypedDict):
    OperationCode: NotRequired[str]
    ContractCode: NotRequired[str]
    Currency: NotRequired[str]
    PositionDate: NotRequired[str]
    interfaceDate: NotRequired[str]
    amount: NotRequired[str]
    notionalValue: NotRequired[str]
    inceptionDate: NotRequired[str]
    maturityDate: NotRequired[str]
    interestRate: NotRequired[str]
    valuesPerCurrency: NotRequired[list[ValuesPerCurrency]]


class Credit(TypedDict):
    Description: NotRequired[str]
    FinancialValue: NotRequired[str]
    SettlementDate: NotRequired[str]


class CryptoAsset(TypedDict):
    name: NotRequired[str]
    code: NotRequired[str]
    type: NotRequired[str]
    productCode: NotRequired[str]


class CryptoAcquisition(TypedDict):
    quantity: NotRequired[str]
    ftsId: NotRequired[str]
    financial: NotRequired[str]
    grossFinancial: NotRequired[str]
    financialClosing: NotRequired[str]
    grossFinancialClosing: NotRequired[str]
    costBasis: NotRequired[str]
    invoiceCode: NotRequired[str]
    incomeTax: NotRequired[str]
    iofTax: NotRequired[str]
    updatedDate: NotRequired[str]
    interfaceDate: NotRequired[str]


class CurrentAccount(TypedDict):
    Value: NotRequired[str]
    PositionDate: NotRequired[str]


class DebtEarlyTerminationPeriod(TypedDict):
    FromDateTime: NotRequired[str]
    ToDateTime: NotRequired[str]


class DebtEarlyTerminationSchedules(TypedDict):
    IndexRateMultiplier: NotRequired[str]
    Rate: NotRequired[str]
    Type: NotRequired[str]
    EarlyTerminationPeriod: NotRequired[DebtEarlyTerminationPeriod]


class Derivative1(TypedDict):
    """Derivative in pending settlements."""
    SecurityCode: NotRequired[str]
    Description: NotRequired[str]
    FinancialValue: NotRequired[str]
    SettlementDate: NotRequired[str]
    Transaction: NotRequired[str]


class Equities1(TypedDict):
    """Equities in pending settlements."""
    Ticker: NotRequired[str]
    SecurityCode: NotRequired[str]
    Description: NotRequired[str]
    FinancialValue: NotRequired[str]
    SettlementDate: NotRequired[str]
    Transaction: NotRequired[str]


class FixedIncome1(TypedDict):
    """Fixed income in pending settlements."""
    SecurityCode: NotRequired[str]
    Description: NotRequired[str]
    FinancialValue: NotRequired[str]
    SettlementDate: NotRequired[str]
    Transaction: NotRequired[str]


class ReferenceAsset(TypedDict):
    SecurityCode: NotRequired[str]
    Ticker: NotRequired[str]


class ForwardPositions(TypedDict):
    Ticker: NotRequired[str]
    Description: NotRequired[str]
    Quantity: NotRequired[str]
    PLPrice: NotRequired[str]
    MarketValue: NotRequired[str]
    CostGrossPrice: NotRequired[str]
    MaturityDate: NotRequired[str]
    CostNetPrice: NotRequired[str]
    SecurityCode: NotRequired[str]
    StrikePrice: NotRequired[str]
    QuantityPendingSettlement: NotRequired[str]
    ReferenceAsset: NotRequired[ReferenceAsset]
    InterfaceDate: NotRequired[str]


class Fund(TypedDict):
    FundName: NotRequired[str]
    SecurityCode: NotRequired[str]
    FundCGECode: NotRequired[str]
    FundCNPJCode: NotRequired[str]
    DatePortfolio: NotRequired[str]
    ManagerName: NotRequired[str]
    ManagerCGECode: NotRequired[str]
    FundLiquidity: NotRequired[str]
    BenchMark: NotRequired[str]
    EsTipoPortfolio: NotRequired[str]
    TipoCvm: NotRequired[str]
    EntityType: NotRequired[str]
    RelatedSecurityCodeClass: NotRequired[str]
    RelatedSecurityCodeFund: NotRequired[str]
    RelatedClassCGECode: NotRequired[str]
    RelatedFundCGECode: NotRequired[str]


class InvestmentFund1(TypedDict):
    """Investment fund in pending settlements."""
    SecurityCode: NotRequired[str]
    Description: NotRequired[str]
    FinancialValue: NotRequired[str]
    SettlementDate: NotRequired[str]
    Transaction: NotRequired[str]


class IrAliquots(TypedDict):
    Aliquot: NotRequired[str]
    IR: NotRequired[str]


class Loan(TypedDict):
    ContractCode: NotRequired[str]
    InceptionDate: NotRequired[str]
    MaturityDate: NotRequired[str]
    DealAmount: NotRequired[str]
    LoanType: NotRequired[str]
    TypeOfCredit: NotRequired[str]
    PercentIndex: NotRequired[str]
    PrincipalAmount: NotRequired[str]
    ActualAmount: NotRequired[str]
    Accrual: NotRequired[str]
    AnnualInterestRate: NotRequired[str]
    Basis: NotRequired[str]
    PositionDate: NotRequired[str]


class NDFPosition(TypedDict):
    NDFCode: NotRequired[str]
    BuySell: NotRequired[str]
    MaturityDate: NotRequired[str]
    CurrentSecurityPrice: NotRequired[str]
    GrossValue: NotRequired[str]
    InceptionDate: NotRequired[str]
    ForwardRate: NotRequired[str]
    Principal: NotRequired[str]
    CurrentCurrencyPrice: NotRequired[str]
    IOFTax: NotRequired[str]
    IncomeTax: NotRequired[str]
    PriceType: NotRequired[str]
    ReferencedSecurity: NotRequired[str]
    ValueType: NotRequired[str]


class TickerInfo(TypedDict):
    LastTradePrice: NotRequired[str]
    ChangePercent: NotRequired[str]
    LastTradeTime: NotRequired[str]


class OptionPositions(TypedDict):
    Ticker: NotRequired[str]
    BuySell: NotRequired[str]
    PremiumValue: NotRequired[str]
    MarketPremium: NotRequired[str]
    PrevClose: NotRequired[str]
    Quantity: NotRequired[str]
    TotalValue: NotRequired[str]
    StrikePrice: NotRequired[str]
    MaturityDate: NotRequired[str]
    OptionType: NotRequired[str]
    Description: NotRequired[str]
    SecurityCode: NotRequired[str]
    QuantityPendingSettlement: NotRequired[str]
    TickerInfo: NotRequired[TickerInfo]
    ReferenceAsset: NotRequired[ReferenceAsset]
    InterfaceDate: NotRequired[str]
    AveragePrice: NotRequired[AveragePrice]


class Others(TypedDict):
    SecurityCode: NotRequired[str]
    Description: NotRequired[str]
    FinancialValue: NotRequired[str]
    SettlementDate: NotRequired[str]
    Transaction: NotRequired[str]


class Pension(TypedDict):
    """Pension in pending settlements."""
    SecurityCode: NotRequired[str]
    Description: NotRequired[str]
    FinancialValue: NotRequired[str]
    SettlementDate: NotRequired[str]
    Transaction: NotRequired[str]


class Positions(TypedDict):
    """Pension positions."""
    FundCGECode: NotRequired[str]
    FundCode: NotRequired[str]
    FundName: NotRequired[str]
    ShareValue: NotRequired[str]
    NumberOfShares: NotRequired[str]
    GrossAssetValue: NotRequired[str]
    NetAssetValue: NotRequired[str]
    AssetCostPrice: NotRequired[str]
    Type: NotRequired[str]
    FundType: NotRequired[str]
    IncomeType: NotRequired[str]
    IndividualGrossAssetValue: NotRequired[str]
    IndividualNumberOfShares: NotRequired[str]
    IndividualPreviousNetAssetValue: NotRequired[str]
    IndividualShareValue: NotRequired[str]
    SusepCode: NotRequired[str]
    TaxRegime: NotRequired[str]
    CertificateName: NotRequired[str]
    CertificateStatus: NotRequired[str]
    InitialDate: NotRequired[str]
    ChangeSincePreviousMonth: NotRequired[str]
    IsExternalPension: NotRequired[str]
    ExternalPension: NotRequired[str]
    PensionCnpjCode: NotRequired[str]
    PositionDate: NotRequired[str]
    PerformanceMonthly: NotRequired[str]
    PerformanceYearly: NotRequired[str]
    Performance12Months: NotRequired[str]
    SecurityCode: NotRequired[str]
    IrAliquots: NotRequired[IrAliquots]


class PrecatoryAsset(TypedDict):
    AssetCode: NotRequired[str]
    Ticker: NotRequired[str]
    FantasyName: NotRequired[str]
    Type: NotRequired[str]
    RiskType: NotRequired[str]
    ProductCode: NotRequired[str]
    AssetType: NotRequired[str]
    AssetSubType: NotRequired[str]
    SettleDate: NotRequired[str]
    MaturityDate: NotRequired[str]


class PrecatoryAcquisition(TypedDict):
    InvoiceCode: NotRequired[str]
    InterfaceDate: NotRequired[str]
    IssueDate: NotRequired[str]
    Quantity: NotRequired[str]
    GrossValue: NotRequired[str]
    CostPrice: NotRequired[str]
    InvestedValue: NotRequired[str]


class PrecatoryScenario(TypedDict):
    Classifier: NotRequired[str]
    EstimatedDeadlineInMonths: NotRequired[str]
    Rentability: NotRequired[str]
    Multiplier: NotRequired[str]
    RentabilityTir: NotRequired[str]
    Indexer: NotRequired[str]
    RentabilityFormatted: NotRequired[str]
    EstimatedDeadlineFormatted: NotRequired[str]


class PortfolioInvestments(TypedDict):
    Code: NotRequired[str]
    GrossValue: NotRequired[str]
    Name: NotRequired[str]
    StockPositions: NotRequired[list["StockPositions"]]


class RealEstate(TypedDict):
    campo: NotRequired[str]


class Receivables(TypedDict):
    campo: NotRequired[str]


class SBCLC(TypedDict):
    accountCgeCode: NotRequired[str]
    accountCgeDescription: NotRequired[str]
    operationCode: NotRequired[str]
    contractCode: NotRequired[str]
    currency: NotRequired[str]
    inceptionDate: NotRequired[str]
    maturityDate: NotRequired[str]
    DealPrice: NotRequired[str]
    blocked: NotRequired[str]
    Description: NotRequired[str]
    feesPay: NotRequired[str]
    TotalValue: NotRequired[str]
    PositionDate: NotRequired[str]
    InterfaceDate: NotRequired[str]
    IofTax: NotRequired[str]
    interest: NotRequired[str]
    amount: NotRequired[str]
    disbursedAmount: NotRequired[str]
    ValuesPerCurrency: NotRequired[list[ValuesPerCurrencySBCLC]]


class StockLendingPositions(TypedDict):
    Ticker: NotRequired[str]
    LendingType: NotRequired[str]
    Quantity: NotRequired[str]
    MarketPrice: NotRequired[str]
    TotalValue: NotRequired[str]
    GrossAccruedValue: NotRequired[str]
    TransactionDate: NotRequired[str]
    RatePorcent: NotRequired[str]
    LenderRebate: NotRequired[str]
    MarketValue: NotRequired[str]
    MaturityDate: NotRequired[str]
    IRTax: NotRequired[str]
    SecurityCode: NotRequired[str]
    CdOperationType: NotRequired[str]
    ReferenceAsset: NotRequired[ReferenceAsset]
    InterfaceDate: NotRequired[str]


class StockPositions(TypedDict):
    Ticker: NotRequired[str]
    Description: NotRequired[str]
    Quantity: NotRequired[str]
    MarketPrice: NotRequired[str]
    PrevClose: NotRequired[str]
    GrossValue: NotRequired[str]
    CostPrice: NotRequired[str]
    ISINCode: NotRequired[str]
    IncomeTax: NotRequired[str]
    InitialInvestimentValue: NotRequired[str]
    Issuer: NotRequired[str]
    SectorCode: NotRequired[str]
    SectorDescription: NotRequired[str]
    SecurityCode: NotRequired[str]
    QuantityPendingSettlement: NotRequired[str]
    IsFII: NotRequired[str]
    TickerInfo: NotRequired[TickerInfo]
    AveragePrice: NotRequired[AveragePrice]
    ReferenceAsset: NotRequired[ReferenceAsset]
    InterfaceDate: NotRequired[str]
    PreferenceToIncome: NotRequired[str]
    FirstDealingDate: NotRequired[str]
    ReferencePrice: NotRequired[str]
    QuotingFactor: NotRequired[str]
    IssuerCge: NotRequired[str]
    EquityTypeDescription: NotRequired[str]


class StructuredProducts(TypedDict):
    Code: NotRequired[str]
    Name: NotRequired[str]
    ReferenceSecurityCode: NotRequired[str]
    ReferenceProductSymbol: NotRequired[str]
    FixingDate: NotRequired[str]
    Quantity: NotRequired[str]
    GrossValue: NotRequired[str]
    StockPositions: NotRequired[list[StockPositions]]
    CetipOptionPosition: NotRequired[list[CetipOptionPosition]]


class SwapPosition(TypedDict):
    SwapCode: NotRequired[str]
    PrincipalAmount: NotRequired[str]
    MarketValueAsset: NotRequired[str]
    MarketValueLiability: NotRequired[str]
    TotalValue: NotRequired[str]
    IndexAsset: NotRequired[str]
    PorcentIndexAsset: NotRequired[str]
    CupomInterestRateAsset: NotRequired[str]
    InceptionDate: NotRequired[str]
    MaturityDate: NotRequired[str]
    IndexLiability: NotRequired[str]
    PorcentIndexLiability: NotRequired[str]
    CupomInterestRateLiability: NotRequired[str]
    OperatorCode: NotRequired[str]
    PriceType: NotRequired[str]
    ValueType: NotRequired[str]


# =============================================================================
# Type Definitions - Main Types
# =============================================================================

class SummaryAccount(TypedDict):
    """Market position summary."""
    MarketName: NotRequired[str]
    MarketAbbreviation: NotRequired[str]
    PositionDate: NotRequired[str]
    EndPositionValue: NotRequired[str]
    StartPositionValue: NotRequired[str]


class InvestmentFund(TypedDict):
    """Investment fund position."""
    ShareValue: NotRequired[str]
    Fund: NotRequired[Fund]
    Acquisition: NotRequired[list[Acquisition]]
    CotaCetipadaFundoExterno: NotRequired[str]
    PositionDate: NotRequired[str]
    ProcessingDateTime: NotRequired[str]


class InvestmentFundCotaCetipada(TypedDict):
    """External investment fund position."""
    ShareValue: NotRequired[str]
    Fund: NotRequired[Fund]
    Acquisition: NotRequired[list[Acquisition]]
    CotaCetipadaFundoExterno: NotRequired[str]
    PositionDate: NotRequired[str]
    ProcessingDateTime: NotRequired[str]


class FixedIncome(TypedDict):
    """Fixed income position."""
    AccountingGroupCode: NotRequired[str]
    Issuer: NotRequired[str]
    IssueDate: NotRequired[str]
    SecurityCode: NotRequired[str]
    IssuerCGECode: NotRequired[str]
    PriceType: NotRequired[str]
    ValueType: NotRequired[str]
    Yield: NotRequired[str]
    Ticker: NotRequired[str]
    ReferenceIndexName: NotRequired[str]
    ReferenceIndexValue: NotRequired[str]
    IndexYieldRate: NotRequired[str]
    MaturityDate: NotRequired[str]
    Quantity: NotRequired[str]
    Price: NotRequired[str]
    GrossValue: NotRequired[str]
    IncomeTax: NotRequired[str]
    IOFTax: NotRequired[str]
    NetValue: NotRequired[str]
    IsLiquidity: NotRequired[str]
    Acquisitions: NotRequired[list[Acquisitions]]
    FTSId: NotRequired[str]
    IsRepo: NotRequired[str]
    CetipCode: NotRequired[str]
    SelicCode: NotRequired[str]
    ISIN: NotRequired[str]
    TaxFree: NotRequired[str]
    IssuerType: NotRequired[str]
    Projection: NotRequired[str]
    Lag: NotRequired[str]
    Default: NotRequired[str]
    YieldAvg: NotRequired[str]
    DebtEarlyTerminationSchedules: NotRequired[list[DebtEarlyTerminationSchedules]]


class Credits(TypedDict):
    """Credit positions."""
    ACCACEs: NotRequired[list[ACCACE]]
    Loan: NotRequired[list[Loan]]
    Commitments: NotRequired[list[Commitments]]
    RealEstate: NotRequired[list[RealEstate]]
    Receivables: NotRequired[list[Receivables]]
    SBCLC: NotRequired[list[SBCLC]]
    ACCs: NotRequired[list[ACCs]]


class PensionInformations(TypedDict):
    """Pension information."""
    FundType: NotRequired[str]
    CertificateName: NotRequired[str]
    StartDate: NotRequired[str]
    FirstContributionDate: NotRequired[str]
    CertificateStatus: NotRequired[str]
    TaxRegime: NotRequired[str]
    IncomeType: NotRequired[str]
    Recipient: NotRequired[str]
    SusepCode: NotRequired[str]
    CorporateCNPJ: NotRequired[str]
    CorporateName: NotRequired[str]
    GrossValue: NotRequired[str]
    NetValue: NotRequired[str]
    CostPrice: NotRequired[str]
    Positions: NotRequired[list[Positions]]
    IsExternalPension: NotRequired[str]
    ExternalPension: NotRequired[str]
    PositionDate: NotRequired[str]
    ContractType: NotRequired[str]


class Commodity(TypedDict):
    """Commodity position."""
    MarketPrice: NotRequired[str]
    MarketValue: NotRequired[str]
    Quantity: NotRequired[str]
    SecurityCode: NotRequired[str]
    Ticker: NotRequired[str]


class Equities(TypedDict):
    """Variable income positions."""
    ForwardPositions: NotRequired[list[ForwardPositions]]
    OptionPositions: NotRequired[list[OptionPositions]]
    StockLendingPositions: NotRequired[list[StockLendingPositions]]
    StockPositions: NotRequired[list[StockPositions]]
    CollateralPositions: NotRequired[list[CollateralPositions]]
    StructuredProducts: NotRequired[list[StructuredProducts]]
    CetipOptionPosition: NotRequired[list[CetipOptionPosition]]
    PortfolioInvestments: NotRequired[list[PortfolioInvestments]]


class Derivative(TypedDict):
    """Derivative positions."""
    NDFPosition: NotRequired[list[NDFPosition]]
    BMFFuturePosition: NotRequired[list[BMFFuturePosition]]
    BMFOptionPosition: NotRequired[list[BMFOptionPosition]]
    CetipOptionPosition: NotRequired[list[CetipOptionPosition]]
    SwapPosition: NotRequired[list[SwapPosition]]


class FixedIncomeStructuredNote(TypedDict):
    """COE (Structured note) position."""
    Issuer: NotRequired[str]
    IssueDate: NotRequired[str]
    MaturityDate: NotRequired[str]
    ReferenceIndexName: NotRequired[str]
    ReferenceIndexValue: NotRequired[str]
    Quantity: NotRequired[str]
    CostPrice: NotRequired[str]
    Price: NotRequired[str]
    InitialInvestmentValue: NotRequired[str]
    GrossValue: NotRequired[str]
    NetValue: NotRequired[str]
    AccountingGroupCode: NotRequired[str]
    IOFTax: NotRequired[str]
    IncomeTax: NotRequired[str]
    SecurityCode: NotRequired[str]
    Ticker: NotRequired[str]
    Yield: NotRequired[str]
    YieldToMaturity: NotRequired[str]
    FantasyName: NotRequired[str]
    InterfaceDate: NotRequired[str]
    PriceIncomeTax: NotRequired[str]
    PriceVirtualIOF: NotRequired[str]
    DateTimeUpdate: NotRequired[str]
    Description: NotRequired[str]
    CetipCode: NotRequired[str]


class PayableReceivables(TypedDict):
    """Payables and receivables."""
    Credit: NotRequired[list[Credit]]


class PendingSettlements(TypedDict):
    """Values in transit."""
    FixedIncome: NotRequired[list[FixedIncome1]]
    InvestmentFund: NotRequired[list[InvestmentFund1]]
    Equities: NotRequired[list[Equities1]]
    Derivative: NotRequired[list[Derivative1]]
    Pension: NotRequired[list[Pension]]
    Others: NotRequired[list[Others]]


class CryptoCoins(TypedDict):
    """Crypto asset positions."""
    quantity: NotRequired[str]
    financial: NotRequired[str]
    grossFinancial: NotRequired[str]
    financialClosing: NotRequired[str]
    grossFinancialClosing: NotRequired[str]
    costBasis: NotRequired[str]
    positionDate: NotRequired[str]
    updatedDate: NotRequired[str]
    puClosing: NotRequired[str]
    marketPrice: NotRequired[str]
    incomeTax: NotRequired[str]
    iofTax: NotRequired[str]
    asset: NotRequired[CryptoAsset]
    acquisitions: NotRequired[list[CryptoAcquisition]]


class Cash(TypedDict):
    """Cash positions."""
    CashCollateral: NotRequired[list[CashCollateral]]
    CurrentAccount: NotRequired[CurrentAccount]
    CashInvested: NotRequired[list[CashInvested]]


class CashCollateralRoot(TypedDict):
    """Cash collateral position."""
    BlockedMethod: NotRequired[str]
    FinancialValue: NotRequired[str]
    ReserveType: NotRequired[str]
    Protocol: NotRequired[str]
    PositionDate: NotRequired[str]


class Precatories(TypedDict):
    """Court-ordered debt positions."""
    IssueDate: NotRequired[str]
    Quantity: NotRequired[str]
    GrossValue: NotRequired[str]
    CostPrice: NotRequired[str]
    MarketPrice: NotRequired[str]
    InvestedValue: NotRequired[str]
    Asset: NotRequired[PrecatoryAsset]
    Acquisitions: NotRequired[list[PrecatoryAcquisition]]
    Scenarios: NotRequired[list[PrecatoryScenario]]


class PrecatoriesCR(TypedDict):
    """CR Court-ordered debt positions."""
    IssueDate: NotRequired[str]
    Quantity: NotRequired[str]
    GrossValue: NotRequired[str]
    CostPrice: NotRequired[str]
    MarketPrice: NotRequired[str]
    InvestedValue: NotRequired[str]
    PositionDate: NotRequired[str]
    Asset: NotRequired[PrecatoryAsset]


class Position(TypedDict):
    """Complete position data for an account."""
    ContractVersion: NotRequired[str]
    AccountNumber: NotRequired[str]
    Agency: NotRequired[str]
    PositionDate: NotRequired[str]
    TotalAmount: NotRequired[str]
    SummaryAccounts: NotRequired[list[SummaryAccount]]
    InvestmentFund: NotRequired[list[InvestmentFund]]
    FixedIncome: NotRequired[list[FixedIncome]]
    InvestmentFundCotaCetipada: NotRequired[list[InvestmentFundCotaCetipada]]
    Credits: NotRequired[list[Credits]]
    PensionInformations: NotRequired[list[PensionInformations]]
    Commodity: NotRequired[list[Commodity]]
    Equities: NotRequired[list[Equities]]
    Derivative: NotRequired[list[Derivative]]
    FixedIncomeStructuredNote: NotRequired[list[FixedIncomeStructuredNote]]
    PayableReceivables: NotRequired[list[PayableReceivables]]
    PendingSettlements: NotRequired[list[PendingSettlements]]
    CryptoCoins: NotRequired[list[CryptoCoins]]
    Cash: NotRequired[list[Cash]]
    CashCollateralRoot: NotRequired[list[CashCollateralRoot]]
    Precatories: NotRequired[list[Precatories]]
    PrecatoriesCR: NotRequired[list[PrecatoriesCR]]


class PositionData(TypedDict):
    """Position data with account number and date."""
    AccountNumber: NotRequired[str]
    PositionDate: NotRequired[str]
    Position: NotRequired[Position]


class PositionDownloadData(TypedDict):
    """Download URL response for partner positions."""
    url: NotRequired[str]
    dateTime: NotRequired[str]
    numberOfAccounts: NotRequired[int]
    fileSize: NotRequired[int]


# =============================================================================
# API Functions - V1
# =============================================================================

def get_position_by_account(
    account_number: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> Position:
    """
    Get position summary for an account in real-time.

    Args:
        account_number: Account number to query (e.g., "001234567")
        timeout: Request timeout in seconds

    Returns:
        Position data for the account

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/position/{account_number}"
    headers = build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        return handle_response(response)


def get_position_by_account_and_date(
    account_number: str,
    date: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> PositionData:
    """
    Get position summary for an account at a specific date.

    Args:
        account_number: Account number to query (e.g., "001234567")
        date: Position date in format "YYYY-MM-DD"
        timeout: Request timeout in seconds

    Returns:
        Position data for the account at the specified date

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/position/{account_number}"
    headers = build_headers()
    body: PositionDateRequest = {"date": date}

    with httpx.Client(timeout=timeout) as client:
        return validate_response(
            client.post(url, headers=headers, json=body),
            [],
        )


def get_position_unit_price_by_account(
    account_number: str,
    start_date: str | None = None,
    end_date: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Request unit price (PU) by account and period for fixed income.

    This is an asynchronous call. Response will be delivered via webhook
    (positions-by-account).

    Args:
        account_number: Account number to query (e.g., "001234567")
        start_date: Start date in format "YYYY-MM-DD" (optional)
        end_date: End date in format "YYYY-MM-DD" (optional)
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/position/unit-price/{account_number}"
    headers = build_headers()
    body: PositionPURequest = {}
    if start_date:
        body["startDate"] = start_date
    if end_date:
        body["endDate"] = end_date

    with httpx.Client(timeout=timeout) as client:
        validate_response(
            client.post(url, headers=headers, json=body),
            [],
        )


def get_position_unit_price_history_by_account(
    account_number: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Request historical unit price (PU) by account for fixed income.

    This is an asynchronous call. Response will be delivered via webhook
    (positions-by-account).

    Args:
        account_number: Account number to query (e.g., "001234567")
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/position/unit-price/history/{account_number}"
    headers = build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


def get_partner_position(
    timeout: float = DEFAULT_TIMEOUT,
) -> PositionDownloadData:
    """
    Get positions for all accounts of the partner.

    Returns a URL to download a ZIP file containing position summaries
    for all accounts (Investment type only, not Funds).

    Note: You must call get_position_refresh() first to update the file.

    Args:
        timeout: Request timeout in seconds

    Returns:
        Download data including URL, datetime, account count, and file size

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/position/partner"
    headers = build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        return handle_response(response)


def get_position_refresh(
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Trigger refresh of partner positions file.

    This is an asynchronous call. Response will be delivered via webhook
    (positions-by-partner). The file is cached for 30 minutes.

    Also updates positions available via get_partner_position().

    Args:
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/position/refresh"
    headers = build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


# =============================================================================
# API Functions - V2
# =============================================================================

def get_position_unit_price_by_account_v2(
    account_number: str,
    start_date: str,
    end_date: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Request unit price (PU) by account and period for fixed income (V2).

    This is a synchronous call that triggers an asynchronous process.
    Response will be delivered via webhook (positions-by-account-v2).
    Results are cached for 12 hours.

    Args:
        account_number: Account number to query (e.g., "001234567")
        start_date: Start date in format "YYYY-MM-DD"
        end_date: End date in format "YYYY-MM-DD"
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v2/position/unit-price/{account_number}"
    headers = build_headers()
    body: PositionPeriodFilter = {
        "startDate": start_date,
        "endDate": end_date,
    }

    with httpx.Client(timeout=timeout) as client:
        validate_response(
            client.post(url, headers=headers, json=body),
            [],
        )


def get_position_unit_price_history_by_account_v2(
    account_number: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Request historical unit price (PU) by account for fixed income (V2).

    This is a synchronous call that triggers an asynchronous process.
    Response will be delivered via webhook (positions-by-account-v2).
    Results are cached for 7 days. Rate limit: 1 request per 30 minutes.

    Args:
        account_number: Account number to query (e.g., "001234567")
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v2/position/unit-price/history/{account_number}"
    headers = build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


def get_position_unit_price_history_by_partner_v2(
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Request historical unit price (PU) for all partner accounts (V2).

    This is an asynchronous call. Response will be delivered via webhook
    (positions-by-account-v2). Results are cached for 7 days.

    Args:
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v2/position/unit-price/history/partner"
    headers = build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


def get_position_unit_price_history_by_accounts_v2(
    accounts: list[str],
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Request historical unit price (PU) for a list of accounts (V2).

    This is a synchronous call that triggers an asynchronous process.
    Response will be delivered via webhook (positions-by-account-v2).
    Results are cached for 12 hours.

    Args:
        accounts: List of account numbers to query
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v2/position/unit-price/history/accounts"
    headers = build_headers()
    body: FixedIncomeHistoryRequest = {"accounts": accounts}

    with httpx.Client(timeout=timeout) as client:
        validate_response(
            client.post(url, headers=headers, json=body),
            [],
        )


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Configuration
    "BASE_URL",
    # Request Types
    "PositionDateRequest",
    "PositionPURequest",
    "PositionPeriodFilter",
    "FixedIncomeHistoryRequest",
    # Response Types - Main
    "Position",
    "PositionData",
    "PositionDownloadData",
    # Response Types - Categories
    "SummaryAccount",
    "InvestmentFund",
    "InvestmentFundCotaCetipada",
    "FixedIncome",
    "Credits",
    "PensionInformations",
    "Commodity",
    "Equities",
    "Derivative",
    "FixedIncomeStructuredNote",
    "PayableReceivables",
    "PendingSettlements",
    "CryptoCoins",
    "Cash",
    "CashCollateralRoot",
    "Precatories",
    "PrecatoriesCR",
    # Response Types - Nested
    "Acquisition",
    "Acquisitions",
    "Fund",
    "StockPositions",
    "OptionPositions",
    "ForwardPositions",
    "StockLendingPositions",
    "CollateralPositions",
    "StructuredProducts",
    "PortfolioInvestments",
    "NDFPosition",
    "BMFFuturePosition",
    "BMFOptionPosition",
    "CetipOptionPosition",
    "SwapPosition",
    "Loan",
    "Commitments",
    "SBCLC",
    "ACCs",
    "Positions",
    "CashCollateral",
    "CashInvested",
    "CryptoAcquisition",
    # API Functions - V1
    "get_position_by_account",
    "get_position_by_account_and_date",
    "get_position_unit_price_by_account",
    "get_position_unit_price_history_by_account",
    "get_partner_position",
    "get_position_refresh",
    # API Functions - V2
    "get_position_unit_price_by_account_v2",
    "get_position_unit_price_history_by_account_v2",
    "get_position_unit_price_history_by_partner_v2",
    "get_position_unit_price_history_by_accounts_v2",
]
