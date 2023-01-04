import smart_value.stock
import pandas as pd
import pathlib
import time
import glob, os

'''
Two ways to create a screener:
1. Create a filter while gathering the data.
2. Collect data & filter based on multiple criteria afterwards. (preferred and used here)
'''

cwd = pathlib.Path.cwd().resolve()
json_dir = cwd / 'financial_models' / 'Opportunities' / 'Monitor' / 'data'

# Step 1: Collect data
def collect_data(tickers, source):
    """Collect a list of company data, then export json.

    :param tickers: a list of tickers to screen through
    :param source: "yf" chooses yahoo finance
    """

    # Collect the company data and export in json
    for ticker in tickers:
        try:
            company_data(ticker, source)
        except KeyError:
            print(f'{ticker} is not valid, skip')
            continue

        print(ticker + ' data added.')

    # export the json files and export the summary in DataFrame
    print("merging data...")
    merge_data()
    print("csv exported.")


def company_data(ticker, source):
    """Collect the company data, then export json.

    :param ticker: collect the data using string ticker
    :param source: "yf" chooses yahoo finance
    """

    # external API error re-try
    try_count = 0
    max_try = 10

    try:
        company = smart_value.stock.Stock(ticker, source)
        # export the summary
        new_row = company.current_summary().transpose()
        new_row.to_json(json_dir / f'{ticker} data.json')
    except IndexError:
        try_count += 1
        if try_count < max_try:
            print(f'external API error, will re-try {ticker} after 80 sec')
            time.sleep(80)
            print(f're-try {ticker}')
            company_data(ticker, source)
    except ValueError:
        try_count += 1
        if try_count < max_try:
            print(f'external API error, will re-try {ticker} after 120 sec')
            time.sleep(120)
            print(f're-try {ticker}')
            company_data(ticker, source)
    except TypeError:
        try_count += 1
        if try_count < max_try:
            print(f'external API error, will re-try {ticker} after 120 sec')
            time.sleep(120)
            print(f're-try {ticker}')
            company_data(ticker, source)


def merge_data():
    """Merge multiple JSON files into a pandas DataFrame, then export to csv"""

    monitor_folder = cwd / 'financial_models' / 'Opportunities' / 'Monitor'

    json_pattern = os.path.join(json_dir, '*.json')
    files = glob.glob(json_pattern)

    dfs = []  # an empty list to store the data frames
    for file in files:
        data = pd.read_json(file)  # read data frame from json file
        dfs.append(data.transpose())  # append the data frame to the list

    df = pd.concat(dfs, ignore_index=False) # concatenate all the data frames in the list.
    df = df[['Ticker','Name','Exchange','Price','Price_currency','Shares','Reporting_Currency','Fx_rate','Dividend',
             'Last_fy','TotalAssets', 'CurrentAssets', 'CurrentLiabilities',
             'CurrentDebtAndCapitalLeaseObligation', 'CurrentCapitalLeaseObligation',
             'LongTermDebtAndCapitalLeaseObligation', 'LongTermCapitalLeaseObligation',
             'TotalEquityGrossMinorityInterest', 'MinorityInterest', 'CashAndCashEquivalents',
             'OtherShortTermInvestments', 'InvestmentProperties', 'LongTermEquityInvestment',
             'InvestmentinFinancialAssets', 'NetPPE', 'TotalRevenue', 'CostOfRevenue',
             'SellingGeneralAndAdministration', 'InterestExpense', 'NetIncomeCommonStockholders']].set_index('Ticker')
    df.to_csv(monitor_folder / 'screener_summary.csv')

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
