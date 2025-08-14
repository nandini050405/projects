from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the trained model safely
MODEL_PATH = 'ml_credit.lb'
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model file not found: ml_credit.lb")

model = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict_form():
    return render_template('predict.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        # Extract and validate form inputs
        job = int(request.form.get('job', -1))
        marital = int(request.form.get('marital', -1))
        education = int(request.form.get('education', -1))
        housing = int(request.form.get('housing', -1))
        approval = int(request.form.get('approval', -1))
        age = float(request.form.get('age', -1))
        balance = float(request.form.get('balance', 0))
        duration = float(request.form.get('duration', 0))

        # Check for valid input ranges
        if not (0 <= job <= 2 and 0 <= marital <= 2 and 0 <= education <= 2 and
                0 <= housing <= 1 and 0 <= approval <= 1 and
                18 <= age <= 100 and duration > 0):
            raise ValueError("Invalid input values.")

        # Create input array for model
        input_data = np.array([[job, marital, education, housing, approval, age, balance, duration]])

        # Make prediction
        prediction = model.predict(input_data)[0]
        result_text = "✅ Approved" if prediction == 1 else "❌ Not Approved"

        return render_template('result.html', prediction=result_text)

    except Exception as e:
        return render_template('result.html', prediction=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
