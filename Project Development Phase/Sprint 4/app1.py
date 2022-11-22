#### This is the IBM model file 


# importing required librariessklearnsklearn

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import warnings
from sklearn import metrics
import requests
import pickle
from feature import FeatureExtraction
warnings.filterwarnings('ignore')

file = open("model.pkl", "rb")
gbc = pickle.load(file)
file.close()


API_KEY = "Rx4qW5JQqFI7p7emOlpR-2uo71MeEC1Xyjdh5TiMIZlQ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", xx=-1)


@app.route("/urldetect", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

    #     # Feature list from input URL
    #     payload_scoring = {"input_data": [
    #         {"fields": [obj.getFeaturesList()], "values": x.tolist()}]}

    #     response_scoring = requests.post('https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/web_phishing_model_nalaiya_thiran/predictions?version=2022-11-22',
    #                                      json=payload_scoring,
    #                                      headers={'Authorization': 'Bearer ' + mltoken}).json()

    #     _pred = response_scoring
    #     print(_pred)
    #     output = _pred['predictions'][0]['values'][0][1][1]

    #     print(output)
    #     # Response from IBM Cloud Model rendered to UI from Flask
    #     return render_template('index.html', xx=output, url=url)
    # return render_template("index.html", xx=-1)

        y_pred = gbc.predict(x)[0]
        #1 is safe
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0, 0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('index.html', xx=round(y_pro_non_phishing, 2), url=url)
    return render_template("index.html", xx=-1)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
