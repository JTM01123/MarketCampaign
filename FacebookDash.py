import pandas as pd
import streamlit as st
import plotly.express as px
from numerize.numerize import numerize

st.set_page_config(page_title = 'Facebook Ad Campaign Dashboard', layout="wide", initial_sidebar_state="collapsed")

@st.cache
def get_data():
  
