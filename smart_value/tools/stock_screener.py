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
    :rtype: integer
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
                new_row = {'Ticker': ticker,
                           'Market cap': capitalization,
                           'Cash': company.bs_df.iloc['CashAndCashEquivalents'],
                           'Debt': debt,
                           'Investments': investments,
                           'Enterprise value': ev,
                           'Net income': net_inc,
                           'Forecasted growth': forecasted_growth,
                           'Dividend yield': div_yield}

                self.summary.append(new_row, ignore_index=True)
                print(ticker + ' added.')
            except:
                print(ticker + ': Something went wrong.')
        self.summary['PE'] = self.summary['Enterprise value'] / self.summary['Net income']
        self.summary['LCR'] = liquidity_coverage('')
        self.summary['PEG'] = summary['PE'] / summary['D+G']
        self.summary.to_csv('summary.csv')

    def filter(self):
        """

        :return: the list of screener result
        """
        condition_1 = self.summary['Cash'] > self.summary['Debt']
