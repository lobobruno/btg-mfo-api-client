// Request Types

export interface PositionDateRequest {
  date: string;
}

export interface PositionPURequest {
  startDate?: string;
  endDate?: string;
}

export interface PositionPeriodFilter {
  startDate: string;
  endDate: string;
}

export interface FixedIncomeHistoryRequest {
  accounts: string[];
}

// Nested Types (alphabetically organized)

export interface ACCACE {
  campo?: string;
}

export interface AccountingGroup {
  Code?: string;
  Name?: string;
  Quantity?: string;
  KnockIn?: string;
  KnockOut?: string;
  StrikePrice?: string;
  MarketValue?: string;
  TypeGroup?: string;
  ReferencePremium?: string;
  BarrierType?: string;
  ReferenceProductSymbol?: string;
}

export interface Acquisition {
  CostPrice?: string;
  IncomeTax?: string;
  VirtualIOF?: string;
  NetAssetValue?: string;
  GrossAssetValue?: string;
  AcquisitionDate?: string;
  NumberOfShares?: string;
  AcquisitionNumber?: string;
  OrigemAmortizacao?: string;
  CostValue?: string;
  CotaCetipada?: string;
}

export interface Prices {
  PriceType?: string;
  Price?: string;
  IncomeTax?: string;
  IOFTax?: string;
}

export interface Acquisitions {
  AcquisitionQuantity?: string;
  SecurityCode?: string;
  YieldToMaturity?: string;
  AcquisitionDate?: string;
  CostPrice?: string;
  InitialInvestmentValue?: string;
  InitialInvestmentQuantity?: string;
  NetValue?: string;
  GrossValue?: string;
  IncomeTax?: string;
  IOFTax?: string;
  Yield?: string;
  ComplementYield?: string;
  IndexYieldRate?: string;
  TransferId?: string;
  FTSId?: string;
  InterfaceDate?: string;
  PriceIncomeTax?: string;
  PriceVirtualIOF?: string;
  DateTimeUpdate?: string;
  PriceType?: string;
  Price?: string;
  Prices?: Prices[];
  IsVirtual?: string;
}

export interface ValuesPerCurrency {
  currency?: string;
  amount?: string;
  notionalValue?: string;
}

export interface ValuesPerCurrencySBCLC {
  currency?: string;
  amount?: string;
  dealPrice?: string;
  disbursedAmount?: string;
  interest?: string;
  iofTax?: string;
  totalValue?: string;
}

export interface ValuesPerCurrencyACC {
  ActualAmount?: string;
  Currency?: string;
  PrincipalAmount?: string;
}

export interface ACCs {
  operationCode?: string;
  Accrual?: string;
  actualAmount?: string;
  AnnualInterestRate?: string;
  Basis?: string;
  ContractCode?: string;
  Currency?: string;
  PositionDate?: string;
  InterfaceDate?: string;
  InceptionDate?: string;
  MaturityDate?: string;
  PercentIndex?: string;
  PrincipalAmount?: string;
  ReferenceIndexValue?: string;
  TypeOfCredit?: string;
  ValuesPerCurrency?: ValuesPerCurrencyACC[];
}

export interface AveragePrice {
  Price?: string;
  Adjustable?: string;
  Proceeds?: string;
  AccumulatedProceeds?: string;
  TotalProceeds?: string;
}

export interface BMFFuturePosition {
  Description?: string;
  BuySell?: string;
  Quantity?: string;
  MarketPrice?: string;
  MarketValue?: string;
  MaturityDate?: string;
  SecurityCode?: string;
  Ticker?: string;
}

export interface BMFOptionPosition {
  Ticker?: string;
  BuySell?: string;
  Quantity?: string;
  MarketPremiumValue?: string;
  MarketValue?: string;
  MaturityDate?: string;
  StrikePrice?: string;
  OptionType?: string;
  GrossValue?: string;
  PremiumValue?: string;
  SecurityCode?: string;
  SecurityDescription?: string;
}

export interface CashCollateral {
  CollateralDescription?: string;
  FinancialValue?: string;
  Custodian?: string;
  CustodianCode?: string;
}

export interface CashInvestedName {
  CodAtivo?: string;
  Nome?: string;
  Indexador?: string;
}

export interface CashInvested {
  MovementID?: string;
  Name?: CashInvestedName;
  CostPrice?: string;
  AcquisitionDate?: string;
  Quantity?: string;
  IncomeTax?: string;
  IofTax?: string;
  NetValue?: string;
  GrossValue?: string;
  Yield?: string;
  IssueDate?: string;
  MaturityDate?: string;
}

