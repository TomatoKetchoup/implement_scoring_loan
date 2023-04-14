
<h1 align="center">Classifier application to credit risk assessment</h1>

  <p align="center">
    Ensure your transactions by knowing whether a customer will default before granting them their credit
    <br/>

## About The Project


This project involves developing a <b>credit scoring</b> tool for the financial company "Prêt à dépenser" that offers consumer loans for individuals with little or no loan history.<br>

The scoring tool must calculate the <b>probability that a customer will repay their loan</b> and <b>classify</b> the application as <b>approved</b> or <b>denied</b>.

The company also wants to develop an <b>interactive dashboard</b> for customer relationship managers to <b>transparently explain credit approval decisions</b> and enable customers to easily access and explore their personal information.

## Built With

 📍 <b>Jupyter Notebook</b> : web-based interactive computing environment <br>

 📍 <b>PyCharm</b> : An integrated development environment (IDE) used for programming in Python.<br>

 📍 <b>FastAPI</b> : web framework for building APIs with Python <br>

 📍 <b>MLflow</b> :An open source platform for the complete machine learning lifecycle<br>

 📍 <b>Heroku</b> : A cloud-based platform that allows developers to deploy, manage, and scale their applications
 
## Installation:

1. Clone the GitHub repository

2. Install dependencies with : pip install -r requirements.txt

## Usage:

📍 Run the FastAPI server with "uvicorn main:app --reload" <br>

📍 Launch the Streamlit application with "streamlit run app.py"<br>

📍 Fill in the required fields in the user interface<br>

📍 Click on the "Predict" button to get predictions<br>

## Operation:
📍 The Streamlit application connects to the FastAPI server to make predictions on a trained model. <br>

📍 Predictions are based on features submitted by the user through the user interface.<br>

📍 The FastAPI server uses a machine learning model to predict an output based on the features provided by the user. <br>

📍 Results are returned to the Streamlit application, which displays the predictions and other useful information.<br>

📍 The machine learning model is based on a preprocessing pipeline, a classification model, and an explanation tool. <br>

📍 The explanation tool is used to identify the most important features that contributed to the prediction.

![img.png](img.png)

## Link to Heroku

https://dashscoringloan-tomatoketchoup.herokuapp.com