from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/contact.html')
def contact():
     return render_template("contact.html")

API_KEY = 'c50a33645d2c478b9d71be98af63584d'
base_currency = 'USD'
API_URL = f'https://open.er-api.com/v6/latest/{base_currency}'
conversion_history = []
def add_history( amount, from_currency, to_currency, result):
    
         conversion_history.append( {
        'amount' : amount,
        'from_currency' : from_currency,
        'to_currency' : to_currency,
        'result' : result
    })
@app.route('/convert', methods=['POST'])
def convert():
    global amount
    amount = float(request.form['amount'])
    global from_currency
    from_currency = request.form['from_currency']
    global to_currency
    to_currency = request.form['to_currency']

    API_URL = f'https://open.er-api.com/v6/latest/{from_currency}'

    response = requests.get(API_URL, params={'apikey': API_KEY})
    
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data['rates'][to_currency] / data['rates'][from_currency]
        global result
        result = amount * exchange_rate
        add_history(amount=amount, from_currency=from_currency, to_currency=to_currency,result=result)
        return jsonify( result=result)
    else:
        return jsonify(error='Failed to fetch exchange rates from the API.')
@app.route('/history.html')
def history():
    global amount, from_currency, to_currency
    if 'amount' not in globals():
       amount = None
    if 'from_currency' not in globals():
       from_currency = None
    if 'to_currency' not in globals():
       to_currency = None
    if 'result' not in globals():
       result = None
    return render_template("history.html", conversion_history=conversion_history, amount=amount, from_currency=from_currency, to_currency=to_currency)
if __name__ == '__main__':
    app.run(debug=True)
