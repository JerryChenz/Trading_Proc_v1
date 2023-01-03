import smart_value.tools.stock_screener as screener

if __name__ == '__main__':
    tickers = ['0806.HK', '1475.HK']
    screener.StockScreener(tickers, "yf")