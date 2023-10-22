from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import sklearn
import pickle
from utils import humtem,rainfall

app=Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/',methods=['POST','GET'])
def index():
    if(request.method=='GET'):
        return render_template("index.html")
    else:
        N = request.form['nitrogen']
        P = request.form['phosphorus']
        K = request.form['potassium']
        ph = request.form['pH']
        state=request.form['state']
        district=request.form['district']
        month=request.form['Month']
        rain=rainfall.get_rainfall(state,district,month)
        temperature,humidity=humtem.get_temp_hum(district,state)
        data = np.array([[N, P, K, temperature, humidity, ph, rain]])
        feature_names = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "pH", "Rainfall"]
        df = pd.DataFrame(data, columns=feature_names)
        predict = model.predict(df)
        return render_template("crop.html",crop=predict[0])

if __name__=="__main__":
    app.run(debug=True)