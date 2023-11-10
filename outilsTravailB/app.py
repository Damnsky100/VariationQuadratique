import streamlit as st
import os
# Use Streamlit's command line option to run the multipage app
# streamlit run app.py
# app.py

# Define the pages
dir_path = os.path.dirname(os.path.realpath(__file__))

pages = {
    "Quadratic Variation Analysis": os.path.join(dir_path, "page1.py"),
    "3D Analysis": os.path.join(dir_path, "page2.py"),
    "Quadratic Variation - Decomposition" : os.path.join(dir_path, "page3.py"),
    "Data Analysis" : os.path.join(dir_path, "page4.py")
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))



# Load the selected page
page_path = pages[selection]
with open(page_path) as f:
    code = compile(f.read(), os.path.basename(page_path), 'exec')
    exec(code, {'__name__': '__main__'})
    
# streamlit run "/Users/sebastiencaron/Desktop/TravailB-VariationQuadratique/app.py"
