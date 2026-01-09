# 📈 PriceTracker Pro

A full-stack web application built with **Python**, **Flask**, and **SQLite** that scrapes live product prices, stores them in a database, and visualizes trends over time with automated charts.

---

## 🚀 Features
* **Automated Web Scraping:** Uses `BeautifulSoup4` to extract live prices from e-commerce sites.
* **Persistent Storage:** SQLite database integration to track price history.
* **Data Visualization:** Generates trend graphs using `Matplotlib`.
* **Web Dashboard:** A clean, responsive UI built with **Flask** and **Jinja2** templates.
* **Management Tools:** Interactive "Delete" functionality with JavaScript confirmation to manage records.
* **Deployment Ready:** Configured for cloud hosting on platforms like **Render** or **PythonAnywhere**.

---

## 🛠️ Technology Stack
- **Backend:** Python 3.x, Flask
- **Database:** SQLite3
- **Scraping:** Requests, BeautifulSoup4
- **Visualization:** Matplotlib
- **Frontend:** HTML5, CSS3, Jinja2

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/price-tracker.git](https://github.com/your-username/price-tracker.git)
cd price-tracker

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

python app.py
