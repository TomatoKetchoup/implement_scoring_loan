
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import os

df = pd.read_csv('C:/Users/td/implement_scoring_loan/api/df_api.csv', nrows= 10)

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

if os.environ.get('IS_HEROKU', '') != '':
    # Vous êtes en production sur Heroku, utilisez la variable d'environnement pour définir le chemin d'accès à votre fichier CSV
    path = ('https://apiscoringloan-tomatoketchoup.herokuapp.com')
else:
    # Vous êtes en train de travailler localement, utilisez le chemin de fichier local
    path = 'http://127.0.0.1:8000/'



if st.sidebar.button('👉🏽 GoGoGo'):
    id_client = int(id_client)
    inputs = {"customer": id_client}
    index_client = str(df[df['SK_ID_CURR'] == id_client].index[0])
    ## Requests
    financial = requests.post(url= (path+'financial'), json = inputs)
    financial = financial.json()

    m1, m2,m3= st.columns((1, 1,1,))
    m1.metric(label=' Customer Income', value='{:,.0f} $'.format(financial['income'][index_client]))
    m2.metric(label='Customer Credit', value='{:,.0f} $'.format(financial['credit'][index_client]))
    m3.metric(label='Customer Annuity', value='{:,.0f} $'.format(financial['annuity'][index_client]))
    # Define the gauge chart
    g1, g2, g3 = st.columns((1, 1, 1))

    # Afficher l'histogramme pour AMT_INCOME_TOTAL
    fig_income, ax = plt.subplots()
    ax.hist(df['AMT_INCOME_TOTAL'], bins=10)
    ax.set_xlabel('INCOME')
    g1.pyplot(fig_income)

    # Afficher l'histogramme pour AMT_CREDIT
    fig_credit, ax = plt.subplots()
    ax.hist(df['AMT_CREDIT'], bins=10)
    ax.set_xlabel('CREDIT')
    g2.pyplot(fig_credit)

    # Afficher l'histogramme pour AMT_ANNUITY
    fig_annuity, ax = plt.subplots()
    ax.hist(df['AMT_ANNUITY'], bins=10)
    ax.set_xlabel('ANNUNITY')
    g3.pyplot(fig_annuity)

    ## Request local feature importance
    # response = requests.post(url=('http://127.0.0.1:8000/local_importance'), json=inputs)
    # result = response.json()
    # feature_names = result['features']
    # importances = result['importances']
    # df_features_importance = pd.DataFrame(list(zip(feature_names, importances)),
    #                                       columns=['Features', 'Importance'])
    # df_features_importance = df_features_importance.sort_values(by=['Importance'],
    #                                                             ascending=True)
    #
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.barh(range(len(df_features_importance)),
    #         df_features_importance['Importance'],
    #         align='center')
    # ax.set_yticks(range(len(df_features_importance)))
    # ax.set_yticklabels(df_features_importance['Features'])
    # ax.set_ylabel('Feature')
    # ax.set_xlabel('Importance')
    # ax.set_title('Feature Importances')
    #
    # # Afficher le plot bar dans Streamlit
    # st.pyplot(fig)
    # result_proba = result['probabilities']
    # fig = go.Figure(go.Indicator(
    #     mode="gauge+number",
    #     value=result_proba[0],
    #     domain={'x': [0, 1], 'y': [0, 1]},
    #     title={'text': "Speed"}))
    # st.plotly_chart(fig)
    # result_proba = result['probabilities']
    # fig = go.Figure(go.Indicator(
    #     mode="gauge+number",
    #     value=result_proba[0],
    #     domain={'x': [0, 1], 'y': [0, 1]},
    #     title={'text': "Speed"}))
    # st.plotly_chart(fig)
