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
total_conversions= float(FB_df1['Total_Conversion'].sum()) 
total_approved_conversions = float(FB_df1['Approved_Conversion'].sum())

#Columns for the 5 metrics
total1,total2,total3,total4,total5, = st.columns(5,gap ='large')

with total1:
  st.metric(label = 'Total Impressions :eyes:', value = numerize(total_impressions))

with total2:
  st.metric(label = 'Total Clicks :three_button_mouse:', value = numerize(total_clicks)) 

with total3:
  st.metric(label = 'Total Spend :moneybag:', value = numerize(total_spent))

with total4:
  st.metric(label = 'Total Conversions :shopping_trolley:', value = numerize(total_conversions))

with total5:
  st.metric(label = 'Approved Conversions :ballot_box_with_check:', value = numerize(total_approved_conversions))

Q1,Q2 = st.columns(2)

with Q1:
    FB_df2 = FB_df1.groupby( by = ['campaign']).sum()[['Impressions', 'Clicks']].rest_index()
    FB_df2['CTR'] = round(FB_df2['Clicks']/FB_df2['Impressions'] *100, 3)
    fig_CTR_by_campaign = px.bar(FB_df2,
                            x='campaign',
                            y='CTR',
                            title='<b>Click Through Rate</b>')
    fig_CTR_by_campaign.update_layout(title = {'x' : 0.5},
                                    plot_bgcolor = "rgba(0,0,0,0)",
                                    xaxis =(dict(showgrid = False)),
                                    yaxis =(dict(showgrid = False)))
    st.plotly_chart(fig_CTR_by_campaign,use_container_width=True)
  
with Q2:
    fig_impressions_per_day = px.line(FB_df1,x='date',
                                    y=['Impressions'],
                                    color='campaign',
                                    title='<b>Daily Impressions By Campaign</b>')
    fig_impressions_per_day.update_xaxes(rangeslider_visible=True)
    fig_impressions_per_day.update_layout(xaxis_range=['2021-01-01','2021-01-31'],
                                        showlegend = False,
                                        title = {'x' : 0.5},
                                         plot_bgcolor = "rgba(0,0,0,0)",
                                        xaxis =(dict(showgrid = False)),
                                        yaxis =(dict(showgrid = False)),)
    st.plotly_chart(fig_impressions_per_day,use_container_width=True)

