from flask import Flask, request, render_template
from main import get_minimum_charges, get_minimum_time
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sender = request.form.get("senderAccountNumber")
        receiver = request.form.get("receiverAccountNumber")
        amount = request.form.get("amount")
        transaction_type = request.form.get("transactionType")

        # Get the required cost/time based on the transaction type
        if transaction_type == "cheapest":
            charge_time = f"₹{get_minimum_charges(request)}"
        else:
            charge_time = f"{get_minimum_time(request)} minutes"

        # Create transaction details
        transaction_details = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "transaction_type": transaction_type.capitalize(),
            "charge_time": charge_time,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Render only the transaction receipt
        return render_template("receipt.html", transaction_details=transaction_details)

    return render_template("index.html")  # Show form initially

if __name__ == "__main__":
    app.run(debug=True)
