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

#KPIs- Connecting columns to our filters
FB_df1 = FB_df.query('campaign == @Campaign_filter & age == @Age_filter & gender == @Gender_filter')

#Metrics: Sum of Impressions, total clicks, total money spent of campaign, total number of conversions, total number of APPROVED conversions
total_impressions = float(FB_df1['Impressions'].sum())
total_clicks = float(FB_df1['Clicks'].sum())
total_spent = float(FB_df1['Spent'].sum())
total_conversions = float(FB_df1['Total_Conversions'].sum())
total_Approved_Conversions = float(FB_df1['Approved_Conversions'].sum())

#Columns for the 5 metrics
total1,total2,total3,total4,total5, = st.columns(5,gap ='large')

with total1:
  st.header("Total Impressions :eyes:")
  st.metric(label = 'Total Impressions :eyes:', value = numerize(total_impressions))

with total2:
  st.metric(label = 'Total Clicks :eyes:', value = numerize(total_clicks)) 

with total3:
  st.metric(label = 'Total Spend :eyes:', value = numerize(total_spent))

with total4:
  st.metric(label = 'Total Conversions :eyes:', value = numerize(total_conversions))

with total5:
  st.metric(label = 'Approved Conversions :eyes:', value = numerize(total_Approved_Conversions))
