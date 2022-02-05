import streamlit as st
import yfinance as yf
import pandas as pd
from math import exp, log, sqrt
import numpy as np
import datetime


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


## Set up of Streamlit Interface
st.title('Financial Dashboard')
# ticker_input = st.text_input('Choose your Type of Option:')
# search_button = st.button('Search')
add_selectbox = st.sidebar.selectbox(
    "What option do you want to use?",
    ("Pricing Simulator", "Stocks Viz")
)
if add_selectbox == 'Pricing Simulator':
    option = st.selectbox('What kind of option whould you like to priced?', ('European', 'American'))
    if option == 'American':
        option_c_or_p = st.selectbox('Call or Put', ('Call', 'Put'))
        st.header('Enter parameters for your option')
        c1, c2, c3, c4 = st.beta_columns(4)
        with c1:
            K = st.text_input('Strike Price: ')
        with c2:
            T = st.text_input('Maturity Time: ')
        with c3:
            S = st.text_input('Stock Price: ')
        with c4:
            r = st.text_input('Discount rate: ')
        button = st.button('Compute')
        if button:
            S = float(S)
            K = float(K)
            T = int(T)
            r = float(r)
            if option_c_or_p == 'Call':
                st.write('Price for this option: ', vanilla_call_price(S, K, r, 0.088864, T))
            else:
                st.write('Price for this option: ', vanilla_put_price(S, K, r, 0.088864, T))
    elif option == 'European':
        option_c_or_p = st.selectbox('Call or Put', ('Call', 'Put'))
        st.header('Enter parameters for your option')
        c1, c2, c3, c4 = st.beta_columns(4)
        with c1:
            K = st.text_input('Strike Price: ')
        with c2:
            T = st.text_input('Maturity Time: ')
        with c3:
            S = st.text_input('Stock Price: ')
        with c4:
            r = st.text_input('Discount rate: ')
        button = st.button('Compute')
        if button:
            st.write("In course of production")

elif add_selectbox == "Stocks Viz":
    st.sidebar.multiselect('What option do you want to add', ['SMA', 'UP&Lo BAND', 'Other'])
    st.header("Stocks Viz")
    ticker = st.text_input("Enter a ticker")
    button = st.button('Enter')
    if button:
        start_date = datetime.datetime(2021, 1, 1)
        end_date = datetime.datetime(2022, 1, 21)
        Adj_Close = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
        Adj_Close = Adj_Close.rename({'Adj Close': ticker}, axis=1)
        ## Compute for the widget options
        SMA = Adj_Close.rolling(window=10).mean()
        STD = Adj_Close.rolling(window=10).std()
        UPPER_BAND = SMA + 3 * STD
        LOWER_BAND = SMA - 3 * STD
        LOG_RETURN = Adj_Close.pct_change()
        print(LOG_RETURN.head())
        # Merged = pd.merge(Adj_Close, SMA, on="Date")
        # Merged = Merged.rename({'Adj Close_x': ticker, 'Adj Close_y': ticker + ' SMA 10'}, axis=1)  # new method
        # Merged_1 = pd.merge(Merged,UPPER_BAND,on="Date")
        # Merged_1 = Merged_1.rename({'Adj Close_x': ticker, 'Adj Close_y': ticker + ' SMA 10','Adj Close':ticker+'UpperBand'}, axis=1)  # new method
        # print(Merged_1.head())
        # Merged_2 = pd.merge(Merged_1,LOWER_BAND,on="Date")
        # Merged_2 = Merged_2.rename({'Adj Close':ticker+'LowerBand'}, axis=1)
        # print(Merged_2.head(20))
        st.header('Stock Price evolution:')
        st.line_chart(Adj_Close, width=200, height=400, use_container_width=True)
        st.header('Return of the Stock:')
        st.line_chart(LOG_RETURN, width=200, height=400, use_container_width=True)
        st.header('Monte Carlo simulation over 2 years:')
        MC = monte_carlo(Adj_Close)
        st.line_chart(MC,width=200, height=400, use_container_width=True)