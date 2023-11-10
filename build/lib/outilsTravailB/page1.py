import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import functions as f  # Ensure this module contains the necessary functions
import os

chemin_relatif = "data2D/"
path = os.path.join(os.getcwd(), chemin_relatif)
# Setup Streamlit widgets to accept user input
st.title("Quadratic Variation and Closing Price Analysis")


# Load and clean data
@st.cache
def load_data():
    data_cleaned = {
        "data1990": pd.read_csv(f"{path}data1990.csv"),
        "data2001": pd.read_csv(f"{path}data2001.csv"),
        "data2007": pd.read_csv(f"{path}data2007.csv"),
        "data2018": pd.read_csv(f"{path}data2018.csv")
    }
    return data_cleaned

data_cleaned = load_data()

# User inputs for the year
year = st.selectbox("Select a year", (1990, 2001, 2007, 2018))

# User inputs for multiple k values and types
selected_k_values = st.multiselect("Select k values", range(1, 391), default=[1])
selected_types = st.multiselect("Select the types", ["Naive", "Mean"], default=["Mean"])

# Create subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.1,
                    subplot_titles=('Quadratic Variation Over Time', 'Closing Price'))

# Loop over selected k values and types for the first plot
for k in selected_k_values:
    for calc_type in selected_types:
        # Calculate the quadratic variation
        df = data_cleaned[f"data{year}"][["dailyDate", "LogReturn"]]
        res1 = f.createFramework(df, k, annualize=True, type = "vq")
        res2 = f.groupByDay(res1, calc_type)
        
        # Add a trace for each combination
        fig.add_trace(go.Scatter(
            x=res2.index,
            y=res2,
            mode='lines',
            name=f'k={k}, {calc_type}'
        ), row=1, col=1)

# Add closing price line plot for the selected year
candle_df = data_cleaned[f"data{year}"]
fig.add_trace(go.Scatter(
    x=candle_df['dailyDate'],
    y=candle_df['Close'],
    mode='lines',
    name='Closing Price'
), row=2, col=1)

# Update layout with titles and legend
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Quadratic Variation (Volatility)",
    legend_title="Legend",
    height=800  # You might need to adjust the height to fit both plots
)

# Update xaxis properties
fig.update_xaxes(title_text="Date", row=2, col=1)

# Update yaxis properties for closing price
fig.update_yaxes(title_text="Price", row=2, col=1)

# Plot the data
st.plotly_chart(fig)