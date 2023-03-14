import streamlit as st
import json
import requests
import lime
import tempfile
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import pickle
import pandas as pd
import streamlit.components.v1 as components
import html
import pydeck as pdk
import json
import streamlit as st
from pydantic import BaseModel
import plotly.graph_objs as go

df = pd.read_csv('C:/Users/td/implement_scoring_loan/notebook/data.csv', nrows= 10)

st.title('🔮Dashboard 🔮')
# Taking id client input
options = np.unique(df['SK_ID_CURR'])
id_client = st.sidebar.selectbox('Customer id', options)
st.sidebar.write('Gender')
if df[df['SK_ID_CURR']== id_client]['CODE_GENDER'].any() == 0:
    st.sidebar.markdown('<img src="https://img.icons8.com/color/48/null/checked-user-male.png"/>',
                        unsafe_allow_html=True)
else :
    st.sidebar.markdown('<img src="https://img.icons8.com/color/48/null/checked-user-female.png"/>',unsafe_allow_html=True)



if st.sidebar.button('👉🏽 GoGoGo'):
    id_client = int(id_client)
    inputs = {"customer": id_client}
    index_client = str(df[df['SK_ID_CURR'] == id_client].index[0])
    ## Request for financial information
    financial = requests.post(url= ('http://127.0.0.1:8000/financial'), json = inputs)
    financial = financial.json()

    m1, m2,m3= st.columns((1, 1,1,))
    m1.metric(label=' Customer Income', value='{:,.0f} $'.format(financial['income'][index_client]))
    m2.metric(label='Customer Credit', value='{:,.0f} $'.format(financial['credit'][index_client]))
    m3.metric(label='Customer Annuity', value='{:,.0f} $'.format(financial['annuity'][index_client]))
    # Define the gauge chart
    g1, g2, g3 = st.columns((1, 1, 1))

    fig_income, ax = plt.subplots()
    ax.boxplot(df['AMT_INCOME_TOTAL'])
    ax.set_xticklabels(['INCOME'])
    g1.pyplot(fig_income)

    fig_credit, ax = plt.subplots()
    ax.boxplot(df['AMT_CREDIT'])
    ax.set_xticklabels(['CREDIT'])
    g2.pyplot(fig_credit)

    fig_annuity, ax = plt.subplots()
    ax.boxplot(df['AMT_ANNUITY'])
    ax.set_xticklabels(['ANNUNITY'])
    g3.pyplot(fig_annuity)

    ## Request local feature importance
    response = requests.post(url=('http://127.0.0.1:8000/local_importance'), json=inputs)
    result = response.json()["result"]['html_explanation']
    result_proba = response.json()['result']['probabilities'][0]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result_proba,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Speed"}))
    st.plotly_chart(fig)
    st.components.v1.html(result, width=1000, height=800, scrolling=True)