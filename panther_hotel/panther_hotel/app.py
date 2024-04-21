from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# Database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create tables if not exists
c.execute('''CREATE TABLE IF NOT EXISTS reservations (
             id INTEGER PRIMARY KEY,
             name TEXT,
             email TEXT,
             date TEXT,
             time TEXT)''')
conn.commit()
conn.close()

# Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO reservations (name, email, date, time) VALUES (?, ?, ?, ?)", (name, email, date, time))
        conn.commit()
        conn.close()
        
        return redirect(url_for('confirmation'))
    
    return render_template('reservation.html')

@app.route('/confirmation')
def confirmation():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reservations ORDER BY id DESC LIMIT 1")
    reservation = c.fetchone()
    conn.close()
    
    return render_template('confirmation.html', reservation=reservation)

@app.route('/reservation_list')
def reservation_list():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reservations")
    reservations = c.fetchall()
    conn.close()
    
    return render_template('reservation_list.html', reservations=reservations)

if __name__ == '__main__':
    app.run(debug=True)
