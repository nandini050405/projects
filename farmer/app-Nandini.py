from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model
model = joblib.load('ml_farmer.lb')

# Load CSV and extract label mapping if needed
df = pd.read_csv('farmer.csv')
label_column = df.columns[-1]  # Last column = crop
df[label_column] = df[label_column].astype('category')
label_map = dict(enumerate(df[label_column].cat.categories))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form inputs
            n = float(request.form['n'])
            p = float(request.form['p'])
            k = float(request.form['k'])
            temp = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])

            # Prepare for prediction
            data = np.array([[n, p, k, temp, humidity, ph, rainfall]])
            prediction = model.predict(data)

            # If model predicts integer codes
            if isinstance(prediction[0], (np.integer, int)):
                crop = label_map.get(prediction[0], "Unknown Crop")
            else:
                # If model predicts crop names directly
                crop = str(prediction[0])

            crop = crop.capitalize()

            return render_template('result.html', crop=crop)

        except Exception as e:
            return f"Something went wrong: {e}"

    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
