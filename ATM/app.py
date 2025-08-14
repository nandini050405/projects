# atm_web_app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulated ATM class
class ATM:
    def __init__(self, balance):
        self.balance = balance
        self.pin = "2005"
        self.name = "User"

    def authenticate(self, entered_pin):
        return entered_pin == self.pin

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"✅ Deposited ₹{amount:.2f} successfully."
        return "❌ Invalid deposit amount."

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return f"✅ Withdrawn ₹{amount:.2f} successfully."
        return "❌ Insufficient balance."

    def check_balance(self):
        return self.balance

# Create an ATM object
atm = ATM(500000)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pin = request.form.get("pin")
        if atm.authenticate(pin):
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="❌ Incorrect PIN")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    message = ""
    if request.method == "POST":
        action = request.form.get("action")
        amount = request.form.get("amount", type=float)

        if action == "balance":
            message = f"💰 Balance: ₹{atm.check_balance():.2f}"
        elif action == "deposit" and amount is not None:
            message = atm.deposit(amount)
        elif action == "withdraw" and amount is not None:
            message = atm.withdraw(amount)
        else:
            message = "❌ Invalid action or amount."

    return render_template("dashboard.html", name=atm.name, balance=atm.check_balance(), message=message)

if __name__ == "__main__":
    app.run(debug=True)