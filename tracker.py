#We need to make a tracker that will track every hour (using time) the prices of what we web scrap
import time
import sqlite3
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
con = sqlite3.connect("price.db")
cur = con.cursor()

class Tracker():
    #setting up the vars
    def __init__(self, url, element, class_name, timer_interval):
        self.url = url
        self.element = element
        self.class_name = class_name
        
        self.timer_interval = timer_interval
        
    def webScrap(self):
        class_name = self.class_name
        element = self.element

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            }
            responce = requests.get(self.url, headers=headers, timeout=10)
            responce.raise_for_status() 
            if responce.status_code == 200:
                soup = BeautifulSoup(responce.text, "html.parser")
                information = soup.find_all(element, class_=class_name)
                for info in information:
                    price_text = info.get_text().strip()
                    # Remove symbols so "361.24" becomes a number
                    cleaned_price = price_text.replace("$", "").replace(",", "")
                    self.current_price = float(cleaned_price) 
                    print(f"Current Price Found and Updated: {self.current_price}")

            else:
                print("Failed to retrieve the webpage")

        except RuntimeError as r: 
            print(f"There was an runtime error, {r}")
        except requests.exceptions.RequestException as e:
            print(f"There was an error making the request: {e}")
        except TimeoutError as t:
            print(f"The request timed out: {t}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")
        
    #adding prices
    def addPrice(self):
        current_price = 0
        cur.execute("CREATE TABLE IF NOT EXISTS price (id INTEGER PRIMARY KEY AUTOINCREMENT, price REAL)")
        cur.execute("INSERT INTO price (price) VALUES (?)", (current_price,))
        con.commit()
        pass
    def printPrices(self):
        cur.execute("SELECT * FROM price")
        rows = cur.fetchall()
        
        # 1. Create a list of prices from the database rows
        # Since your table has (id, price), the price is at index 1
        prices = [row[1] for row in rows]
        
        for row in rows:
            print(row)
            
        # 2. Plot the list of prices instead of just one number
        if prices:
            plt.plot(prices, marker='o') # 'o' adds dots so you can see single entries
            plt.xlabel('Entry Number')
            plt.ylabel('Price')
            plt.title('Price Over Time')
            plt.savefig('price_over_time.png')  # Save the plot as a PNG file
        else:
            print("No data available to plot.")

    def waitTime(self):
          # 1 hour in seconds
        self.addPrice()
        if self.timer_interval > 0:
            print(f"Waiting for {self.timer_interval} seconds before the next check...")
            time.sleep(self.timer_interval)
        else:
            self.addPrice()
        pass
    
my_url = "https://www.pricecharting.com/console/playstation-4"
x = Tracker(url=my_url, element="td", class_name="price numeric new_price", timer_interval=3600)
while True:
    x.webScrap()
    x.addPrice()
    x.waitTime()
    x.printPrices()