import os
import pandas as pd
import numpy as np
import streamlit as st


def run_the_app():
    # basic intoduction setup
    City_Name = st.text_input('City Name', 'Houston')
    st.write('The city of your dream is', City_Name)
    Graphic_Genration(City_Name)

def Graphic_Generation(City_name):
