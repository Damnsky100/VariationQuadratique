import streamlit as st
import os
# Use Streamlit's command line option to run the multipage app
# streamlit run app.py
# app.py
def main():
    print("App is running")


# Define the pages
pages = {
    "Quadratic Variation Analysis": "page1",
    "3D Analysis": "page2",
    "Quadratic Variation - Decomposition" : "page3",
    "Data Analysis" : "page4"
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))



# Load the selected page
page = pages[selection]
with open(page + ".py") as f:
    code = compile(f.read(), page + ".py", 'exec')
    exec(code, {'__name__':'__main__'})
    
# streamlit run "/Users/sebastiencaron/Desktop/TravailB-VariationQuadratique/app.py"
