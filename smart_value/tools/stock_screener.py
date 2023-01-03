import smart_value.stock
import pandas as pd

'''
Two ways to create a screener:
1. Create a filter while gathering the data.
2. Collect data & filter based on multiple criteria afterwards. (preferred and used here)
'''


def enterprise_value(stock):
    """Return the stock's Enterprise value.

    :param stock: Stock object
    :return: the Enterprise Value
    :rtype: integer
    """

    ev = 1

    return ev


def liquidity_coverage(stock):
    """Return the stock's Liquidity Coverage ratio.

    :param stock: Stock object
    :return: the Liquidity Coverage ratio
    :rtype: Integer
    """

    lcr = 1

    return lcr


class StockScreener:
    """A Python stock screener"""

    def __init__(self, tickers):
        """
        :param tickers: a list of tickers to screen through
        """
        self.tickers = tickers
        # Output in a dataframe
        self.summary = pd.DataFrame(columns=['Ticker', 'Market cap', 'Net income',
                                             'Cash', 'Debt', 'Investments', 'Enterprise value',
                                             'Forecasted growth', 'Dividend yield'])

    def collect_data(self):
        """Return the stock data in the screener format above and appends to the summary.

        :return: self.summary - the screener output
        :rtype: DataFrame
        """

        for ticker in self.tickers:
            try:
                company = smart_value.stock.Stock(ticker)
                # balance sheet information
                new_row = company.bs_df.iloc[:,:1]


                self.summary.append(new_row, ignore_index=True)
                print(ticker + ' added.')
            except:
                print(ticker + ': Something went wrong.')
        self.summary['PE'] = self.summary['Enterprise value'] / self.summary['Net income']
        self.summary['LCR'] = liquidity_coverage('')
        self.summary['PEG'] = self.summary['PE'] / self.summary['D+G']
        self.summary.to_csv('summary.csv')

        # insert the tickers list at the first column index in pandas
        self.summary.insert(loc=0, column='Ticker',value=self.tickers)

    def filter(self):
        """

        :return: the list of screener result
        """
        condition_1 = self.summary['Cash'] > self.summary['Debt']
