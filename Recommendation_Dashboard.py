import os
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler
# need to change the order 

def recommend_city():
    # basic intoduction setup

    # for future language processing
    st.sidebar.write('Personal Options')

    home_discribtion = st.sidebar.text_input('How would you discribe your new home', 'A small and cozy place')
    k = st.sidebar.slider('How my results would you like?', 1,10,5)
    population = st.sidebar.selectbox("Bussling City or Quite Town?", ['Bussling City', 'Quite Town'])
    diversity = st.sidebar.slider("How important is Diversity to your?",  0, 10, 5)
    
    st.sidebar.write('Work Options')

    commuting = st.sidebar.slider("How important is the communte time?", 0, 10, 5)

    WorkingStype = st.sidebar.selectbox("What is your working style",
        ["Private Work", "Public Work", "Self Employed", "Family Work"])

    Sector = st.sidebar.selectbox("What section do you want to work for?",
        ["Professional", "Sevice", "Office", "Construction", "Producation"])

    Submit = st.sidebar.button("Summit")

    if Submit:
        data = {'population':population, "diversity":diversity, "commuting":commuting, "WorkingStype":WorkingStype, "Sector":Sector}
        Cities = Recommendation_lister(data, k)
        for i,city in enumerate(Cities):
            st.write("{}) {}".format(i+1, city))



# @st.cache(suppress_st_warning=True)
def Recommendation_lister(data, k):
    final_df = pd.read_csv(FINAL_PATH)
    del final_df['Unnamed: 0']
    final_matrix = final_df[final_df.columns[final_df.columns != 'City']]
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(final_matrix)
    
    weights = np.array(data_2_weight(data))
    ranking_vector = np.dot(scaled_matrix, weights)
    ranking_vector = np.argsort(ranking_vector)
    city_index = list()
    city_list = list()
    for i in range(k):
        city_index.append(np.where(ranking_vector == i)[0][0])
    for i, index in enumerate(city_index):
        city_list.append(final_df['City'].iloc[index])
    return city_list

def data_2_weight(data):
    p = 5 if data['population'] == "Bussling City" else 2
    d = data['diversity']*5
    c = data['commuting']*-5

    Prf = 5 if data['Sector'] == "Professional" else 1
    Se = 5 if data['Sector'] == "Sevice" else 1
    Of = 5 if data['Sector'] == "Office" else 1
    Co = 5 if data['Sector'] == "Construction" else 1
    Pro = 5 if data['Sector'] == "Producation" else 1

    Pr_W = 5 if data['WorkingStype'] == "Private Work" else 1
    Pu_W = 5 if data['WorkingStype'] == "Public Work"else 1
    Se_E = 5 if data['WorkingStype'] == "Self Employed"else 1
    Fa_E = 5 if data['WorkingStype'] == "Family Work"else 1

    weights = [-2, d, 7, Prf, Se, Of, Co, Pro, 1, 1, 1, 1, 1, 1, c, Pr_W, Pu_W, Se_E, Fa_E, 1, 1, 1, p]
    return weights
    
LOCALPATH = os.getcwd()
DATAPATH = os.path.join(LOCALPATH,"data")
FILTERPATH = os.path.join(DATAPATH,"Filtered_data")
FINAL_PATH = os.path.join(FILTERPATH,"final_data.csv")