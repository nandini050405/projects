from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.lb')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect input from form
        age = int(request.form['age'])
        sex = 1 if request.form['sex'].lower() == 'male' else 0
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = 1 if request.form['smoker'].lower() == 'yes' else 0
        region = request.form['region'].lower()

        # Region encoding
        region_map = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}
        region_encoded = region_map.get(region, 0)  # Default to 0 if region not found

        # Prepare input for prediction
        features = np.array([[age, sex, bmi, children, smoker, region_encoded]])
        prediction = model.predict(features)[0]

        return render_template('result.html', prediction=round(prediction, 2))
    
    except Exception as e:
        # You could log the error if needed
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
