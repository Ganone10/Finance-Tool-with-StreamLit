import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from pricing_simulator import *
from BSM import Pricer
from fun_finance import *

l_suggestions = ["AAPL", "NVDA"]

## Set up of Streamlit Interface
st.title('Financial Dashboard')
# ticker_input = st.text_input('Choose your Type of Option:')
# search_button = st.button('Search')
add_selectbox = st.sidebar.selectbox(
    "What option do you want to use?",
    ("Portfolio simulation","Pricing Simulator", "Stocks Viz","Credit Analysis")
    #("Pricing Simulator", "Stocks Viz","Risk Management & Diversification","Commodities")
)
if add_selectbox == 'Pricing Simulator':
    option = st.selectbox('What kind of option whould you like to priced?', ('European', 'American'))
    if option == 'American':
        option_c_or_p = st.selectbox('Call or Put', ('Call', 'Put'))
        st.header('Enter parameters for your option')
        c1, c2, c3, c4 = st.columns(4)
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
        c1, c2, c3, c4 = st.columns(4)
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            S = st.text_input('Stock Price: ')
        with c2:
            K = st.text_input('Strike Price: ')
        with c3:
            T = st.text_input('Maturity Time: ')
        with c4:
            sigma = st.text_input('volatility: ')
        with c5:
            r = st.text_input('Discount rate: ')
        with c6:
            d = st.text_input('Dividen paid: ')

        button = st.button('Compute')
        if button:
            class Call_Put(Pricer):
                pass
            print(type(float(S)))
            print(S)
            pricer = Call_Put("MC.PA", float(S), float(K), float(T), float(sigma), float(r), float(d))
            if option_c_or_p == 'Call':
                st.write('Price for this option: ', pricer.CALL())
            else:
                st.write('Price for this option: ', pricer.PUT())

elif add_selectbox == "Stocks Viz":
    #def exists_variables():
        #if "Adj_Close" not in st.session_state:
        #    print("0")
        #else:
            #st.multiselect("Options: ", ['SMA', 'L&U BANDS', 'Other'],st.session_state["options"])
            #if 'SMA' in st.session_state["options"]:
            #    Merged = pd.merge(st.session_state['Adj_Close'], st.sessions_state["SMA"], on="Date")
            #    Merged = Merged.rename({'Adj Close_x': ticker, 'Adj Close_y': ticker + ' SMA 10'}, axis=1)
            #    st.header('Stock Price evolution:')
            #    st.line_chart(Merged, width=200, height=400, use_container_width=True)
            #else:
            #st.header('Stock Price evolution:')
            #st.line_chart(st.session_state["Adj_Close"], width=200, height=400, use_container_width=True)
            #st.header('Return of the Stock:')
            #st.line_chart(st.session_state["LOG_RETURN"], width=200, height=400, use_container_width=True)
            #st.header('Monte Carlo simulation over 2 years:')
            #MC = monte_carlo(st.session_state["Adj_Close"])
            #st.line_chart(MC, width=200, height=400, use_container_width=True)
    def exists_variables():
        if "Adj_Close" not in st.session_state:
            print('0')
        else:
            #st.multiselect("Options: ", ['SMA', 'L&U BANDS', 'Other'],st.session_state["options"])
            if 'SMA' in st.session_state["options"]:
                Merged = pd.merge(st.session_state['Adj_Close'], st.sessions_state["SMA"], on="Date")
                Merged = Merged.rename({'Adj Close_x': ticker, 'Adj Close_y': ticker + ' SMA 10'}, axis=1)
                st.header('Stock Price evolution:')
                st.line_chart(Merged, width=200, height=400, use_container_width=True)
            else:
                st.header('Stock Price evolution:')
                st.line_chart(st.session_state["Adj_Close"], width=200, height=400, use_container_width=True)
            st.header('Return of the Stock:')
            st.line_chart(st.session_state["LOG_RETURN"], width=200, height=400, use_container_width=True)
            st.header('Monte Carlo simulation over 2 years:')
            MC = monte_carlo(st.session_state["Adj_Close"])
            st.line_chart(MC, width=200, height=400, use_container_width=True)
    st.header("Stocks Viz")
    ticker = st.text_input("Enter a ticker")
    button = st.button('Enter')
    #exists_variables()
    if ticker != '':
        l_suggestions = search_company(ticker)
    if button:

    # Computation Stock charts, Log returns, Monte Carlo,
        Adj_Close = get_stock_and_display(ticker)
        LOG_RETURN = Adj_Close.pct_change()
        MC = monte_carlo(Adj_Close)

        articles = get_latest_news("a96775949a0543ceaf31ed99fef7a2a0", ticker)
        if articles:
            st.write(f"Top 5 most relevant articles related to {ticker}:")
            for index, article in enumerate(articles[:5], start=1):
                st.subheader(f"Article {index}: {article['title']}")
                st.write(f"Published at: {article['publishedAt']}")
                st.write(f"Source: {article['source']['name']}")
                st.write(f"URL: {article['url']}")
                st.write()
        def store_variables():
            if "Adj_Close" not in st.session_state:
                st.session_state["Adj_Close"]=Adj_Close
            #if "SMA" not in st.session_state:
            #    st.session_state["SMA"]=SMA
            #if "STD" not in st.session_state:
            #    st.session_state["STD"]=STD
            #if "UPPER_BAND" not in st.session_state:
            #    st.session_state["UPPER_BAND"]=UPPER_BAND
            #if "LOWER_BAND" not in st.session_state:
            #    st.session_state["LOWER_BAND"] = LOWER_BAND
            if "LOG_RETURN" not in st.session_state:
                st.session_state["LOG_RETURN"] = LOG_RETURN



        st.header('Stock Price evolution:')
        st.line_chart(Adj_Close, width=200, height=400, use_container_width=True)
        st.header('Return of the Stock:')
        st.line_chart(LOG_RETURN, width=200, height=400, use_container_width=True)
        st.header('Monte Carlo simulation over 2 years:')
        st.line_chart(MC, width=200, height=400, use_container_width=True)
elif add_selectbox=="Portfolio simulation":
    st.header('Portfolio composition:')
    pie_chart = draw_pie_charts()
    pie_chart.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(pie_chart)
    stocks_hist = get_stock_and_display_multi(['HYG', 'TTE.PA', 'ORA.PA'])
    st.line_chart(stocks_hist)
elif add_selectbox=="Credit Analysis":
    st.header('Credit Analysis review:')
    ticker_credit = st.text_input("Enter a ticker")
    button_credit = st.button('Enter')