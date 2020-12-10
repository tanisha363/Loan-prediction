from flask import Flask, render_template, json, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import MySQLdb
import os
import json
import numpy as np
import pandas as pd
#from sklearn.externals import joblib
from sklearn.model_selection import train_test_split  # , GridSearchCV
#from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import tree
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from numpy import array
import io
import graphviz
import image
from PIL import Image

app = Flask(__name__)

app = Flask(__name__)
app.static_folder = 'static'



@app.route("/")
def main():
    return render_template("index.html")


""" @app.route("/showLender")
def showLender():
    return render_template("lender.html")
 """

@app.route("/showBorrower")
def showBorrower():
    return render_template("borrower.html")


""" @app.route("/showSignUp")
def showSignUp():
    return render_template("signup.html") """


@app.route("/showResult")
def showResult(prediction):
    return render_template("gallery.html", result=prediction)


@app.route('/signUp', methods=["POST"])
def signUp():
   #  create user code will be here !!
   #  read the posted values from the UI
    cur = mysql.connection.cursor()
    conn = MySQLdb.connect(host="localhost", user="root",
                           password="", db="loan_prediction")
    _name = request.form['name']
    _email = request.form['email']
    _password = request.form['password']

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (Name,Email,Password)VALUES(%s,%s,%s)", (_name, _email, _password))
    conn.commit()
    return redirect(url_for("showLogin"))


@app.route("/predict", methods=['GET', 'POST'])
def predict():

    # reading csv data
    data = pd.read_csv(os.getcwd()+"/customer_loan_details.csv")

    # List Attributes
    print(list(data.columns))

    # Shape of Data
    print(data.shape)

    # Checking for any null values for the attributes
    for _ in data.columns:
        print("The number of null values in:{} == {}".format(
            _, data[_].isnull().sum()))

  
    x = data.iloc[:, 1:13].values
    y = data.iloc[:, 13].values

    
    le = LabelEncoder()
    y = le.fit_transform(y)
    y = y.reshape(684, 1)
  
    x[:, 0] = le.fit_transform(x[:, 0])
    x[:, 0] = x[:, 0].reshape(684)
 
    x[:, 1] = le.fit_transform(x[:, 1])
    x[:, 1] = x[:, 1].reshape(684)
    
    x[:, 3] = le.fit_transform(x[:, 3])
    x[:, 3] = x[:, 3].reshape(684)
    # marital_status
    # Married=1,Single=2,Divorced=0
    x[:, 4] = le.fit_transform(x[:, 4])
    x[:, 4] = x[:, 4].reshape(684)
    # occupation
    # NYPD=4,IT=2,Accout=0,Business=1,Manager=3
    x[:, 5] = le.fit_transform(x[:, 5])
    x[:, 5] = x[:, 5].reshape(684)
    # loan_type
    # Personal=3,Auto=0,Credit=1,Home=2
    x[:, 9] = le.fit_transform(x[:, 9])
    x[:, 9] = x[:, 9].reshape(684)
    # Property
    # Urban=2,Rural=0,SemiUrban=1
    x[:, 11] = le.fit_transform(x[:, 11])
    x[:, 11] = x[:, 11].reshape(684)

    # Training and Test Data
    train_feature, test_feature, train_target, test_target = train_test_split(
        x, y, test_size=0.25, random_state=0)
    

    # Implementing Decision Tree Algorithm
    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(train_feature, train_target)
   

   

    # user input
    _state = request.form['state']
    _gender = request.form['gender']
    _age = int(request.form['age'])
    _race = request.form['race']
    _marital_status = request.form['marital_status']
    _occupation = request.form['occupation']
    _credit_score = int(request.form['credit_score'])
    _income = float(request.form['income'])
    _debts = float(request.form['debts'])
    _loan_type = request.form['loan_type']
    _LoanAmount = int(request.form['LoanAmount'])
    _Property = request.form['Property']

    # categorical data
    select_state = {'JK': 1, 'Ladakh': 2, 'Punjab': 3, 'Haryana': 4, 'Delhi': 5, 'Rajasthan': 6, 'UP': 7, 'Mhegalaya': 8, 'UK': 9, 'Bihar': 10, 'Gujarat': 11, 'MP': 12,
                    'WB': 13, 'Jharkhand': 14, 'Assam': 15, 'Arunachalpradesh': 16, 'Orissa': 17, 'Telangana': 18, 'Maharastra': 19, 'Andhra pradesh': 20, 'Karnataka': 21, 'Tamilnadu': 22, 'Kerala': 23,
                    }
    _state = select_state.get(_state, "Invalid state")

    select_gender = {'Male': 1, 'Female': 0}
    _gender = select_gender.get(_gender, "Invalid gender")

    select_race = {'Non-Coapplicant': 4, 'White': 6, 'Not applicable': 5, 'Asian': 1, 'American': 0,
                   'Indian': 3, 'Black African': 2}
    _race = select_race.get(_race, "Invalid race")
    select_ms = {'Married': 1, 'Single': 2, 'Divorced': 0}
    _marital_status = select_ms.get(_marital_status, "Invalid marital_status")

    select_occupation = {'Govt': 4, 'IT': 2,
                         'Accountant': 0, 'Business': 1, 'Manager': 3}
    _occupation = select_occupation.get(_occupation, "Invalid occupation")

    select_loan_type = {'Personal': 3, 'Auto': 0, 'Credit': 1, 'Home': 2}
    _loan_type = select_loan_type.get(_loan_type, "Invalid loan_type")

    select_property = {'Urban': 2, 'Rural': 0, 'SemiUrban': 1}
    _Property = select_property.get(_Property, "Invalid property")

    user_input = [_state, _gender, _age, _race, _marital_status, _occupation, _credit_score, _income, _debts,
                  _loan_type, _LoanAmount, _Property]

    user_input = array(user_input)
    user_input = user_input.reshape(1, 12)

    result = classifier.predict(user_input)

    if result == 0:
        prediction = "Your Loan Will Get Approved!"
    else:
        prediction = "Your Loan Will Not Get Approved"

    probability = classifier.predict_proba(user_input)

    return showResult(prediction)

def add(a,b):
    return (a + b) 

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8000)

