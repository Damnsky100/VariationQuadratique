import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import functions as f  # Ensure this module contains the necessary functions
import os
# Setup Streamlit widgets to accept user input
st.title("3D Quadratic Variation Analysis")


# Set your path
dir_path = os.path.dirname(os.path.realpath(__file__))
chemin_relatif = "data3D/"
path = os.path.join(dir_path, chemin_relatif)


# Load and clean data
@st.cache
def load_data():
    typeList = ["Naive", "Mean"]
    dateList = ["1990", "2001", "2007", "2018"]
    data_cleaned = {}
    for type in typeList:
        for date in dateList:
            # Create a unique key for each combination of type and date
            key = f"{type}_{date}"
            # Load the corresponding CSV file
            df = pd.read_csv(f"{path}{type}{date}.csv")
            
            # Check if "Unnamed: 0" is in the columns and convert it to datetime
            if "Unnamed: 0" in df.columns:
                df["Unnamed: 0"] = pd.to_datetime(df["Unnamed: 0"])
                df = df.set_index("Unnamed: 0")
            else:
                # If "Unnamed: 0" is not in columns, you may want to set the first column as index
                # and convert it to datetime if it contains date information
                df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
                df = df.set_index(df.columns[0])
            data_cleaned[key] = df
                
    return data_cleaned

data_cleaned = load_data()

# User inputs for the type and year
selected_type = st.selectbox("Select the type", ["Naive", "Mean"])
selected_year = st.selectbox("Select a year", ["1990", "2001", "2007", "2018"])

# Fetch the dataframe based on user selection
selected_df_key = f"{selected_type}_{selected_year}"
selected_df = data_cleaned[selected_df_key]

# Convert the date to a proper format if necessary
# Assuming the dataframe has a 'Date' column which needs to be converted to datetime
# selected_df['Date'] = pd.to_datetime(selected_df['Date'])

# Create meshgrid for 3D surface plot
x, y = np.meshgrid(selected_df.columns, selected_df.index)
z = selected_df.to_numpy()

# Create the 3D surface plot
fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

# Update the layout of the figure
fig.update_layout(
    title=f"{selected_type} Quadratic Variation - {selected_year}",
    scene=dict(
        xaxis_title="n pas par jours",
        yaxis_title="Date",
        zaxis_title="Quadratic Variation"
    ),
    autosize=False,
    width=800,
    height=800,
    margin=dict(l=65, r=50, b=65, t=90)
)

# Display the figure in Streamlit
st.plotly_chart(fig)
