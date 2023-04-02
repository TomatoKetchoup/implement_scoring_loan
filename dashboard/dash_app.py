
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import os
import plotly.graph_objs as go



if os.environ.get('IS_HEROKU', '') != '':
    # Vous êtes en production sur Heroku, utilisez la variable d'environnement pour définir le chemin d'accès à votre fichier CSV
    path_request = 'https://apiscoringloan-tomatoketchoup.herokuapp.com/'
    path_df = 'https://raw.githubusercontent.com/TomatoKetchoup/implement_scoring_loan/main/dashboard/'

else:
    # Vous êtes en train de travailler localement, utilisez le chemin de fichier local
    path_request = 'http://127.0.0.1:8000/'
    path_df = 'C:/Users/td/implement_scoring_loan/dashboard/'
path_df = 'https://raw.githubusercontent.com/TomatoKetchoup/implement_scoring_loan/main/dashboard/'
df = pd.read_csv(path_df+'df_api.csv', nrows= 10)


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
    # Get data from df to send to Fastapi
    id_client = int(id_client)
    index_client = df[df['SK_ID_CURR'] == id_client].index[0]
    features = df.iloc[index_client].to_dict()
    # Send data to Fastapi1`
    response = requests.post(path_request+'prediction', json=features)

    # Afficher la réponse de FastAPI

    result = response.json()
    # Get predict proba from Fastapi
    exp_score = result['model reliability']

    if result['predict_proba'][0]>result['predict_proba'][1]:
        color = 'green'
        image_url = 'https://img.icons8.com/emoji/48/null/bottle-with-popping-cork.png'
    else :
        proba_class = (result['predict_proba'][1])*100
        color = 'red'
        image_url = "https://img.icons8.com/external-justicon-lineal-color-justicon/64/null/external-storm-spring-season-justicon-lineal-color-justicon.png"
    st.image(image_url)
    st.write(f"Prediction reliability: {exp_score:.2f}")
    st.progress(exp_score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        title = 'Probability of payment default',
        value=result['predict_proba'][1]*100,
        gauge= {'bar': {'color': color}},
        number={'suffix': "%", 'valueformat': '.2f'},
        domain={'x': [0, 1], 'y': [0, 1]}))
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
