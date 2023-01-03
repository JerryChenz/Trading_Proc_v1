from smart_value.asset import *
from smart_value.financial_data import yahoo_data as yh
from smart_value.financial_data import exchange_rate as fx
import pandas as pd


class Stock(Asset):
    """a type of Securities"""

    def __init__(self, asset_code, source="yf"):
        """
        :param asset_code: string ticker of the stock
        :param source: "yf" chooses yahoo finance
        """
        super().__init__(asset_code)

        self.invest_horizon = 3  # 3 years holding period for stock by default
        self.report_currency = None
        self.is_df = None
        self.bs_df = None # annual data, latest quarter data needed
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

        ticker_data = yh.Financials(self.asset_code)

        self.name = ticker_data.name
        self.price = ticker_data.price
        self.exchange = ticker_data.exchange
        self.shares = ticker_data.shares
        self.report_currency = ticker_data.report_currency
        self.fx_rate = fx.get_forex_rate(self.report_currency, self.price[1])
        self.periodic_payment = ticker_data.dividends
        self.is_df = ticker_data.income_statement
        self.bs_df = ticker_data.balance_sheet
        self.last_fy = ticker_data.balance_sheet.columns[0]

    def present_data(self):
        """Return a summary of all the key stock data.

        :return: All key stock data in one DataFrame
        """

        # balance sheet and income statement information
        current_bs = self.bs_df.iloc[:, :1]
        current_is = self.is_df.iloc[:, :1]
        # concat 2 Series column-wise
        stock_summary = pd.concat([current_bs, current_is]).T
        # transpose the DataFrame to one row
        stock_summary.transpose()
        # rename the column names to prevent KeyError due to different data sources
        stock_summary.columns = ['TotalAssets', 'CurrentAssets','CurrentLiabilities',
                                 'CurrentDebtAndCapitalLeaseObligation','CurrentCapitalLeaseObligation',
                                 'LongTermDebtAndCapitalLeaseObligation','LongTermCapitalLeaseObligation',
                                 'TotalEquityGrossMinorityInterest','MinorityInterest','CashAndCashEquivalents',
                                 'OtherShortTermInvestments','InvestmentProperties','LongTermEquityInvestment',
                                 'InvestmentinFinancialAssets','NetPPE','TotalRevenue','CostOfRevenue',
                                 'SellingGeneralAndAdministration','InterestExpense','NetIncomeCommonStockholders']
        # ticker and dividend
        stock_summary.insert(loc=0, column='Ticker', value=self.asset_code)
        stock_summary['Name'] = self.name
        stock_summary['Exchange'] = self.exchange
        stock_summary['Price'] = self.price[0]
        stock_summary['Price_currency'] = self.price[1]
        stock_summary['Shares'] = self.shares
        stock_summary['Reporting_Currency'] = self.report_currency
        stock_summary['Fx_rate'] = self.fx_rate
        stock_summary['Last_fy'] = self.last_fy
        stock_summary['Dividend'] = self.periodic_payment

        return stock_summary.set_index('Ticker')

    def csv_statements(self, df):
        """Export the DataFrame in csv format.

        :param df: a DataFrame containing stock data
        """

        df.to_csv(f'{self.asset_code}_{df.name}.csv', sep=',', encoding='utf-8')
