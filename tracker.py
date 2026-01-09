import sqlite3
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from flask import Flask

# making the flask stuff
app = Flask(__name__)

class Tracker():
    def __init__(self, url, element, class_name, timer_interval):
        self.url = url
        self.element = element
        self.class_name = class_name
        self.timer_interval = timer_interval
        self.current_price = 0

    def webScrap(self):
        print("Starting web scraping...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, "html.parser")
            information = soup.find_all(self.element, class_=self.class_name)
            
            # For simplicity, we'll take the first price found
            if information:
                price_text = information[0].get_text().strip()
                cleaned_price = price_text.replace("$", "").replace(",", "")
                self.current_price = float(cleaned_price)
                return self.current_price
        except Exception as e:
            print(f"Scraping error: {e}")
            return None

    def addPrice(self, price):
        # Local connection to avoid SQLite threading issues
        with sqlite3.connect("price.db") as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS price (id INTEGER PRIMARY KEY AUTOINCREMENT, price REAL)")
            cur.execute("INSERT INTO price (price) VALUES (?)", (price,))
            con.commit()

    def printPrices(self):
        with sqlite3.connect("price.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM price")
            rows = cur.fetchall()
        
        if not rows:
            return "No data found in database yet."

        # Prepare a string to send to the web browser
        output = "<h1>Price History</h1><ul>"
        prices = []
        for row in rows:
            output += f"<li>ID: {row[0]} - Price: ${row[1]}</li>"
            prices.append(row[1])
        output += "</ul>"

        # Create Plot
        plt.figure()
        plt.plot(prices, marker='o')
        plt.savefig('price_over_time.png') # Flask likes files in a /static folder
        
        return output

# 1. Create the instance
my_url = "https://www.pricecharting.com/console/playstation-4"
x = Tracker(url=my_url, element="td", class_name="price numeric new_price", timer_interval=3600)

# 2. Define Routes
@app.route('/')
def index():
    # Example: Scrap a price and add it to DB every time page is refreshed
    # In a real app, you'd do this in a background thread
    new_price = x.webScrap()
    if new_price:
        x.addPrice(new_price)
    
    return x.printPrices()

# 3. Run Flask at the very end
if __name__ == "__main__":
    app.run(debug=True)