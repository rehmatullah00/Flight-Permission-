# 📁 Project Structure
# Smart Flight Permit Tracker & Status Notifier

# Folder Structure:
# smart_flight_permit/
# ├── app.py                      # Main Flask app
# ├── templates/
# │   ├── index.html            # Submit permit form
# │   ├── dashboard.html         # Admin panel
# ├── static/
# │   ├── style.css            # Basic styling
# ├── database.py                 # DB connection and setup
# ├── permit_model.py             # Optional ML prediction logic
# ├── notifier.py                 # Email/WhatsApp notifications
# ├── README.md                   # Project intro and run instructions
# ├── requirements.txt            # Packages to install

# ✅ app.py

from flask import Flask, render_template, request, redirect
# from database import  add_permit_request, get_all_requests, update_status, delete_request
from notifier import send_notification

app = Flask(__name__)
# init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    flight_no = request.form['flight_no']
    country = request.form['country']
    email = request.form['email']
    add_permit_request(name, flight_no, country, email)
    return "Request Submitted Successfully!"

@app.route('/admin')
def admin():
    permits = get_all_requests()
    return render_template('dashboard.html', permits=permits)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    new_status = request.form['status']
    update_status(id, new_status)
    send_notification(id)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)


# ✅ database.py

import sqlite3

def init_db():
    conn = sqlite3.connect('permits.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS permits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            flight_no TEXT,
            country TEXT,
            email TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

def add_permit_request(name, flight_no, country, email):
    conn = sqlite3.connect('permits.db')
    c = conn.cursor()
    c.execute("INSERT INTO permits (name, flight_no, country, email) VALUES (?, ?, ?, ?)",
              (name, flight_no, country, email))
    conn.commit()
    conn.close()

def get_all_requests():
    conn = sqlite3.connect('permits.db')
    c = conn.cursor()
    c.execute("SELECT * FROM permits")
    results = c.fetchall()
    conn.close()
    return results

def update_status(permit_id, new_status):
    conn = sqlite3.connect('permits.db')
    c = conn.cursor()
    c.execute("UPDATE permits SET status = ? WHERE id = ?", (new_status, permit_id))
    conn.commit()
    conn.close()
def delete_request(permit_id):
    conn = sqlite3.connect('permits.db')
    c = conn.cursor()
    c.execute("DELETE FROM permits WHERE id = ?", (permit_id,))
    conn.commit()
    conn.close()