export interface CetipOptionPosition {
  Underlying?: string;
  BuySell?: string;
  Quantity?: string;
  MarketPremiumValue?: string;
  MarketValue?: string;
  QuotingFactor?: string;
  MaturityDate?: string;
  StrikePrice?: string;
  OptionType?: string;
  PortfolioPercentage?: string;
  DealPrice?: string;
  GrossValue?: string;
  PremiumValue?: string;
  KnockIn?: string;
  KnockOut?: string;
  SecurityCode?: string;
  InterfaceDate?: string;
  CodAsset?: string;
  ReferencePremium?: string;
  BarrierType?: string;
  RebatePremium?: string;
  FixingDate?: string;
  AccountingGroup?: AccountingGroup[];
}

export interface CollateralPositions {
  CollateralDescription?: string;
  Description?: string;
  MarketPrice?: string;
  Quantity?: string;
  Ticker?: string;
  TotalValue?: string;
  SecurityCode?: string;
}

export interface Commitments {
  OperationCode?: string;
  ContractCode?: string;
  Currency?: string;
  PositionDate?: string;
  interfaceDate?: string;
  amount?: string;
  notionalValue?: string;
  inceptionDate?: string;
  maturityDate?: string;
  interestRate?: string;
  valuesPerCurrency?: ValuesPerCurrency[];
}

export interface Credit {
  Description?: string;
  FinancialValue?: string;
  SettlementDate?: string;
}

export interface CryptoAsset {
  name?: string;
  code?: string;
  type?: string;
  productCode?: string;
}

export interface CryptoAcquisition {
  quantity?: string;
  ftsId?: string;
  financial?: string;
  grossFinancial?: string;
  financialClosing?: string;
  grossFinancialClosing?: string;
  costBasis?: string;
  invoiceCode?: string;
  incomeTax?: string;
  iofTax?: string;
  updatedDate?: string;
  interfaceDate?: string;
}

export interface CurrentAccount {
  Value?: string;
  PositionDate?: string;
}

export interface DebtEarlyTerminationPeriod {
  FromDateTime?: string;
  ToDateTime?: string;
}

export interface DebtEarlyTerminationSchedules {
  IndexRateMultiplier?: string;
  Rate?: string;
  Type?: string;
  EarlyTerminationPeriod?: DebtEarlyTerminationPeriod;
}

export interface Derivative1 {
  SecurityCode?: string;
  Description?: string;
  FinancialValue?: string;
  SettlementDate?: string;
  Transaction?: string;
}

export interface Equities1 {
  Ticker?: string;
  SecurityCode?: string;
  Description?: string;
  FinancialValue?: string;
  SettlementDate?: string;
  Transaction?: string;
}

export interface FixedIncome1 {
  SecurityCode?: string;
  Description?: string;
  FinancialValue?: string;
  SettlementDate?: string;
  Transaction?: string;
}

export interface ReferenceAsset {
  SecurityCode?: string;
  Ticker?: string;
}

export interface ForwardPositions {
  Ticker?: string;
  Description?: string;
  Quantity?: string;
  PLPrice?: string;
  MarketValue?: string;
  CostGrossPrice?: string;
  MaturityDate?: string;
  CostNetPrice?: string;
  SecurityCode?: string;
  StrikePrice?: string;
  QuantityPendingSettlement?: string;
  ReferenceAsset?: ReferenceAsset;
  InterfaceDate?: string;
}

export interface Fund {
  FundName?: string;
  SecurityCode?: string;
  FundCGECode?: string;
  FundCNPJCode?: string;
  DatePortfolio?: string;
  ManagerName?: string;
  ManagerCGECode?: string;
  FundLiquidity?: string;
  BenchMark?: string;
  EsTipoPortfolio?: string;
  TipoCvm?: string;
  EntityType?: string;
  RelatedSecurityCodeClass?: string;
  RelatedSecurityCodeFund?: string;
  RelatedClassCGECode?: string;
  RelatedFundCGECode?: string;
}

export interface InvestmentFund1 {
  SecurityCode?: string;
  Description?: string;
  FinancialValue?: string;
  SettlementDate?: string;
  Transaction?: string;
}

export interface IrAliquots {
  Aliquot?: string;
  IR?: string;
}

export interface Loan {
  ContractCode?: string;
  InceptionDate?: string;
  MaturityDate?: string;
  DealAmount?: string;
  LoanType?: string;
  TypeOfCredit?: string;
  PercentIndex?: string;
  PrincipalAmount?: string;
  ActualAmount?: string;
  Accrual?: string;
  AnnualInterestRate?: string;
  Basis?: string;
  PositionDate?: string;
}

