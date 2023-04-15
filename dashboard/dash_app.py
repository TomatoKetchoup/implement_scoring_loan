import os
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go
import requests
import streamlit as st
import pathlib
import numpy as np
# dash_dir = pathlib.Path(__file__).parent.resolve()
# print(dash_dir)
if 'DYNO' in os.environ:
    # Vous êtes en production sur Heroku, utilisez la variable d'environnement pour définir le chemin d'accès à votre fichier CSV
    path_request = 'https://apiscoringloan-tomatoketchoup.herokuapp.com/'
    path_df = 'https://raw.githubusercontent.com/TomatoKetchoup/implement_scoring_loan/main/dashboard/'

else:
# Vous êtes en train de travailler localement, utilisez le chemin de fichier local
    path_request = 'http://localhost:8000/'
    # path_df = dash_dir/'dashboard/'
    path_df = 'C:/Users/td/implement_scoring_loan/dashboard/'
# TODO CHANGE NUMBER OF ROWS
df = pd.read_csv(path_df+'data_test_dash.csv', nrows= 10)

st.image('logo_dash.ico')
# Taking id client input
options = np.unique(df['SK_ID_CURR'])
id_client = st.sidebar.selectbox('Customer id', options)


if st.sidebar.button('👉🏽 GoGoGo'):
    id_client = int(id_client)
    st.sidebar.write('Gender')
    if df[df['SK_ID_CURR'] == id_client]['CODE_GENDER'].any() == 0:
        st.sidebar.markdown('<img src="https://img.icons8.com/color/48/null/checked-user-male.png"/>',
                            unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<img src="https://img.icons8.com/color/48/null/checked-user-female.png"/>',
                            unsafe_allow_html=True)

    # Get data from df to send to Fastapi
    index_client = df[df['SK_ID_CURR'] == id_client].index[0]
    features = df.iloc[index_client]
    features = features.fillna('missing').to_dict()

    # Send data to Fastapi`
    response = requests.post(path_request+'prediction', json=features)

    result = response.json()
    # Get predict proba from Fastapi

    if result['predict_proba'][0]>result['predict_proba'][1]:
        color = 'green'
        image_png = 'logo_congratulations.png'
    else :
        proba_class = (result['predict_proba'][1])*100
        color = 'red'
        image_png = "logo_sorry.png"
    st.image(image_png)


    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        title="Probability of payment default",
        value=result["predict_proba"][1] * 100,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color}
        },
        number={"suffix": "%", "valueformat": ".2f"},
        domain={"x": [0, 1], "y": [0, 1]}
    ))

    st.plotly_chart(fig)



    # Show financial Customer information
    customer_income = df.loc[df['SK_ID_CURR'] == id_client, 'AMT_INCOME_TOTAL'].values[0]
    customer_credit = df.loc[df['SK_ID_CURR'] == id_client,'AMT_CREDIT'].values[0]
    customer_annuity = df.loc[df['SK_ID_CURR'] == id_client, 'AMT_ANNUITY'].values[0]
    m1, m2,m3= st.columns((1, 1,1,))
    m1.metric(label=' Customer Income', value='{:,.0f} $'.format(customer_income))
    m2.metric(label='Customer Credit', value='{:,.0f} $'.format(customer_credit))
    m3.metric(label='Customer Annuity', value='{:,.0f} $'.format(customer_annuity))
    # Histogramm
    g1, g2, g3 = st.columns((1, 1, 1))
    # Show AMT_INCOME_TOTAL
    fig_income, ax = plt.subplots()
    ax.hist(df['AMT_INCOME_TOTAL'], bins=10)
    ax.set_xlabel('INCOME')
    ax.axvline(x=customer_income, color='red')
    g1.pyplot(fig_income)
    #  Show AMT_CREDIT
    fig_credit, ax = plt.subplots()
    ax.hist(df['AMT_CREDIT'], bins=10)
    ax.set_xlabel('CREDIT')
    ax.axvline(x=customer_credit, color='red')
    g2.pyplot(fig_credit)
    # Show AMT_ANNUITY
    fig_annuity, ax = plt.subplots()
    ax.hist(df['AMT_ANNUITY'], bins=10)
    ax.set_xlabel('ANNUITY')
    ax.axvline(x=customer_annuity, color='red')
    g3.pyplot(fig_annuity)

    # Feature importance
    df_features_importance = pd.DataFrame({'Features': result['feature_names'], 'Importance': result['importance']})
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(df_features_importance)),
            df_features_importance['Importance'],
            align='center')
    ax.set_yticks(range(len(df_features_importance)))
    ax.set_yticklabels(df_features_importance['Features'])
    ax.set_ylabel('Feature')
    ax.set_xlabel('Importance')
    ax.set_title('Feature Importances')
    st.pyplot(fig)
