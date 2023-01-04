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
    :return: company summary on current data
    :rtype: DataFrame
    """

    summary = None
    for ticker in tickers:
        company = smart_value.stock.Stock(ticker, source)
        new_row = company.current_summary()
        if summary is None:
            summary = new_row
        else:
            summary = pd.concat([summary, new_row])
        print(ticker + ' added.')

    # export the summary
    cwd = pathlib.Path.cwd().resolve()
    monitor_folder = cwd / 'financial_models' / 'Opportunities' / 'Monitor'
    summary.to_csv(monitor_folder / 'screener_summary.csv')
    return summary


# Step 2: filter
def load_filters(csv_file):
    """Filter the data sorted in csv based on multiple criteria.

    :param csv_file: Collected data in csv format
    :return: the list of screener result
    """

    df = pd.read_csv(csv_file)
    # capitalization in reporting currency
    capitalization = df['Price'] * df['Shares'] * df['Fx_rate']
    print(capitalization)
    total_debt = df['CurrentDebtAndCapitalLeaseObligation'] + df['LongTermDebtAndCapitalLeaseObligation']
    print(total_debt)
    enterprise_value = capitalization + total_debt + df['MinorityInterest'] - df['CashAndCashEquivalents']
    # more easily realizable non-operating assets
    monetary_assets = df['OtherShortTermInvestments'] + df['InvestmentinFinancialAssets']
    # less easily realizable non-operating assets
    fixed_nonop_assets = (df['InvestmentProperties'] + df['LongTermEquityInvestment']) * 0.5
    # liquidity_coverage_ratio
    lcr = monetary_assets / df['CurrentLiabilities']
    current_ratio = df['CurrentAssets'] / df['CurrentLiabilities']

    # filter conditions
    condition_1 = df['CashAndCashEquivalents'] > df['CurrentDebtAndCapitalLeaseObligation']
    condition_2 = lcr >= 1

    print(df.loc[condition_1 & condition_2])