export interface NDFPosition {
  NDFCode?: string;
  BuySell?: string;
  MaturityDate?: string;
  CurrentSecurityPrice?: string;
  GrossValue?: string;
  InceptionDate?: string;
  ForwardRate?: string;
  Principal?: string;
  CurrentCurrencyPrice?: string;
  IOFTax?: string;
  IncomeTax?: string;
  PriceType?: string;
  ReferencedSecurity?: string;
  ValueType?: string;
}

export interface TickerInfo {
  LastTradePrice?: string;
  ChangePercent?: string;
  LastTradeTime?: string;
}

export interface OptionPositions {
  Ticker?: string;
  BuySell?: string;
  PremiumValue?: string;
  MarketPremium?: string;
  PrevClose?: string;
  Quantity?: string;
  TotalValue?: string;
  StrikePrice?: string;
  MaturityDate?: string;
  OptionType?: string;
  Description?: string;
  SecurityCode?: string;
  QuantityPendingSettlement?: string;
  TickerInfo?: TickerInfo;
  ReferenceAsset?: ReferenceAsset;
  InterfaceDate?: string;
  AveragePrice?: AveragePrice;
}

export interface Others {
  SecurityCode?: string;
  Description?: string;
  FinancialValue?: string;
  SettlementDate?: string;
  Transaction?: string;
}

export interface Pension {
  SecurityCode?: string;
  Description?: string;
  FinancialValue?: string;
  SettlementDate?: string;
  Transaction?: string;
}

export interface Positions {
  FundCGECode?: string;
  FundCode?: string;
  FundName?: string;
  ShareValue?: string;
  NumberOfShares?: string;
  GrossAssetValue?: string;
  NetAssetValue?: string;
  AssetCostPrice?: string;
  Type?: string;
  FundType?: string;
  IncomeType?: string;
  IndividualGrossAssetValue?: string;
  IndividualNumberOfShares?: string;
  IndividualPreviousNetAssetValue?: string;
  IndividualShareValue?: string;
  SusepCode?: string;
  TaxRegime?: string;
  CertificateName?: string;
  CertificateStatus?: string;
  InitialDate?: string;
  ChangeSincePreviousMonth?: string;
  IsExternalPension?: string;
  ExternalPension?: string;
  PensionCnpjCode?: string;
  PositionDate?: string;
  PerformanceMonthly?: string;
  PerformanceYearly?: string;
  Performance12Months?: string;
  SecurityCode?: string;
  IrAliquots?: IrAliquots;
}

export interface PrecatoryAsset {
  AssetCode?: string;
  Ticker?: string;
  FantasyName?: string;
  Type?: string;
  RiskType?: string;
  ProductCode?: string;
  AssetType?: string;
  AssetSubType?: string;
  SettleDate?: string;
  MaturityDate?: string;
}

export interface PrecatoryAcquisition {
  InvoiceCode?: string;
  InterfaceDate?: string;
  IssueDate?: string;
  Quantity?: string;
  GrossValue?: string;
  CostPrice?: string;
  InvestedValue?: string;
}

export interface PrecatoryScenario {
  Classifier?: string;
  EstimatedDeadlineInMonths?: string;
  Rentability?: string;
  Multiplier?: string;
  RentabilityTir?: string;
  Indexer?: string;
  RentabilityFormatted?: string;
  EstimatedDeadlineFormatted?: string;
}

export interface PortfolioInvestments {
  Code?: string;
  GrossValue?: string;
  Name?: string;
  StockPositions?: StockPositions[];
}

export interface RealEstate {
  campo?: string;
}

export interface Receivables {
  campo?: string;
}

export interface SBCLC {
  accountCgeCode?: string;
  accountCgeDescription?: string;
  operationCode?: string;
  contractCode?: string;
  currency?: string;
  inceptionDate?: string;
  maturityDate?: string;
  DealPrice?: string;
  blocked?: string;
  Description?: string;
  feesPay?: string;
  TotalValue?: string;
  PositionDate?: string;
  InterfaceDate?: string;
  IofTax?: string;
  interest?: string;
  amount?: string;
  disbursedAmount?: string;
  ValuesPerCurrency?: ValuesPerCurrencySBCLC[];
}

export interface StockLendingPositions {
  Ticker?: string;
  LendingType?: string;
  Quantity?: string;
  MarketPrice?: string;
  TotalValue?: string;
  GrossAccruedValue?: string;
  TransactionDate?: string;
  RatePorcent?: string;
  LenderRebate?: string;
  MarketValue?: string;
  MaturityDate?: string;
  IRTax?: string;
  SecurityCode?: string;
  CdOperationType?: string;
  ReferenceAsset?: ReferenceAsset;
  InterfaceDate?: string;
}

