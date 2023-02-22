import streamlit as st
import json
import requests

st.title('🔮Dashboard 🔮')

# Taking id client input
id_client = st.text_input('Customer id')

if st.button('GoGoGo'):
    m1, m2, m3, m4 = st.columns((1, 1, 1, 1))
    id_client = int(id_client)
    inputs = {"customer": id_client}
    res = requests.post(url= ('http://127.0.0.1:8000/gender'), json = inputs)
    gender_value = res.json()
    st.write(f"Customer gender = {gender_value}")
    ## Request for financial information
    financial = requests.post(url= ('http://127.0.0.1:8000/financial'), json = inputs)
    financial = financial.json()
    m1.write('')
    m2.metric(label='Customer Income', value='{:,.0f} $'.format(financial['income']['0']))
    m3.metric(label='Customer Credit', value='{:,.0f} $'.format(financial['credit']['0']))
    m4.metric(label='Customer Annuity', value='{:,.0f} $'.format(financial['annuity']['0']))
