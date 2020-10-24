import os
import pandas as pd
import numpy as np
import streamlit as st
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
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
    tran_mode = st.sidebar.selectbox("What is your mode of Transportation",
        ['Drive','Carpool','Transit','Walk','OtherTransp', 'WorkAtHome'])
    WorkingStype = st.sidebar.selectbox("What is your working style",
        ["Private Work", "Public Work", "Self Employed", "Family Work"])

    Sector = st.sidebar.selectbox("What section do you want to work for?",
        ["Professional", "Sevice", "Office", "Construction", "Producation"])

    Submit = st.sidebar.button("Summit")

    if Submit:
        data = {'population':population, "diversity":diversity, "commuting":commuting, 
            "WorkingStype":WorkingStype, "Sector":Sector, "Tran_mode":tran_mode}
        Cities, States = Recommendation_lister(data, k)
        for i,city in enumerate(Cities):
            st.write("{}) {}, {}".format(i+1, city, States[i]))
        map_drawer(Cities,States)


def City_to_Number(Cities, States):
    Cities_States = list()
    for i, City in enumerate(Cities):
        Cities_States.append(City+' '+States[i])
    geolocator = Nominatim(user_agent='myapplication')
    Longitude, Latitude = list(), list()
    for i, City_State in enumerate(Cities_States):
        location = geolocator.geocode(City_State)
        if location != None:
            Longitude.append(location.longitude)
            Latitude.append(location.latitude)
    return Longitude,Latitude

def map_drawer(Cities,States):
    longi,lat = City_to_Number(Cities,States)
    fig, ax = plt.subplots()
    for i, logs in enumerate(longi):
        if -65 < logs or -125 > logs:
            longi.remove(logs)
            lat.remove(lat[i])
    for i, la in enumerate(lat):
        if 50 < la or 25 > la:
            longi.remove(longi[i])
            lat.remove(la)
    # BBox = [-175,-55,15,65]
    BBox = [-125,-65,25,50]
    us_m = plt.imread(MAPPATH)
    ax.scatter(longi,lat, zorder=1, alpha=1, c='r', s=20)
    # ax.set_xlim(BBox[0],BBox[1])
    # ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(us_m, zorder=0, aspect='auto', extent = BBox)
    st.pyplot(fig)
    
    

# @st.cache(suppress_st_warning=True)
def Recommendation_lister(data, k):
    rec_df = pd.read_csv(RECOMMENPATH)
    City_State_df = rec_df[['City','State']]
    Number_df = rec_df.drop(['City', 'State'], axis = 1)
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(Number_df)
    weights = np.array(data_2_weight(data))
    ranking_vector = np.dot(scaled_matrix, weights)
    ranking_vector = np.argsort(ranking_vector)
    city_index = list()
    city_list = list()
    state_list = list()
    for i in range(k):
        city_index.append(np.where(ranking_vector == i)[0][0])
    for i, index in enumerate(city_index):
        city_list.append(City_State_df['City'].iloc[index])
        state_list.append(City_State_df['State'].iloc[index])
    return city_list, state_list

def data_2_weight(data):
    Po = 10 if data['population'] == "Bussling City" else -5 
    En = 5 if data['population'] == "Bussling City" else 2
    Pv = 1
    Dv = data['diversity']*5
    Em = 10
    c = data['commuting']*-5

    Dr = 5 if data['Tran_mode'] == 'Drive' else 1
    Cr = 5 if data['Tran_mode'] == 'Carpool' else 1
    Tr = 5 if data['Tran_mode'] == 'Transit' else 1
    Wa = 5 if data['Tran_mode'] == 'Walk' else 1
    Ot = 5 if data['Tran_mode'] == 'OtherTransp' else 1
    Wh = 5 if data['Tran_mode'] == 'WorkAtHome' else 1

    Prf = 5 if data['Sector'] == "Professional" else 1
    Se = 5 if data['Sector'] == "Sevice" else 1
    Of = 5 if data['Sector'] == "Office" else 1
    Co = 5 if data['Sector'] == "Construction" else 1
    Pro = 5 if data['Sector'] == "Producation" else 1

    Pr_W = 5 if data['WorkingStype'] == "Private Work" else 1
    Pu_W = 5 if data['WorkingStype'] == "Public Work"else 1
    Se_E = 5 if data['WorkingStype'] == "Self Employed"else 1
    Fa_E = 5 if data['WorkingStype'] == "Family Work"else 1

    weights = [Po, Pv ,Dv, Em, Prf, Se, Of, Co, Pro, Dr, Cr, 
    Tr, Wa, Ot, Wh, c, Pr_W, Pu_W, Se_E, Fa_E, En, En, En, En]
    return weights
    
LOCALPATH = os.getcwd()
MAPPATH = os.path.join(LOCALPATH,"map.png")
DATAPATH = os.path.join(LOCALPATH,"City_Search_Data")
POP_PATH = os.path.join(DATAPATH,"Population_df.csv")
DIV_PATH = os.path.join(DATAPATH,"Diversity_df.csv")
POV_PATH = os.path.join(DATAPATH,'Poverty_df.csv')
EMPLOYMENT_PATH = os.path.join(DATAPATH,'Employment_df.csv')
EMPLOYMENT_RATIO_PATH = os.path.join(DATAPATH,"Employment_ratio_df.csv")
INDUSTRY_PATH = os.path.join(DATAPATH,"Industry_df.csv")
TRANSPORT_PATH = os.path.join(DATAPATH,"Transportation_df.csv")
INCOME_PATH = os.path.join(DATAPATH,"Mean_Income_df.csv")
TOTAL_SEARCH_PATH = os.path.join(DATAPATH, "Total_Search_df.csv")
RECOMMENPATH = os.path.join(DATAPATH, "Recommendation_df.csv")