export interface StockPositions {
  Ticker?: string;
  Description?: string;
  Quantity?: string;
  MarketPrice?: string;
  PrevClose?: string;
  GrossValue?: string;
  CostPrice?: string;
  ISINCode?: string;
  IncomeTax?: string;
  InitialInvestimentValue?: string;
  Issuer?: string;
  SectorCode?: string;
  SectorDescription?: string;
  SecurityCode?: string;
  QuantityPendingSettlement?: string;
  IsFII?: string;
  TickerInfo?: TickerInfo;
  AveragePrice?: AveragePrice;
  ReferenceAsset?: ReferenceAsset;
  InterfaceDate?: string;
  PreferenceToIncome?: string;
  FirstDealingDate?: string;
  ReferencePrice?: string;
  QuotingFactor?: string;
  IssuerCge?: string;
  EquityTypeDescription?: string;
}

export interface StructuredProducts {
  Code?: string;
  Name?: string;
  ReferenceSecurityCode?: string;
  ReferenceProductSymbol?: string;
  FixingDate?: string;
  Quantity?: string;
  GrossValue?: string;
  StockPositions?: StockPositions[];
  CetipOptionPosition?: CetipOptionPosition[];
}

export interface SwapPosition {
  SwapCode?: string;
  PrincipalAmount?: string;
  MarketValueAsset?: string;
  MarketValueLiability?: string;
  TotalValue?: string;
  IndexAsset?: string;
  PorcentIndexAsset?: string;
  CupomInterestRateAsset?: string;
  InceptionDate?: string;
  MaturityDate?: string;
  IndexLiability?: string;
  PorcentIndexLiability?: string;
  CupomInterestRateLiability?: string;
  OperatorCode?: string;
  PriceType?: string;
  ValueType?: string;
}

// Main Types

export interface SummaryAccount {
  MarketName?: string;
  MarketAbbreviation?: string;
  PositionDate?: string;
  EndPositionValue?: string;
  StartPositionValue?: string;
}

export interface InvestmentFund {
  ShareValue?: string;
  Fund?: Fund;
  Acquisition?: Acquisition[];
  CotaCetipadaFundoExterno?: string;
  PositionDate?: string;
  ProcessingDateTime?: string;
}

export interface InvestmentFundCotaCetipada {
  ShareValue?: string;
  Fund?: Fund;
  Acquisition?: Acquisition[];
  CotaCetipadaFundoExterno?: string;
  PositionDate?: string;
  ProcessingDateTime?: string;
}

export interface FixedIncome {
  AccountingGroupCode?: string;
  Issuer?: string;
  IssueDate?: string;
  SecurityCode?: string;
  IssuerCGECode?: string;
  PriceType?: string;
  ValueType?: string;
  Yield?: string;
  Ticker?: string;
  ReferenceIndexName?: string;
  ReferenceIndexValue?: string;
  IndexYieldRate?: string;
  MaturityDate?: string;
  Quantity?: string;
  Price?: string;
  GrossValue?: string;
  IncomeTax?: string;
  IOFTax?: string;
  NetValue?: string;
  IsLiquidity?: string;
  Acquisitions?: Acquisitions[];
  FTSId?: string;
  IsRepo?: string;
  CetipCode?: string;
  SelicCode?: string;
  ISIN?: string;
  TaxFree?: string;
  IssuerType?: string;
  Projection?: string;
  Lag?: string;
  Default?: string;
  YieldAvg?: string;
  DebtEarlyTerminationSchedules?: DebtEarlyTerminationSchedules[];
}

export interface Credits {
  ACCACEs?: ACCACE[];
  Loan?: Loan[];
  Commitments?: Commitments[];
  RealEstate?: RealEstate[];
  Receivables?: Receivables[];
  SBCLC?: SBCLC[];
  ACCs?: ACCs[];
}

export interface PensionInformations {
  FundType?: string;
  CertificateName?: string;
  StartDate?: string;
  FirstContributionDate?: string;
  CertificateStatus?: string;
  TaxRegime?: string;
  IncomeType?: string;
  Recipient?: string;
  SusepCode?: string;
  CorporateCNPJ?: string;
  CorporateName?: string;
  GrossValue?: string;
  NetValue?: string;
  CostPrice?: string;
  Positions?: Positions[];
  IsExternalPension?: string;
  ExternalPension?: string;
  PositionDate?: string;
  ContractType?: string;
}

export interface Commodity {
  MarketPrice?: string;
  MarketValue?: string;
  Quantity?: string;
  SecurityCode?: string;
  Ticker?: string;
}

