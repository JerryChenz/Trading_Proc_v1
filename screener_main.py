import smart_value.tools.stock_screener as screener


def screener_data(companies):
    """Return the company data from the screener

    :param companies: list of tickers
    :return: company data
    :rtype: DataFrame
    """

    s = screener.StockScreener(companies, "yf")
    s.collect_data(s.source)
    print(s.summary)

if __name__ == '__main__':
    tickers = ['0806.HK', '1475.HK']
    screener_data(tickers)
