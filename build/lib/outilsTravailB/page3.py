import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import functions as f  # Ensure this module contains the necessary functions
import os
# Setup Streamlit widgets to accept user input
st.title("Quadratic Variation Decompositions")

# Set your path
dir_path = os.path.dirname(os.path.realpath(__file__))
chemin_relatif = "data2D/"
path = os.path.join(dir_path, chemin_relatif)


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

# User inputs for the year and k
year = st.selectbox("Select a year", (1990, 2001, 2007, 2018))
selected_k = st.selectbox("Select k value", range(1, 391))
selected_types = st.selectbox("Select the types", ["Naive", "Mean"])

# Checkbox for users to choose which components to display
show_vq = st.checkbox("Show Quadratic Variation", True)
show_iv = st.checkbox("Show Integrated Variance", True)
show_jump = st.checkbox("Show Jump Component", True)

df = data_cleaned[f"data{year}"][["dailyDate", "LogReturn"]]
df = df.fillna(0)

# Calculations
resvq = f.createFramework(df, selected_k, annualize=True, type="vq")
resiv = f.createFramework(df, selected_k, annualize=True, type="iv")

resvqF = f.groupByDay(resvq, selected_types)
resivF = f.groupByDay(resiv, selected_types)
resjumpF = np.maximum(0, resvqF - resivF)

# Plot
fig = make_subplots(specs=[[{"secondary_y": True}]])

if show_vq:
    fig.add_trace(go.Scatter(x=resvqF.index, y=resvqF, mode='lines', name='Quadratic Variation'))

if show_iv:
    fig.add_trace(go.Scatter(x=resivF.index, y=resivF, mode='lines', name='Integrated Variance'))

if show_jump:
    fig.add_trace(go.Scatter(x=resjumpF.index, y=resjumpF, mode='lines', name='Jump Component'))

# Update the layout of the figure
fig.update_layout(
    title='Quadratic Variation, Integrated Variance, and Jump Component Over Time',
    xaxis_title='Date',
    yaxis_title='Value',
    legend_title='Legend'
)

# Show the figure in a Streamlit app
st.plotly_chart(fig)
