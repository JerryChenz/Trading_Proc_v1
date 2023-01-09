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
            company_data(ticker, source, 0)
        except KeyError:
            print(f'{ticker} is not valid, skip')
            continue

        print(ticker + ' data added.')

    # export the json files and export the summary in DataFrame
    print("merging data...")
    merge_data()
    print("csv exported.")


def company_data(ticker, source, attempt):
    """Collect the company data, then export json.

    :param attempt: try_count
    :param ticker: collect the data using string ticker
    :param source: "yf" chooses yahoo finance
    """

    # external API error re-try
    max_try = 10

    try:
        company = smart_value.stock.Stock(ticker, source)
        # export the summary
        new_row = company.current_summary().transpose()
        new_row.to_json(json_dir / f'{ticker} data.json')
        time.sleep(1.5)
    except IndexError:
        attempt += 1
        if attempt < max_try:
            print(f'external API error, will re-try {ticker} after 80 sec')
            time.sleep(80)
            print(f're-try {ticker}')
            company_data(ticker, source, attempt)
    except ValueError:
        attempt += 1
        if attempt < max_try:
            print(f'external API error, will re-try {ticker} after 120 sec')
            time.sleep(120)
            print(f're-try {ticker}')
            company_data(ticker, source, attempt)
    except TypeError:
        attempt += 1
        if attempt < max_try:
            print(f'external API error, will re-try {ticker} after 120 sec')
            time.sleep(120)
            print(f're-try {ticker}')
            company_data(ticker, source, attempt)
    except AttributeError:
        attempt += 1
        if attempt < max_try:
            print(f'external API error, will re-try {ticker} after 120 sec')
            time.sleep(120)
            print(f're-try {ticker}')
            company_data(ticker, source, attempt)


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
         'InvestmentinFinancialAssets', 'NetPPE', 'TotalRevenue', 'Avg_sales_growth', 'CostOfRevenue',
         'GrossMargin', 'Avg_Gross_margin', 'SellingGeneralAndAdministration',
         'EBIT', 'EbitMargin', 'Avg_ebit_margin', 'Avg_ebit_growth', 'InterestExpense',
         'NetIncomeCommonStockholders', 'NetMargin', 'Avg_net_margin', 'Avg_NetIncome_growth',
         'Years_of_data']].set_index('Ticker')
    df.to_csv(screener_folder / 'screener_summary.csv')

# Step 2: filter done using ipynb with Jupyter Notebook
