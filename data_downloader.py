
import yfinance as yahooFinance
import pandas as pd
import csv

# GetAlteryxInformation = yahooFinance.Ticker("T")
# ticker_historical_data = yahooFinance.download(tickers="T")
# print(type(ticker_historical_data))
# ticker_historical_data.to_csv('At_&_Tdata.csv')


# print(GetAlteryxInformation.history(period="max"))
csco = yahooFinance.Ticker("CSCO")
# print(T.news)
# csco.balancesheet.to_csv('Cisco_data/balancesheet.csv')
# # T.earnings_trend.to_csv('T_earnings_trend.csv')
# T.cash_flow.to_csv('T_cash_flow.csv')
#T.capital_gains.to_csv('T_capital_gains.csv')
# T.dividends.to_csv('T_Dividends.csv')

# csco.get_earnings.to_csv('Cisco_data/earnings.csv')
df = pd.DataFrame(csco.history())
df.to_csv('Cisco_data/history.csv')
print(df.head(5))
# print(dir(csco))