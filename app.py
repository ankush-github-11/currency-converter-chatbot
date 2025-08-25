from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
@app.route("/", methods=['POST'])
def index():
    data = request.get_json()
    amount = data["queryResult"]["parameters"]["unit-currency"]["amount"]
    source_currency = data["queryResult"]["parameters"]["unit-currency"]["currency"]
    target_currency = data["queryResult"]["parameters"]["currency-name"]
    target_amount = round(fetchCurrencyFactor(amount, source_currency, target_currency), 2)
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, target_amount, target_currency)
    }
    return jsonify(response)
def fetchCurrencyFactor(amount, source_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/897b6b5ee1e617cf3161e3e7/latest/{source_currency}"
    res = requests.get(url)
    currencyJSON = res.json()
    if res.status_code == 200:
        currencyJSON = res.json()
        rate = currencyJSON["conversion_rates"].get(target_currency)
        if rate: return amount * rate
        else: return None
    else: return None
if __name__ == "__main__":
    app.run(debug=True)