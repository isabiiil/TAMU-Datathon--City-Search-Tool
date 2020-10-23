import os
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt 
import scipy.stats as stats

def search_city():
    # basic intoduction setup
    City_and_State = st.text_input('City Name', 'Houston, TX')
    City_name, State_name = City_State_processor(City_and_State)
    ser_df = pd.read_csv(SEARCH_PATH, index_col ='index')
    index = City_State_index_finder(City_name,State_name,ser_df)
    if index != None:
        st.write('The city of your dream is', City_name)
        Graphic_Generation(ser_df,index)
    else:
        st.write('{}, {} is a invalid input or it does not exist, Please make sure that City and State are both added like "Houston, Tx". The City Spacing and spelling are correct.'.format(City_name, State_name))
    
def City_State_processor(City_and_State):
    input_val = City_and_State.split(', ')
    if (len(input_val) != 2):
        City, State = 'Houston', 'TX'
    else:
        City = input_val[0]
        City = City.lower().capitalize()
        State = input_val[1].upper()[0:2]
    return City, State

def City_State_index_finder(City_name, State_name, ser_df):
    # Checking the Search
    index = list(np.sum(ser_df[['City', 'State']].values == [City_name,State_name],axis=1)//2 == 1)
    if sum(index) == 0:
        index=None 
    return index

def Graphic_Generation(ser_df,index):
    #City Data Extraction
    values = City_Data_Grabber(ser_df,index)
    st.write("There are approximatly {} people living in {}. The yougest person the is {} years old and the olders person is {} years old.".format(
        values['pop'][0], values['City'],values['pop'][1],values['pop'][2]))
    Graphic_maker(values)


def City_Data_Grabber(ser_df,index):
    ser_data = ser_df[index]
    City = ser_data['City'].iloc[0]
    State = ser_data['State'].iloc[0]
    inc_data = ser_data[['Mean','Median','Stdev']]
    emp_data = ser_data[['Employed','Unemployment']]
    pov_data = ser_data[['Poverty','ChildPoverty']]
    div_data = ser_data[['Hispanic','White','Black','Native','Asian','Pacific']]
    ind_data = ser_data[['Professional','Service','Office','Construction','Production']]
    tra_data = ser_data[['Drive','Carpool','Transit','Walk','OtherTransp','WorkAtHome']]
    emp_r_data = ser_data[['PrivateWork','PublicWork','SelfEmployed','FamilyWork']]
    pop_data = ser_data[['population','minimum_age_x','minimum_age_y']].values[0]

    values = {'City':City,'State':State,'inc':inc_data,'emp':emp_data,'pov':pov_data, 'div':div_data, 'ind':ind_data,'tra':tra_data,
    'emp_r':emp_r_data,'pop':pop_data}
    
    return values

def Graphic_maker(values):
        LineBreak()
        plt.style.use("seaborn-deep")

        x = Histgram_data_maker(values['inc'].values[0][0], values['inc'].values[0][2])
        median = values['inc'].values[0][1]

        fig = sns.displot(data=x,kde=True)
        plt.axvline(median,color='b', linestyle='--')
        plt.xlabel('Income')
        plt.ylabel('Count')
        plt.title('Income Distribution of the City')
        st.pyplot(fig)

        LineBreak()
        fig2, ax2 = plt.subplots()
        ax2 = plt.bar(values['tra'].columns[0:6], values['tra'].values[0][0:6])
        plt.ylabel("Percentage")
        fig2.suptitle("Transportation Modes")
        st.pyplot(fig2)

        LineBreak()
        fig3, ax3 = plt.subplots()
        ax3 = plt.bar(values['ind'].columns[1:], values['ind'].values[0][1:])
        plt.ylabel("Percentage")
        fig3.suptitle("Job Sector")
        st.pyplot(fig3)

        LineBreak()
        fig4, axs = plt.subplots(2,2)        
        axs[0,0].pie(values['div'].values[0][:], labels= values['div'].columns[:])
        axs[0,0].set_title("Ethinic Makeup")
        axs[0,1].pie(values['emp_r'].values[0][:], labels= values['emp_r'].columns[:])       
        axs[0,1].set_title("Economic Makeup")
        axs[1,0].pie(values['emp'].values[0][:], labels= values['emp'].columns[:])
        axs[1,0].set_title("Employment Makeup")
        axs[1,1].pie(values['pov'].values[0][:], labels= values['pov'].columns[:])
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
DATAPATH = os.path.join(LOCALPATH,"City_Search_Data")
SEARCH_PATH = os.path.join(DATAPATH, "Total_Search_df.csv")