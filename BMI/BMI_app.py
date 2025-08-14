from flask import Flask, render_template, request

app = Flask(__name__)

class BMICalculator:
    def __init__(self, name, weight, height):
        self.name = name
        self.weight = weight
        self.height = height

    def BMIcal(self):
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)

    def yourCategory(self):
        bmi = self.BMIcal()
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

@app.route("/", methods=["GET", "POST"])
def bmi_form():
    if request.method == "POST":
        name = request.form["name"]
        weight = float(request.form["weight"])
        height = float(request.form["height"])

        person = BMICalculator(name, weight, height)
        bmi = person.BMIcal()
        category = person.yourCategory()

        return render_template("result.html", name=name, bmi=bmi, category=category)

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)