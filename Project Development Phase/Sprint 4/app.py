# from flask import Flask, request, render_template
# from googlesearch import search
# import numpy as np
# import pandas as pd
# from sklearn import metrics
# from feature import FeatureExtraction
# import requests
# # file = open("model.pkl","rb")
# # gbc = pickle.load(file)
# # file.close()


# # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
# API_KEY = "Rx4qW5JQqFI7p7emOlpR-2uo71MeEC1Xyjdh5TiMIZlQ"
# token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
#  API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
# mltoken = token_response.json()["access_token"]

# header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# app = Flask(__name__)

# @app.route("/", methods=["GET", "POST"])
# def home():
#     return render_template("index.html", xx =-1)

# @app.route("/urldetect", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":

#         url = request.form["url"]
#         obj = FeatureExtraction(url)
#         x = np.array(obj.getFeaturesList()).reshape(1,30)

#         y_pred =gbc.predict(x)[0]
#         #1 is safe
#         #-1 is unsafe
#         y_pro_phishing = gbc.predict_proba(x)[0,0]
#         y_pro_non_phishing = gbc.predict_proba(x)[0,1]
#         # if(y_pred ==1 ):
#         pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
#         return render_template('index.html',xx =round(y_pro_non_phishing,2),url=url )
#     return render_template("index.html", xx =-1)


# if __name__ == "__main__":
#     app.run(debug=True,port=2002)

# ------------------------------------------------------------------------------------------------------
# -------------------------------------

from flask import Flask, render_template, redirect, url_for
from feature import FeatureExtraction
from googlesearch import search
import numpy as np
import pandas as pd
from sklearn import metrics
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html", xx=-1)


@app.route("/urldetect", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

    # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
    API_KEY = "Rx4qW5JQqFI7p7emOlpR-2uo71MeEC1Xyjdh5TiMIZlQ"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
        "apikey": API_KEY,
        "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
    })
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + mltoken}
    payload_scoring = {
        "input_data": [{"fields": [["UsingIP", "LongURL", "ShortURL", "Symbol@", "Redirecting//", "PrefixSuffix-", "SubDomains", "HTTPS", "DomainRegLen", "Favicon", "NonStdPort", "HTTPSDomainURL", "RequestURL", "AnchorURL", "LinksInScriptTags", "ServerFormHandler", "InfoEmail", "AbnormalURL", "WebsiteForwarding", "StatusBarCust", "DisableRightClick", "UsingPopupWindow", "IframeRedirection", "AgeofDomain", "DNSRecording", "WebsiteTraffic", "PageRank", "GoogleIndex", "LinksPointingToPage", "StatsReport"
                                    ]], "values": []
                        }
                       ]}

    response_scoring = requests.post(
        'https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/web_phishing_nalaiya_thiran/predictions?version=2022-11-22',
        json=payload_scoring,
        headers=header
    ).json()

    print(response_scoring)


@ app.route('/<path:path>')
def catch_all():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
