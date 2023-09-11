import pandas as pd
import streamlit as st
import plotly.express as px
from numerize.numerize import numerize

st.set_page_config(page_title = 'Facebook Ad Campaign Dashboard', layout="wide", initial_sidebar_state="collapsed")


#Setting up cache to up app run faster by keeping data in cache
@st.cache 
def get_data():
  FBcampaign_df = pd.read_csv('FacebookCampaignData.csv')
  FBcampaign_df['date'] = pd.to_datetime(FBcampaign_df['date'])
  return FBcampaign_df

FB_df = get_data()

header_left,header_mid,header_right = st.columns([1,2,1], gap = 'large')

with header_mid:
  st.title('Facebook Campaign Dashboard')

#Sidebar will act as filters for data
with st.sidebar:
  Campaign_filter = st.multiselect(label = 'Select The Campaign',
                                   options = FB_df['campaign'].unique(),
                                   default = FB_df['campaign'].unique())
  
  Age_filter = st.multiselect(label = 'Select Age Group',
                                   options = FB_df['age'].unique(),
                                   default = FB_df['age'].unique())

  Gender_filter = st.multiselect(label = 'Select Gender Group',
                                   options = FB_df['gender'].unique(),
                                   default = FB_df['gender'].unique())


