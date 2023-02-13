import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title('🤑  Dashboard : Customer Loan')
log_reg_pickle = open('model_saved_loan.pickle', 'rb')
cust_info_pickle=open('cust`omers_info','rb')
log_reg=pickle.load(log_reg_pickle)
customer_infos=pickle.load(cust_info_pickle)
nb_customer=np.unique(customer_infos['SK_ID_CURR'])
customer_number=st.selectbox('Customer Number',options=nb_customer)
customer_annuity=customer_infos[customer_infos['SK_ID_CURR']==customer_number]['AMT_ANNUITY']
credit_customer=customer_infos[customer_infos['SK_ID_CURR']==customer_number]['AMT_CREDIT']
st.write('Credit :'+"${:,.2f}".format(credit_customer.iloc[0]))
st.write('Annuity :'+"${:,.2f}".format(customer_annuity.iloc[0]))


# if st.button("Refresh"):
#     st.experimental_rerun()






