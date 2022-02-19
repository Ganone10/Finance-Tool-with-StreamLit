import pandas as pd
import numpy as np
from math import exp, log, sqrt
import datetime
import yfinance as yf

global ticker_1
global Adj_close_1


def already_search(ticker=None, Adj_close=None):
    ticker_1 = ticker
    Adj_close_1 = Adj_close
    return ticker_1, Adj_close_1


def get_stock_and_display(ticker):
    start_date = datetime.datetime(2021, 1, 1)
    end_date = datetime.datetime(2022, 1, 21)
    Adj_Close = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
    Adj_Close = Adj_Close.rename({'Adj Close': ticker}, axis=1)
    return Adj_Close


def norm_pdf(x):
    """
    Standard normal probability density function
    """
    return (1.0 / ((2 * np.pi) ** 0.5)) * exp(-0.5 * x * x)


def norm_cdf(x):
    """
    An approximation to the cumulative distribution
    function for the standard normal distribution:
    N(x) = \frac{1}{sqrt(2*\pi)} \int^x_{-\infty} e^{-\frac{1}{2}s^2} ds
    """
    k = 1.0 / (1.0 + 0.2316419 * x)
    k_sum = k * (0.319381530 + k * (-0.356563782 + k * (1.781477937 + k * (-1.821255978 + 1.330274429 * k))))
    if x >= 0.0:
        return 1.0 - (1.0 / ((2 * np.pi) ** 0.5)) * exp(-0.5 * x * x) * k_sum
    else:
        return 1.0 - x.norm_cdf(-x)


def d_j(j, S, K, r, v, T):
    """
    d_j = \frac{log(\frac{S}{K})+(r+(-1)^{j-1} \frac{1}{2}v^2)T}{v sqrt(T)}
    """
    return (log(S / K) + (r + ((-1) ** (j - 1)) * 0.5 * v * v) * T) / (v * (T ** 0.5))


def vanilla_call_price(S, K, r, v, T):
    """
    Price of a European call option struck at K, with
    spot S, constant rate r, constant vol v (over the
    life of the option) and time to maturity T
    """
    return S * norm_cdf(d_j(1, S, K, r, v, T)) - K * exp(-r * T) * norm_cdf(d_j(2, S, K, r, v, T))


def vanilla_put_price(S, K, r, v, T):
    """
    Price of a European put option struck at K, with
    spot S, constant rate r, constant vol v (over the
    life of the option) and time to maturity T
    """
    return -S * norm_cdf(-d_j(1, S, K, r, v, T)) + K * exp(-r * T) * norm_cdf(-d_j(2, S, K, r, v, T))


def monte_carlo(prices):
    returns = prices.pct_change()

    last_price = prices[-1]

    # Number of Simulations
    num_simulations = 20
    num_days = 250

    simulation_df = pd.DataFrame()

    for x in range(num_simulations):
        count = 0
        daily_vol = returns.std()
        price_series = []
        price = last_price * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)
        for y in range(num_days):
            if count == 251:
                break
            price = price_series[count] * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)
            count += 1
        simulation_df[x] = price_series
    return simulation_df


def cagr(start_value, end_value, num_periods):
    return (end_value / start_value) ** (1 / (num_periods - 1)) - 1
