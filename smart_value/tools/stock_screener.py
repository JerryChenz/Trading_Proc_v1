import smart_value.stock
import pandas as pd
import pathlib

'''
Two ways to create a screener:
1. Create a filter while gathering the data.
2. Collect data & filter based on multiple criteria afterwards. (preferred and used here)
'''


# Step 1: Collect data
def collect_data(tickers, source):
    """Return the stock data in the screener format above and appends to the summary.

    :param tickers: a list of tickers to screen through
    :param source: "yf" chooses yahoo finance
    """

    summary = None
    for ticker in tickers:
        company = smart_value.stock.Stock(ticker, source)
        new_row = company.present_data()
        if summary is None:
            data = new_row
        else:
            summary = pd.concat([summary, new_row])
        print(ticker + ' added.')

    # export the summary
    cwd = pathlib.Path.cwd().resolve()
    monitor_folder = cwd / 'financial_models' / 'Opportunities' / 'Monitor'
    summary.to_csv(monitor_folder / 'screener_summary.csv')


# Step 2: filter
def load_filters(csv_file):
    """Filter the data sorted in csv based on multiple criteria.

    :param csv_file: Collected data in csv format
    :return: the list of screener result
    """

    df = pd.read_csv(csv_file)
    capitalization = df['Price'] * df['Shares']
    enterprise_value = capitalization
    liquidity_coverage_ratio = 0
    current_ratio = df['CurrentAssets'] / df['CurrentLiabilities']

    condition_1 = df['Cash'] > df['Debt']
