from flask import Flask,request,jsonify,render_template,redirect,url_for
from util import get_predicted_price
import config
import sys
import pandas as pd 
import os 
import re
import traceback
import pymongo
import project_db

app=Flask(__name__)
@app.route("/regestration",methods=["GET","POST"])
def regestration():
    if request.method == 'POST':

        data=request.form
        print("Data: ",data)
        name=data['name']
        emailid=data['emailid']
        mobileno=int(data['mobileno'])
        passward=data['passward']
        response=project_db.save_regestration_details(name,emailid,mobileno,passward)

    return jsonify({"Message":response})

@app.route("/login")
def login():
    data=request.form
    print("data: ",data)
    emailid=data['emailid']
    passward=data['passward']

    resp=project_db.login_user(emailid,passward)
    return jsonify({"Message":resp})

@app.route("/")
def home():
    return render_template("medical_insurance1.html")

@app.route('/predict_charges',methods=['GET','POST'])
def predict_charges():
    try:
        if request.method=="GET":
            data=request.args.get
            print("Data: ",data)
            age=int(data('age'))
            gender=data('gender')
            bmi=eval(data('bmi'))
            children=int(data('children'))
            smoker=data('smoker')
            region=data('region')

            pred_price=get_predicted_price(age,gender,bmi,children,smoker,region)
            project_db.save_predicted_data(age,gender,bmi,children,smoker,region,pred_price)
            return render_template("medical_insurance1.html",prediction=pred_price)
        elif request.method=="POST":

            data=request.form
            print("Data: ",data)
            age=int(data['age'])
            gender=data['gender']
            bmi=int(data['bmi'])
            children=int(data['children'])
            smoker=data['smoker']
            region=data['region']

            pred_price=get_predicted_price(age,gender,bmi,children,smoker,region)
            project_db.save_predicted_data(age,gender,bmi,children,smoker,region,pred_price)
            return render_template("medical_insurance1.html",prediction=pred_price)
    except:
        return print(traceback.print_exc())
if __name__=="__main__":
    app.run(host='0.0.0.0',port=config.PORT_NUMBER)