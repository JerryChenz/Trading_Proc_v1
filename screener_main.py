import smart_value.tools.stock_screener as screener


def screener_data():
    """Return the company data from the screener

    :param companies: list of tickers
    :return: company data
    :rtype: DataFrame
    """

    companies = ['0806.HK']
    return screener.collect_data(companies, "yf")

if __name__ == '__main__':

    print(screener_data())
