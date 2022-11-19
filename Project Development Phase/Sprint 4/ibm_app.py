from flask import Flask, render_template,request,jsonify
import pickle
import inputScript
import numpy as np
from flask_cors import CORS
import requests

import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "ebYz4uHMy0S-ZaJ_x2OB-gP_xvIBur-Ecgp_W8sm0UxF"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}




app = Flask(__name__)
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/final')
def  final():
    
    return render_template("final.html")

@app.route('/y_predict',methods=['POST'])
def y_predict():
    
    
    url = request.form['URL']
    checkprediction = inputScript.main(url)
    
    payload_scoring = {"input_data": [{"field": [["f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16","f17","f18","f19","f20","f21","f22","f23","f24","f25","f26","f27","f28","f29"]], "values": checkprediction}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/89f1da33-fd1e-4707-9700-ce517b0f2b99/predictions?version=2022-11-18', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    
    prediction=(response_scoring.json())
    output=prediction['predictions'][0]['values'][0][0]

    #prediction =loaded_model.predict(checkprediction)
    #print(prediction) 
    #output=prediction[0]


    if(output==-1):
        pred = "You are safe!! This is a Legimate Website "
    elif(output==1):
        pred = "You are in a phishing site. Dont Trust "
    else:
        pred = "You are in a suspecious site. Be Cautious "
    print(pred)
    return render_template('final.html', prediction_text='{}'.format(pred),url=url)
    
"""@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = loaded_model.y_predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)"""

if __name__ == '__main__':
   app.run()
