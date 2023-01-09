# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 17:00:50 2023

@author: ronit
"""

import streamlit as st

def Forecastfordays():
    import plotly.graph_objects as go
    from prophet import Prophet
    from prophet.plot import plot_plotly
    from yahoo_fin.stock_info import get_data
    import datetime
    
    
    today = datetime.date.today()
    before = today - datetime.timedelta(days=500)
    start_date = st.sidebar.date_input('Start date', before)
    end_date = st.sidebar.date_input('End date', today)
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.sidebar.error('Error: End date must fall after start date.')
        
    
    st.title('Stock Forecast')
    st.title("![Alt Text](https://i.imgur.com/sNL8QOK.jpg)")

    stocks = (get_data("RELIANCE.NS",start_date="01/01/2015",end_date="04/01/2023",index_as_date=True,interval="1d"))
    @st.cache
    def load_data(ticker):
        data = stocks.drop('ticker',axis=1)
        data.reset_index(inplace=True)
        data.dropna()
        return data
    
    data_load_state = st.text('Loading data...')
    data = load_data(stocks)
    data_load_state.text('Loading data... done!')

    st.subheader('Raw data')
    st.write(data.tail())


    # Plot raw data
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['index'], y=data['open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['index'], y=data['close'], name="stock_close"))
        fig.update_layout(autosize=False,width=1000,height=600)
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

        stk = data
        stk = stk[['open','close']]
        st.write('Difference between Open and Close Price')    
        st.bar_chart(stk, width=1500,height=400)

    plot_raw_data()
    
    def main():
        days = st.slider('days of predictions:', 1, 31)
        period = days*1
            
        data_pred1 = data[['index','close']]
        data_pred1=data_pred1.rename(columns={"index": "ds", "close": "y"})
        # code for facebook prophet prediction

        m2 = Prophet()
        m2.fit(data_pred1)
        future = m2.make_future_dataframe(periods=period)
        forecast1 = m2.predict(future)
        forecast1

        #plot forecast
        fig3 = plot_plotly(m2, forecast1)
        st.write('Forecasting closing of stock value for a period of: '+str(days)+'days')
        st.plotly_chart(fig3)

        #plot component wise forecast
        st.write("Component wise forecast")
        fig4 = m2.plot_components(forecast1)
        st.write(fig4)
        
    if __name__ == '__main__':
        main()
    
def Forecastforyears():
    from ta.trend import MACD
    from ta.momentum import RSIIndicator
    from prophet import Prophet
    from prophet.plot import plot_plotly
    from yahoo_fin.stock_info import get_data
    import datetime

    def main():
        today = datetime.date.today()
        before = today - datetime.timedelta(days=500)
        start_date = st.sidebar.date_input('Start date', before)
        end_date = st.sidebar.date_input('End date', today)
        if start_date < end_date:
            st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
        else:
            st.sidebar.error('Error: End date must fall after start date.')
            

        st.title('Stock Forecast App')

        stocks = (get_data("RELIANCE.NS",start_date="01/01/2015",end_date="04/01/2023",index_as_date=True,interval="1d"))

        years = st.slider('years of prediction:', 1, 10)
        period = years*365

        @st.cache
        def load_data(ticker):
            data = stocks.drop('ticker',axis=1)
            data.reset_index(inplace=True)
            data.dropna()
            return data

        data = load_data(stocks)
        # preparing the data for Facebook-Prophet.

        data_pred = data[['index','close']]
        data_pred=data_pred.rename(columns={"index": "ds", "close": "y"})


        #Moving Average Convergence Divergence
        def macd_plot():
            macd = MACD(data['close']).macd()
            st.write('Stock Moving Average Convergence Divergence (MACD)= Close')
            st.area_chart(macd)
            
            
        macd_plot()


        # Resistence Strength Indicator
        def RSI_plot():
            rsi = RSIIndicator(data['close']).rsi()
            st.write('Resistence Strength Indicator (RSI)= Close')
            st.line_chart(rsi)
        
            
        RSI_plot()

        # code for facebook prophet prediction

        m = Prophet()
        m.fit(data_pred)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)


        #plot forecast
        fig1 = plot_plotly(m, forecast)
        if st.checkbox('Show forecast data'):
            st.subheader('forecast data')
            st.write(forecast)
        st.write('Forecasting closing of stock value for a period of: '+str(years)+'years')
        st.plotly_chart(fig1)

        #plot component wise forecast
        st.write("Component wise forecast")
        fig2 = m.plot_components(forecast)
        st.write(fig2)
    

    if __name__ == '__main__':
        main()

page_names_to_funcs = {
    "page1": Forecastfordays,
    "page2": Forecastforyears,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
