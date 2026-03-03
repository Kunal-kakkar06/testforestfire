import pickle
from flask import Flask, request, render_template
import pandas as pd

application = Flask(__name__)
app = application

# Load full pipeline model
model = pickle.load(open('models/model.pkl','rb'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():

    if request.method == "POST":

        input_df = pd.DataFrame([{
            'Temperature': float(request.form.get('Temperature')),
            'RH': float(request.form.get('RH')),
            'Ws': float(request.form.get('Ws')),
            'Rain': float(request.form.get('Rain')),
            'FFMC': float(request.form.get('FFMC')),
            'DMC': float(request.form.get('DMC')),
            'DC': float(request.form.get('DC')),
            'ISI': float(request.form.get('ISI')),
            'BUI': float(request.form.get('BUI')),
            'Classes': float(request.form.get('Classes')),
            'Region': float(request.form.get('Region'))
        }])

        result = model.predict(input_df)

        return render_template('home.html', results=round(result[0], 3))

    return render_template('home.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)