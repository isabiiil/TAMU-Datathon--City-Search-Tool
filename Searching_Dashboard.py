import streamlit as st
from 
import pandas as pd
import numpy as np

def main():

    st.title("The city of your Dreams")
    # Add a selectbox to the sidebar:
    aboutus_text = st.markdown(get_file_content_as_string("About_Us.md"))



    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["About Us", "City Search", "City Recomendation"])
    if app_mode == "About Us":
        st.sidebar.success('To continue select "Run the app".')
    elif app_mode == "City Search":
        aboutus_text.empty()
        # st.code(get_file_content_as_string("app.py"))
        run_the_app()
    # elif app_mode == "Run the app":
    #     readme_text.empty()
    #     run_the_app()

def run_the_app():
    City_Name = st.text_input('City Name', 'Houston')
    st.write('The city of your dream is', City_Name)

def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/streamlit/demo-self-driving/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

if __name__ == "__main__":
    main()    