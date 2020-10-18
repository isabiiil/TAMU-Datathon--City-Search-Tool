import os
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt 


def search_city():
    # basic intoduction setup
    City_Name = st.text_input('City Name', 'Houston')
    st.write('The city of your dream is', City_Name)
    Graphic_Generation(City_Name)

def Graphic_Generation(City_name):
    # reading the files
    pop_df = pd.read_csv(POP_PATH)
    div_df = pd.read_csv(DIV_PATH)
    emp_r_df = pd.read_csv(EMPLOYMENT_RATIO_PATH)
    ind_df = pd.read_csv(INDUSTRY_PATH)
    tra_df = pd.read_csv(TRANSPORT_PATH)
    in_df = pd.read_csv(INCOME_PATH)

    new_df = div_df.merge(pop_df, on='City', how="inner")
    Cities_List = list(new_df['City'].values)
    if City_name not in Cities_List:
        City_name='Houston'
    else:
        pop_data = (pop_df[pop_df['City'] == City_name]).values[0]
        st.write("There are approximatly {} people living in {}. The yougest person the is {} years old and the olders person is {} years old.".format(pop_data[0], pop_data[1],pop_data[2],pop_data[3]))
        
        div_data = div_df[div_df['City'] == City_name]
        emp_r_data = emp_r_df[emp_r_df['City'] == City_name]
        ind_df_data = ind_df[ind_df['City'] == City_name]
        tra_df_data = tra_df[tra_df['City'] == City_name]
        inc_df_data = in_df[in_df['City'] == City_name]
        plt.style.use("seaborn-deep")
        x = Histgram_data_maker(inc_df_data.values[0][1], inc_df_data.values[0][2])
        fig1, ax = plt.subplots()
        ax = sns.distplot(x)
        # fig1.xlabel('"House Hold Income"')
        ax.set_title("Income Distribution of the city")
        st.pyplot(fig1)

        fig2, axs = plt.subplots(2,2)        
        axs[0,0].pie(div_data.values[0][1:5], labels= div_data.columns[1:5])
        axs[0,0].set_title("Ethinic Makeup")
        axs[1,0].pie(emp_r_data.values[0][1:5], labels= emp_r_data.columns[1:5])       
        axs[1,0].set_title("Economic Makeup")
        axs[0,1].pie(ind_df_data.values[0][1:6], labels= ind_df_data.columns[1:6])
        axs[0,1].set_title("Work Style Makeup")
        axs[1,1].pie(tra_df_data.values[0][1:7], labels= tra_df_data.columns[1:7])
        axs[1,1].set_title("Transportation Makeup")
        fig2.suptitle("Visualization the make up of the City")
        st.pyplot(fig2)


def Histgram_data_maker(mean,std):
    np.random.seed(0)
    dataset = std* np.random.randn(200) + mean
    return dataset
    
LOCALPATH = os.getcwd()
DATAPATH = os.path.join(LOCALPATH,"data")
FILTERPATH = os.path.join(DATAPATH,"Filtered_data")
POP_PATH = os.path.join(FILTERPATH,"City_based_population.csv")
DIV_PATH = os.path.join(FILTERPATH,"Diversity_df.csv")
EMPLOYMENT_RATIO_PATH = os.path.join(FILTERPATH,"Employment_ratio_df.csv")
INDUSTRY_PATH = os.path.join(FILTERPATH,"Industry_df.csv")
TRANSPORT_PATH = os.path.join(FILTERPATH,"Transportation_df.csv")
INCOME_PATH = os.path.join(FILTERPATH,"Income_clean.csv")