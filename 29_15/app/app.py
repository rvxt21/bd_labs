from flask import Flask, render_template, request
from app.create_db import DBCurrency


class CurrencyConverterApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.db_currency = DBCurrency('currency_rates.db')


        self.app.add_url_rule('/', 'index', self.index, methods=['GET', 'POST'])

    def index(self):
        currencies = self.db_currency.get_currencies()
        result = None
        if request.method == 'POST':
            currency1_id = request.form.get('currency1')
            currency2_id = request.form.get('currency2')
            amount = float(request.form.get('amount'))
            result = self.db_currency.convert_currency(currency1_id, currency2_id, amount)
        
        return render_template('index.html', currencies=currencies, result=result)  
    
    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app = CurrencyConverterApp()
    app.run()