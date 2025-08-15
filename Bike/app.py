from flask import Flask, render_template, request, url_for
import joblib

app = Flask(__name__)
model = joblib.load('model.lb')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')  

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        brand_name = request.form['brand_name']
        owner = request.form['owner']
        age = request.form['age']
        power = request.form['power']
        kms_driven = request.form['kms_driven']

        # Convert to proper types
        try:
            owner = int(owner)
            age = int(age)
            power = float(power)
            kms_driven = int(kms_driven)
        except ValueError:
            return render_template('project.html', prediction="Invalid input type.")

        # Dictionary for encoding brand names
        bike_number = {'TVS':0, 'Royal Enfield':1, 'Triumph':2, 'Yamaha':3, 'Honda':4, 'Hero':5,
            'Bajaj':6, 'Suzuki':7, 'Benelli':8, 'KTM':9, 'Mahindra':10, 'Kawasaki':11,
            'Ducati':12, 'Hyosung':13, 'Harley-Davidson':14, 'Jawa':15, 'BMW':16, 'Indian':17,
            'Rajdoot':18, 'LML':19, 'Yezdi':20, 'MV':21, 'Ideal':22}
        
        if brand_name not in bike_number:
            return render_template('project.html', prediction="Invalid brand name selected.")

        brand_encoded = bike_number[brand_name]
        input_vector = [brand_encoded, owner, age, power, kms_driven]

        # Prediction
        try:
            pred = model.predict([input_vector])[0]
            pred = round(pred, 2)
        except Exception as e:
            return render_template('project.html', prediction=f"Prediction error: {e}")

        return render_template('project.html', prediction=pred)

    return render_template('project.html', prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
