import sqlite3

def init_db():
    conn = sqlite3.connect('pr.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            tfn INTEGER,
            wtr INTEGER,
            prtn INTEGER,
            fc INTEGER,
            gym INTEGER,
            nm REAL,
            tb REAL,
            wrk REAL,
            wrkttl REAL,
            wrt REAL,
            wrtttl REAL,
            rd REAL,
            rdttl REAL,
            result REAL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
