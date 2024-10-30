import sqlite3
import os

class DBCurrency:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            self.create_db()
            
    def create_db(self):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS currencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(3) UNIQUE NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS exchange_rates (
            currency1_id INTEGER,
            currency2_id INTEGER,
            rate REAL,
            PRIMARY KEY (currency1_id, currency2_id),
            FOREIGN KEY (currency1_id) REFERENCES currencies (id),
            FOREIGN KEY (currency2_id) REFERENCES currencies (id)
        )
        ''')
        
        # Insert sample data into currencies table
        currencies = [
            ('UAH',),
            ('USD',),
            ('EUR',)
        ]
        cursor.executemany('INSERT OR IGNORE INTO currencies (code) VALUES (?)', currencies)

        exchange_rates = [
            (1, 2, 0.024),  # UAH to USD
            (1, 3, 0.022),  # UAH to EUR
            (2, 1, 41.30),   # USD to UAH
            (3, 1, 44.66),  # EUR to UAH
        ]
        cursor.executemany('INSERT OR IGNORE INTO exchange_rates (currency1_id, currency2_id, rate) VALUES (?, ?, ?)', exchange_rates)
        
        conn.commit()
        conn.close()
    
    def get_currencies(self):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute("SELECT id, code FROM currencies")
        currencies = cursor.fetchall()
        conn.close()
        return currencies

    def convert_currency(self, currency1_id, currency2_id, amount):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute("SELECT rate FROM exchange_rates WHERE currency1_id=? AND currency2_id=?", (currency1_id, currency2_id))
        result = cursor.fetchone()
        conn.close()
        if result:
            return amount * result[0]
        return None
    

if __name__ == '__main__':
    db = DBCurrency('currency_rates.db')
    
