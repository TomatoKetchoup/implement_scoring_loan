import streamlit as st
import json
import requests

st.title('Dashboard')

# Taking id client input
id_client = st.text_input('Customer id')
id_client = int(id_client)
inputs={"customer":id_client}

if st.button('GoGoGo'):
    res = requests.post(url= ('http://127.0.0.1:8000/gender'), data = json.dumps(inputs))
    st.write(f"Customer gender = {res}")