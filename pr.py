import os
import sqlite3
from flask import Flask, render_template, request, redirect
from init_db import init_db

app = Flask(__name__)

# Initialize the database and table if they don't exist
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            date=request.form.get('date','')
            tfn = int(request.form.get('tfn', 0))
            wtr = int(request.form.get('wtr', 0))
            prtn = int(request.form.get('prtn', 0))
            fc = int(request.form.get('fc', 0))
            gym = int(request.form.get('gym', 0))
            nm = float(request.form.get('nm', 0))
            tb = float(request.form.get('tb', 0))
            wrk = float(request.form.get('wrk', 0))
            wrkttl = float(request.form.get('wrkttl', 1))
            wrt = float(request.form.get('wrt', 0))
            wrtttl = float(request.form.get('wrtttl', 1))
            read = float(request.form.get('rd', 0))
            readttl = float(request.form.get('rdttl', 1))

            per = ((((tfn + wtr + prtn + fc) / 2) + gym + (wrk / wrkttl) + (wrt / wrtttl) + (read / readttl)) / 6)

            tbp = (tb / 4) * -0.2
            nmp = (nm / 1) * -0.2
            per = per + tbp + nmp
            result = per * 100

            # Save to database
            try:
                conn = sqlite3.connect('pr.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO pr (date, tfn, wtr, prtn, fc, gym, nm, tb, wrk, wrkttl, wrt, wrtttl, rd, rdttl, result)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (date, tfn, wtr, prtn, fc, gym, nm, tb, wrk, wrkttl, wrt, wrtttl, read, readttl, result))
                conn.commit()
                conn.close()
            except Exception as db_e:
                print(f"Database error: {db_e}")
            
            # Fetch all records to display
            try:
                conn = sqlite3.connect('pr.db')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM pr ORDER BY id DESC')
                data = cursor.fetchall()
                conn.close()
            except Exception as db_e:
                print(f"Database error fetching: {db_e}")
                data = []

        except Exception as e:
            result = f"Error: {str(e)}"
            data = []
            
        return render_template('prhtml.html', result=result, data=data)
        
    # GET request also needs to fetch data
    try:
        conn = sqlite3.connect('pr.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pr ORDER BY id DESC')
        data = cursor.fetchall()
        conn.close()
    except Exception as db_e:
        print(f"Database error fetching initial: {db_e}")
        data = []

    return render_template('prhtml.html', result=None, data=data)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    try:
        conn = sqlite3.connect('pr.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pr WHERE id = ?', (id,))
        cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM pr) WHERE name = 'pr'")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error deleting record: {e}")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
