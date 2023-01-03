import smart_value.stock
import pandas as pd
import pathlib

'''
Two ways to create a screener:
1. Create a filter while gathering the data.
2. Collect data & filter based on multiple criteria afterwards. (preferred and used here)
'''

class StockScreener:
    """A Python stock screener"""

    def __init__(self, tickers, source = "yf"):
        """
        :param tickers: a list of tickers to screen through
        """
        self.tickers = tickers
        # Output in a dataframe
        self.summary = None
        self.source = source
        self.condition_1 = True
        self.condition_2 = True
        self.condition_3 = True
        self.condition_4 = True
        self.condition_5 = True

    def collect_data(self, source):
        """Return the stock data in the screener format above and appends to the summary."""

        data = None
        for ticker in self.tickers:
            company = smart_value.stock.Stock(ticker, source)
            new_row = company.present_data()
            if data is None:
                data = new_row
            else:
                self.summary = pd.concat([data,new_row])
            print(ticker + ' added.')

        cwd = pathlib.Path.cwd().resolve()
        monitor_folder = cwd / 'financial_models' / 'Opportunities' / 'Monitor'
        self.summary.to_csv(monitor_folder / 'screener_summary.csv')

    def load_filters(self, csv_file):
        """Filter the data sorted in csv based on multiple criteria.

        :param csv_file: Collected data in csv format
        :return: the list of screener result
        """

        df = pd.read_csv(csv_file)
        enterprise_value = 0
        liquidity_coverage_ratio = 0
        current_ratio = df['CurrentAssets']/df['CurrentLiabilities']


        self.condition_1 = df['Cash'] > df['Debt']