export interface Equities {
  ForwardPositions?: ForwardPositions[];
  OptionPositions?: OptionPositions[];
  StockLendingPositions?: StockLendingPositions[];
  StockPositions?: StockPositions[];
  CollateralPositions?: CollateralPositions[];
  StructuredProducts?: StructuredProducts[];
  CetipOptionPosition?: CetipOptionPosition[];
  PortfolioInvestments?: PortfolioInvestments[];
}

export interface Derivative {
  NDFPosition?: NDFPosition[];
  BMFFuturePosition?: BMFFuturePosition[];
  BMFOptionPosition?: BMFOptionPosition[];
  CetipOptionPosition?: CetipOptionPosition[];
  SwapPosition?: SwapPosition[];
}

export interface FixedIncomeStructuredNote {
  Issuer?: string;
  IssueDate?: string;
  MaturityDate?: string;
  ReferenceIndexName?: string;
  ReferenceIndexValue?: string;
  Quantity?: string;
  CostPrice?: string;
  Price?: string;
  InitialInvestmentValue?: string;
  GrossValue?: string;
  NetValue?: string;
  AccountingGroupCode?: string;
  IOFTax?: string;
  IncomeTax?: string;
  SecurityCode?: string;
  Ticker?: string;
  Yield?: string;
  YieldToMaturity?: string;
  FantasyName?: string;
  InterfaceDate?: string;
  PriceIncomeTax?: string;
  PriceVirtualIOF?: string;
  DateTimeUpdate?: string;
  Description?: string;
  CetipCode?: string;
}

export interface PayableReceivables {
  Credit?: Credit[];
}

export interface PendingSettlements {
  FixedIncome?: FixedIncome1[];
  InvestmentFund?: InvestmentFund1[];
  Equities?: Equities1[];
  Derivative?: Derivative1[];
  Pension?: Pension[];
  Others?: Others[];
}

export interface CryptoCoins {
  quantity?: string;
  financial?: string;
  grossFinancial?: string;
  financialClosing?: string;
  grossFinancialClosing?: string;
  costBasis?: string;
  positionDate?: string;
  updatedDate?: string;
  puClosing?: string;
  marketPrice?: string;
  incomeTax?: string;
  iofTax?: string;
  asset?: CryptoAsset;
  acquisitions?: CryptoAcquisition[];
}

export interface Cash {
  CashCollateral?: CashCollateral[];
  CurrentAccount?: CurrentAccount;
  CashInvested?: CashInvested[];
}

export interface CashCollateralRoot {
  BlockedMethod?: string;
  FinancialValue?: string;
  ReserveType?: string;
  Protocol?: string;
  PositionDate?: string;
}

export interface Precatories {
  IssueDate?: string;
  Quantity?: string;
  GrossValue?: string;
  CostPrice?: string;
  MarketPrice?: string;
  InvestedValue?: string;
  Asset?: PrecatoryAsset;
  Acquisitions?: PrecatoryAcquisition[];
  Scenarios?: PrecatoryScenario[];
}

export interface PrecatoriesCR {
  IssueDate?: string;
  Quantity?: string;
  GrossValue?: string;
  CostPrice?: string;
  MarketPrice?: string;
  InvestedValue?: string;
  PositionDate?: string;
  Asset?: PrecatoryAsset;
}

export interface Position {
  ContractVersion?: string;
  AccountNumber?: string;
  Agency?: string;
  PositionDate?: string;
  TotalAmount?: string;
  SummaryAccounts?: SummaryAccount[];
  InvestmentFund?: InvestmentFund[];
  FixedIncome?: FixedIncome[];
  InvestmentFundCotaCetipada?: InvestmentFundCotaCetipada[];
  Credits?: Credits[];
  PensionInformations?: PensionInformations[];
  Commodity?: Commodity[];
  Equities?: Equities[];
  Derivative?: Derivative[];
  FixedIncomeStructuredNote?: FixedIncomeStructuredNote[];
  PayableReceivables?: PayableReceivables[];
  PendingSettlements?: PendingSettlements[];
  CryptoCoins?: CryptoCoins[];
  Cash?: Cash[];
  CashCollateralRoot?: CashCollateralRoot[];
  Precatories?: Precatories[];
  PrecatoriesCR?: PrecatoriesCR[];
}

export interface PositionData {
  AccountNumber?: string;
  PositionDate?: string;
  Position?: Position;
}

export interface PositionDownloadData {
  url?: string;
  dateTime?: string;
  numberOfAccounts?: number;
  fileSize?: number;
}
