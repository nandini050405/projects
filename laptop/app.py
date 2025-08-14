from flask import Flask, render_template, request, url_for
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('ml_laptop_Price.lb')

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
        brand = request.form['brand']
        processor_brand = request.form['processor_brand']
        processor_name = request.form['processor_name']
        ram = request.form['ram']
        hdd = request.form['hdd']
        ssd = request.form['ssd']
        os = request.form['os']
        os_bit = request.form['os_bit']
        warranty = request.form['warranty']
        weight= request.form['weight']
        graphics_card = request.form['graphics_card']
        touchscreen = request.form['touchscreen']
        msoffice = request.form['msoffice']
        rating = request.form['rating']
        screen_size = request.form['screen_size']

        # Convert numerical inputs
        try:
            ram = int(ram)
            hdd = int(hdd)
            ssd = int(ssd)
            os_bit = int(os_bit)
            warranty = int(warranty)
            weight = float(weight)
            graphics_card = int(graphics_card)
            touchscreen = int(touchscreen)
            msoffice = int(msoffice)
            rating = float(rating)
            screen_size = float(screen_size)
        except ValueError:
            return render_template('project.html', prediction="Invalid numeric input.")

        # Encoding dictionaries
        brand_dict = {'ASUS': 1, 'Lenovo': 2, 'acer': 3, 'Avita': 4, 'HP': 5, 'DELL': 6, 'MSI': 7, 'APPLE': 8}
        processor_name_dict = {'i3': 1, 'i5': 2, 'i7': 3, 'Ryzen 3': 4, 'Ryzen 5': 5, 'Ryzen 7': 6}
        processor_brand_dict = {'Intel': 0, 'M1': 1, 'AMD': 2}
        os_dict = {'Windows':0,'Dos':1,'Mac':2}

        # Get encoded values
        brand_encoded = brand_dict.get(brand)
        processor_brand_encoded = processor_brand_dict.get(processor_brand)
        processor_name_encoded = processor_name_dict.get(processor_name)
        os_encoded = os_dict.get(os)


        if None in [brand_encoded, processor_brand_encoded,processor_name_encoded,os_encoded]:
            return render_template('project.html', prediction="Invalid categorical input.")

        # Final input vector for prediction
        input_vector = [brand_encoded, processor_brand_encoded, processor_name_encoded, ram, ssd, hdd, weight, os_encoded, warranty, graphics_card, os_bit, touchscreen, msoffice, rating, screen_size]

        # Predict price
        try:
            pred = model.predict([input_vector])[0]
            pred_value = round(float(pred),2)
        except Exception as e:
            return render_template('project.html', prediction=f"Prediction error: {e}")

        return render_template('project.html', prediction=f"{pred_value}")

    return render_template('project.html', prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
