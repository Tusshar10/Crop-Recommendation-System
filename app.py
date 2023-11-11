from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle
from utils import humtem,rainfall

app=Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/',methods=['POST','GET'])
def index():
    if(request.method=='GET'):
        return render_template("index.html")
    else:
        crop={}
        crop['N'] = request.form['nitrogen']
        crop['P'] = request.form['phosphorus']
        crop['K'] = request.form['potassium']
        crop['ph'] = request.form['pH']
        crop['state']=request.form['state']
        crop['district']=request.form['district']
        crop['month']=request.form['Month']
        crop['rain']=rainfall.get_rainfall(crop['state'],crop['district'],crop['month'])
        crop['temperature'],crop['humidity']=humtem.get_temp_hum(crop['district'],crop['state'])
        data = np.array([[crop['N'], crop['P'], crop['K'], crop['temperature'], crop['humidity'], crop['ph'], crop['rain']]])
        feature_names = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "pH", "Rainfall"]
        df = pd.DataFrame(data, columns=feature_names)
        predict = model.predict(df)
        crop['name']=predict[0]
        return render_template("crop.html",crop=crop)

if __name__=="__main__":
    app.run(debug=True)