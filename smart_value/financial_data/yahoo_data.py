import pandas as pd
from yfinance import Ticker
from datetime import datetime


class Financials:
    """Retrieves the data from YH Finance API and yfinance package"""

    def __init__(self, ticker):
        self.ticker = ticker
        # yfinance
        try:
            self.stock_data = Ticker(self.ticker)
        except KeyError:
            print("Check your stock ticker")
        self.name = self.stock_data.info['shortName']
        self.price = [self.stock_data.info['currentPrice'], self.stock_data.info['currency']]
        self.exchange = self.stock_data.info['exchange']
        self.shares = self.stock_data.info['sharesOutstanding']
        self.report_currency = self.stock_data.info['financialCurrency']
        self.next_earnings = pd.to_datetime(datetime.fromtimestamp(self.stock_data.info['mostRecentQuarter'])
                                            .strftime("%Y-%m-%d")) + pd.DateOffset(months=6)
        self.annual_bs = self.get_balance_sheet("annual")
        self.quarter_bs = self.get_balance_sheet("quarter")
        self.income_statement = self.get_income_statement()
        self.cash_flow = self.get_cash_flow()
        try:
            self.dividends = -int(self.cash_flow.loc['CommonStockDividendPaid'][0]) / self.shares
        except ZeroDivisionError:
            self.dividends = 0

    def get_balance_sheet(self, option):
        """Returns a DataFrame with selected balance sheet data"""

        dummy = {
            "Dummy": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]}

        if option == "annual":
            balance_sheet = self.stock_data.get_balance_sheet()
            bs_index = ['TotalAssets', 'CurrentAssets', 'CurrentLiabilities', 'CurrentDebtAndCapitalLeaseObligation',
                        'CurrentCapitalLeaseObligation', 'LongTermDebtAndCapitalLeaseObligation',
                        'LongTermCapitalLeaseObligation', 'TotalEquityGrossMinorityInterest', 'MinorityInterest',
                        'CashAndCashEquivalents', 'OtherShortTermInvestments', 'InvestmentProperties',
                        'LongTermEquityInvestment', 'InvestmentinFinancialAssets', 'NetPPE']
        else:
            balance_sheet = self.stock_data.quarterly_balance_sheet
            # Quarter balance sheet index is different from annual bs
            bs_index = ['Total Assets', 'Current Assets', 'Current Liabilities',
                      'Current Debt And Capital Lease Obligation',
                      'Current Capital Lease Obligation',
                      'Long Term Debt And Capital Lease Obligation',
                      'Long Term Capital Lease Obligation',
                      'Total Equity Gross Minority Interest',
                      'MinorityInterest', 'Cash And Cash Equivalents',
                      'Other Short Term Investments', 'Investment Properties',
                      'Long Term Equity Investment', 'Investmentin Financial Assets', 'Net PPE']
        # Start of Cleaning: make sure the data has all the required indexes
        dummy_df = pd.DataFrame(dummy, index=bs_index)
        clean_bs = dummy_df.join(balance_sheet)
        bs_df = clean_bs.loc[bs_index]
        # Ending of Cleaning: drop the dummy column after join
        bs_df.drop('Dummy', inplace=True, axis=1)

        return bs_df.fillna(0)

    def get_income_statement(self):
        """Returns a DataFrame with selected income statement data"""

        income_statement = self.stock_data.get_income_stmt()
        # Start of Cleaning: make sure the data has all the required indexes
        dummy = {"Dummy": [None, None, None, None, None]}
        is_index = ['TotalRevenue', 'CostOfRevenue', 'SellingGeneralAndAdministration', 'InterestExpense',
                    'NetIncomeCommonStockholders']
        dummy_df = pd.DataFrame(dummy, index=is_index)
        clean_is = dummy_df.join(income_statement)
        is_df = clean_is.loc[is_index]
        # Ending of Cleaning: drop the dummy column after join
        is_df.drop('Dummy', inplace=True, axis=1)

        return is_df.fillna(0)

    def get_cash_flow(self):
        """Returns a DataFrame with selected Cash flow statement data"""

        cash_flow = self.stock_data.get_cashflow()
        # Start of Cleaning: make sure the data has all the required indexes
        dummy = {"Dummy": [None]}
        cf_index = ['CommonStockDividendPaid']
        dummy_df = pd.DataFrame(dummy, index=cf_index)
        clean_cf = dummy_df.join(cash_flow)
        cf_df = clean_cf.loc[cf_index]
        # Ending of Cleaning: drop the dummy column after join
        cf_df.drop('Dummy', inplace=True, axis=1)

        return cf_df.fillna(0)