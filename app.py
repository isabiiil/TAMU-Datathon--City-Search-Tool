import os
import pandas as pd
import numpy as np
import streamlit as st
from Searching_Dashboard import search_city
from Recommendation_Dashboard import recommend_city

def main():
    st.title("The city of your Dreams")
    aboutus_text = st.markdown("")  
    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("El Dorado")
    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["City Recomendation", "City Search", "About Us"])

    if app_mode == "City Recomendation":
        aboutus_text.empty()
        recommend_city()
    elif app_mode == "City Search":
        aboutus_text.empty()
        search_city()
        # st.code(get_file_content_as_string("app.py"))
    elif app_mode == "About Us":
        aboutus_text = st.markdown(local_get_file_content_as_string(ABOUTUSPATH), unsafe_allow_html=True) 
        st.sidebar.success('Try other pages for finding your new home')    
    # Add a selectbox to the sidebar:

def local_get_file_content_as_string(path):
    file_path = os.path.join(LOCALPATH,path)
    return open(file_path, 'r').read()

LOCALPATH = os.getcwd()
ABOUTUSPATH = "About_Us.md"

if __name__ == "__main__":
    main()    