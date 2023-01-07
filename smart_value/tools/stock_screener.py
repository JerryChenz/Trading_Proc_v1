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
screener_folder = cwd / 'financial_models' / 'Opportunities' / 'Screener'
json_dir = screener_folder / 'data'


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

    json_pattern = os.path.join(json_dir, '*.json')
    files = glob.glob(json_pattern)

    dfs = []  # an empty list to store the data frames
    for file in files:
        data = pd.read_json(file)  # read data frame from json file
        dfs.append(data.transpose())  # append the data frame to the list

    df = pd.concat(dfs, ignore_index=False)  # concatenate all the data frames in the list.
    df = df[
        ['Ticker', 'Name', 'Exchange', 'Price', 'Price_currency', 'Shares', 'Reporting_Currency', 'Fx_rate',
         'Dividend', 'Buyback', 'Last_fy', 'TotalAssets', 'CurrentAssets', 'CurrentLiabilities',
         'CurrentDebtAndCapitalLeaseObligation', 'CurrentCapitalLeaseObligation',
         'LongTermDebtAndCapitalLeaseObligation', 'LongTermCapitalLeaseObligation',
         'TotalEquityGrossMinorityInterest', 'MinorityInterest', 'CashAndCashEquivalents',
         'OtherShortTermInvestments', 'InvestmentProperties', 'LongTermEquityInvestment',
         'InvestmentinFinancialAssets', 'NetPPE', 'TotalRevenue', 'CostOfRevenue', 'GrossMargin',
         'SellingGeneralAndAdministration', 'EBIT', 'EbitMargin', 'InterestExpense', 'NetIncomeCommonStockholders',
         'NetMargin', 'Avg_Gross_margin', 'Avg_sales_growth', 'Avg_ebit_margin', 'Avg_ebit_growth',
         'Avg_net_margin', 'Avg_NetIncome_growth',
         'Years_of_data']].set_index('Ticker')
    df.to_csv(screener_folder / 'screener_summary.csv')

# Step 2: filter done using ipynb with Jupyter Notebook
