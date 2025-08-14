from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load('ml_farmer.lb')

# Load the CSV to create label mapping
df = pd.read_csv('farmer.csv')
label_column = df.columns[-1]  # assuming the last column is the label
df[label_column] = df[label_column].astype('category')
label_map = dict(enumerate(df[label_column].cat.categories))  # int -> crop name

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get input data from form
            n = float(request.form['n'])
            p = float(request.form['p'])
            k = float(request.form['k'])
            temp = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])

            # Make prediction
            data = np.array([[n, p, k, temp, humidity, ph, rainfall]])
            prediction = model.predict(data)
            label = prediction[0]
            

            # Convert label to crop name
            crop = label_map.get(label, "Unknown Crop").capitalize()
           
            return render_template('result.html', crop=crop)

        except Exception as e:
            return f"Something went wrong: {e}"

    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
