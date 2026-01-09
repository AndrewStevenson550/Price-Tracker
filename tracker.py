import sqlite3
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
from flask import Flask, render_template, redirect, url_for, request
DB_PATH = "/opt/render/project/src/data/price.db"
app = Flask(__name__)

# Ensure the static folder exists for our graphs
if not os.path.exists('static'):
    os.makedirs('static')

class Tracker():
    def __init__(self, url, element, class_name):
        self.url = url
        self.element = element
        self.class_name = class_name

    def webScrap(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
        try:
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, "html.parser")
            info = soup.find(self.element, class_=self.class_name)
            
            if info:
                price_text = info.get_text().strip()
                # Cleaning data: Remove $ and commas
                cleaned_price = price_text.replace("$", "").replace(",", "")
                return float(cleaned_price)
        except Exception as e:
            print(f"Scraping error: {e}")
            return None

    def addPrice(self, price):
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS price (id INTEGER PRIMARY KEY AUTOINCREMENT, price REAL)")
            cur.execute("INSERT INTO price (price) VALUES (?)", (price,))
            con.commit()

    def get_data(self):
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS price (id INTEGER PRIMARY KEY AUTOINCREMENT, price REAL)")
            cur.execute("SELECT * FROM price ORDER BY id DESC")
            return cur.fetchall()

    def deletePrice(self, price_id):
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM price WHERE id = ?", (price_id,))
            con.commit()

    def generate_graph(self, rows):
        if not rows:
            return
        # Extract prices and reverse them so the graph goes left-to-right (oldest to newest)
        prices = [row[1] for row in rows][::-1]
        plt.figure(figsize=(10, 5))
        plt.plot(prices, marker='o', color='#007bff', linewidth=2)
        plt.title('Price Trend')
        plt.xlabel('Days/Checks')
        plt.ylabel('Price ($)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.savefig('static/price_over_time.png')
        plt.close() # Close to free up memory

# Initialize our tracker
my_url = "https://www.pricecharting.com/console/playstation-4"
x = Tracker(url=my_url, element="td", class_name="price numeric new_price")

@app.route('/')
def index():
    # Scrape new data on refresh
    current_price = x.webScrap()
    if current_price:
        x.addPrice(current_price)
    
    # Get all records and generate graph
    rows = x.get_data()
    x.generate_graph(rows)
    
    return render_template("index.html", rows=rows)

@app.route('/delete/<int:price_id>', methods=['POST'])
def delete(price_id):
    x.deletePrice(price_id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)