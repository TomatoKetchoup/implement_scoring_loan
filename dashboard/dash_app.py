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
import json
import streamlit as st




# df = pd.read_csv('C:/Users/td/implement_scoring_loan/notebook/data.csv', nrows=10)

st.title('🔮Dashboard 🔮')
# Taking id client input
id_client = st.text_input('Customer id')


if st.button('👉🏽 GoGoGo'):
    id_client = int(id_client)
    inputs = {"customer": id_client}
    response = requests.post(url=('http://127.0.0.1:8000/local_importance'), json=inputs)
    result = response.json()["result"]
    st.components.v1.html(result, width=1000, height=800, scrolling=True)