from smart_value.asset import *
from smart_value.financial_data import yahoo_data as yf
from smart_value.financial_data import exchange_rate as fx
import pandas as pd


class Stock(Asset):
    """a type of Securities"""

    def __init__(self, asset_code, source="yf"):
        """
        :param asset_code: string ticker of the stock
        :param source: data source selector. "yf" selects yahoo finance
        """
        super().__init__(asset_code)

        self.invest_horizon = 3  # 3 years holding period for stock by default
        self.report_currency = None
        self.is_df = None
        self.annual_bs = None  # annual balance sheet data
        self.quarter_bs =None  # last quarter balance sheet data
        self.fx_rate = None
        self.source = source
        self.load_data()

    def load_data(self):
        """data source selector."""

        if self.source == "yf":
            self.load_from_yf()
        else:
            pass  # Other sources of data to-be-implemented

    def load_from_yf(self):
        """Scrap the financial_data from yfinance API"""

        ticker_data = yf.Financials(self.asset_code)

        self.name = ticker_data.name
        self.price = ticker_data.price
        self.exchange = ticker_data.exchange
        self.shares = ticker_data.shares
        self.report_currency = ticker_data.report_currency
        self.fx_rate = fx.get_forex_rate(self.report_currency, self.price[1])
        self.periodic_payment = ticker_data.dividends
        self.is_df = ticker_data.income_statement
        self.annual_bs = ticker_data.annual_bs
        self.quarter_bs = ticker_data.quarter_bs
        self.last_fy = ticker_data.annual_bs.columns[0]

    def current_summary(self):
        """Return a summary of all the key stock data.

        :return: All key stock data in one DataFrame
        """

        # balance sheet and income statement information
        current_bs = self.quarter_bs.iloc[:, :1]
        # standardize the column name to enable concat
        current_bs.columns = [self.last_fy]
        current_is = self.is_df.iloc[:, :1]
        # concat 2 Series column-wise
        stock_summary = pd.concat([current_bs, current_is]).T
        # transpose the DataFrame to one row
        stock_summary.transpose()
        # standardize the column names to prevent KeyError due to different data sources
        stock_summary.columns = ['TotalAssets', 'CurrentAssets', 'CurrentLiabilities',
                                 'CurrentDebtAndCapitalLeaseObligation', 'CurrentCapitalLeaseObligation',
                                 'LongTermDebtAndCapitalLeaseObligation', 'LongTermCapitalLeaseObligation',
                                 'TotalEquityGrossMinorityInterest', 'MinorityInterest', 'CashAndCashEquivalents',
                                 'OtherShortTermInvestments', 'InvestmentProperties', 'LongTermEquityInvestment',
                                 'InvestmentinFinancialAssets', 'NetPPE', 'TotalRevenue', 'CostOfRevenue',
                                 'SellingGeneralAndAdministration', 'InterestExpense', 'NetIncomeCommonStockholders']
        # ticker and dividend
        stock_summary.insert(loc=0, column='Ticker', value=self.asset_code)
        stock_summary.insert(loc=1, column='Name', value=self.name)
        stock_summary.insert(loc=2, column='Exchange', value=self.exchange)
        stock_summary.insert(loc=3, column='Price', value=self.price[0])
        stock_summary.insert(loc=4, column='Price_currency', value=self.price[1])
        stock_summary.insert(loc=5, column='Shares', value=self.shares)
        stock_summary.insert(loc=6, column='Reporting_Currency', value=self.report_currency)
        stock_summary.insert(loc=7, column='Fx_rate', value=self.fx_rate)
        stock_summary.insert(loc=8, column='Dividend', value=self.periodic_payment)
        stock_summary.insert(loc=9, column='Last_fy', value=self.last_fy)

        return stock_summary

    def csv_statements(self, df):
        """Export the DataFrame in csv format.

        :param df: a DataFrame containing stock data
        """

        df.to_csv(f'{self.asset_code}_{df.name}.csv', sep=',', encoding='utf-8')
