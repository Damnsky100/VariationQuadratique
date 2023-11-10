import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import os

# Set your path
dir_path = os.path.dirname(os.path.realpath(__file__))
chemin_relatif = "data2D/"
path = os.path.join(dir_path, chemin_relatif)

@st.cache
def load_data(year):
    data = pd.read_csv(f"{path}data{year}.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    # Set 'dailyDate' as the index
    data.set_index('Date', inplace=True)
    # Adding new columns for analysis
    data['Open-Close (%)'] = ((data['Open'] - data['Close']) / data['Close']) * 100  # Convert to percentage
    data['High-Low (%)'] = ((data['High'] - data['Low']) / data['Close']) * 100  # Convert to percentage
    return data

st.title("Data Analysis of Financial Contracts")

# User selects the year
selected_year = st.selectbox("Select a year", [1990, 2001, 2007, 2018])
df = load_data(selected_year)

# Display constant info
contract_name = df['ContractName'].iloc[0]
time_zone = df['TimeZone'].iloc[0]
st.write(f"Contract Name: {contract_name}, Time Zone: {time_zone}")

# High-Low Graph in Percentage
st.subheader("High-Low Difference Over Time (Percentage)")
fig_high_low = go.Figure(data=[go.Scatter(x=df.index, y=df['High-Low (%)'], mode='lines')])
fig_high_low.update_layout(title='High-Low Difference Through Time (Percentage)', xaxis_title='Date', yaxis_title='High-Low Difference (%)')
st.plotly_chart(fig_high_low)

# OHLC Chart
"""st.subheader("OHLC Chart")
fig_ohlc = go.Figure(data=[go.Ohlc(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
fig_ohlc.update_layout(title='OHLC Data', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig_ohlc)"""

nbtrade = df.groupby("dailyDate")['NbTrade'].sum()
# Number of Trades Graph
st.subheader(f"Number of Daily Trades Over Time : {selected_year}")
fig_nb_trade = go.Figure(data=[go.Scatter(x=nbtrade.index, y=nbtrade, mode='lines')])
fig_nb_trade.update_layout(title='Number of Trades Over Time', xaxis_title='Date', yaxis_title='Number of Trades')
st.plotly_chart(fig_nb_trade)
# Columns to analyze
columns_to_analyze = ['Open', 'Close', 'High', 'Low', 'LastTradedPrice', 
                      'LagSameContractLastTradedPrice', 'Volume', 'NbTrade', 'LogReturn',
                      'Open-Close (%)', 'High-Low (%)']

# Show statistical metrics
stats_data = {}
for col in columns_to_analyze:
    stats_data[col] = df[col].describe()

# Create a big table for all the stats
stats_df = pd.DataFrame(stats_data)
st.subheader(f"Descriptive Statistics {selected_year} - Period : Minute")
st.write(stats_df.transpose())

# Visualizations for specific columns
columns_for_distribution = ['NbTrade', 'LogReturn', 'Open-Close (%)', 'High-Low (%)']
for col in columns_for_distribution:
    st.subheader(f"Analysis of {col}")
    fig = px.histogram(df, x=col, title=f"Distribution of {col}")
    st.plotly_chart(fig)

# Creating the Data Table
start_date = df['dailyDate'].iloc[0]
end_date = df['dailyDate'].iloc[-1]
na_dates = df[df.isna().any(axis=1)]['dailyDate'].unique()

st.subheader(f"Summary Table : {selected_year}")
summary_table = pd.DataFrame({
    "Start Date": [start_date],
    "End Date": [end_date],
    "Dates with NaN": [na_dates]
})
st.write(summary_table)