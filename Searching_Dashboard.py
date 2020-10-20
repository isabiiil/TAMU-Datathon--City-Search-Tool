import os
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt 
import scipy.stats as stats



def search_city():
    # basic intoduction setup
    City_Name = st.text_input('City Name', 'Houston')
    st.write('The city of your dream is', City_Name)
    Graphic_Generation(City_Name)

def Graphic_Generation(City_name):
    
    # reading the files
    pop_df = pd.read_csv(POP_PATH)
    pov_df = pd.read_csv(POV_PATH)
    div_df = pd.read_csv(DIV_PATH)
    inc_df = pd.read_csv(INCOME_PATH)
    ind_df = pd.read_csv(INDUSTRY_PATH)
    tra_df = pd.read_csv(TRANSPORT_PATH)
    emp_df = pd.read_csv(EMPLOYMENT_PATH)
    emp_r_df = pd.read_csv(EMPLOYMENT_RATIO_PATH)

    new_df = div_df.merge(pop_df, on='City', how="inner")
    Cities_List = list(new_df['City'].values)
    if City_name not in Cities_List:
        City_name='Houston'
    else:
        #City Data Extraction
        inc_data = inc_df[inc_df['City'] == City_name]
        emp_data = emp_df[emp_df['City'] == City_name]
        pov_data = pov_df[pov_df['City'] == City_name]
        div_data = div_df[div_df['City'] == City_name]
        ind_data = ind_df[ind_df['City'] == City_name]
        tra_data = tra_df[tra_df['City'] == City_name]
        emp_r_data = emp_r_df[emp_r_df['City'] == City_name]
        pop_data = (pop_df[pop_df['City'] == City_name]).values[0]
        
        st.write("There are approximatly {} people living in {}. The yougest person the is {} years old and the olders person is {} years old.".format(pop_data[1], pop_data[0],pop_data[2],pop_data[3]))
        
        LineBreak()
        plt.style.use("seaborn-deep")
        x = Histgram_data_maker(inc_data.values[0][1], inc_data.values[0][2])
        median = inc_data.values[0][3]

        fig = sns.displot(data=x,kde=True)
        plt.axvline(median,color='b', linestyle='--')
        plt.xlabel('Income')
        plt.ylabel('Count')
        plt.title('Income Distribution of the City')
        st.pyplot(fig)

        LineBreak()
        fig2, ax2 = plt.subplots()
        ax2 = plt.bar(tra_data.columns[1:7], tra_data.values[0][1:7])
        plt.ylabel("Percentage")
        fig2.suptitle("Transportation Modes")
        st.pyplot(fig2)

        LineBreak()
        fig3, ax3 = plt.subplots()
        ax3 = plt.bar(ind_data.columns[1:], ind_data.values[0][1:])
        plt.ylabel("Percentage")
        fig3.suptitle("Job Sector")
        st.pyplot(fig3)

        LineBreak()
        fig4, axs = plt.subplots(2,2)        
        axs[0,0].pie(div_data.values[0][1:5], labels= div_data.columns[1:5])
        axs[0,0].set_title("Ethinic Makeup")
        axs[0,1].pie(emp_r_data.values[0][1:5], labels= emp_r_data.columns[1:5])       
        axs[0,1].set_title("Economic Makeup")
        axs[1,0].pie(emp_data.values[0][1:], labels= emp_data.columns[1:])
        axs[1,0].set_title("Employment Makeup")
        axs[1,1].pie(pov_data.values[0][1:], labels= pov_data.columns[1:])
        axs[1,1].set_title("Poverty Makeup")
        st.pyplot(fig4)


def LineBreak():
    st.markdown("---", unsafe_allow_html=True)


def Histgram_data_maker(mu,sigma):
    a, b = 0, 2000000
    dist = stats.truncnorm((a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)
    values = dist.rvs(1000)
    return values
    
LOCALPATH = os.getcwd()
DATAPATH = os.path.join(LOCALPATH,"data")
FILTERPATH = os.path.join(DATAPATH,"Filtered_data")
POP_PATH = os.path.join(FILTERPATH,"City_based_population.csv")
DIV_PATH = os.path.join(FILTERPATH,"Diversity_df.csv")
POV_PATH = os.path.join(FILTERPATH,'Poverty_df.csv')
EMPLOYMENT_PATH = os.path.join(FILTERPATH,'Employment_df.csv')
EMPLOYMENT_RATIO_PATH = os.path.join(FILTERPATH,"Employment_ratio_df.csv")
INDUSTRY_PATH = os.path.join(FILTERPATH,"Industry_df.csv")
TRANSPORT_PATH = os.path.join(FILTERPATH,"Transportation_df.csv")
INCOME_PATH = os.path.join(FILTERPATH,"Income_clean.csv")