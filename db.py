import sqlite3
from contextlib import closing

conn = None

def connect():
    global conn
    if not conn:
        DB_FILE = "session_db.sqlite"
    DB_FILE = "session_db.sqlite"
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row   # so we can access columns by their names from the query result

def close():
    if conn:
        conn.close()

def create_session():
    #Task 1
    c = conn.cursor()
    c.execute("CREATE table IF NOT EXISTS Session (sessionID INTEGER PRIMARY KEY, startTime TEXT, startMoney REAL, stopTime TEXT, stopMoney REAL);")
    #Task 2
    if (get_last_session()):
        pass
    else:
        c.execute("INSERT INTO Session(sessionID, startTime, startMoney, stopTime, stopMoney) VALUES(0, 'x', 199, 'y', 199);")
        conn.commit()

def get_last_session():
    query = "SELECT * FROM Session ORDER BY sessionID DESC;"
    with closing(conn.cursor()) as c:
        c.execute(query)
        lastSession = c.fetchone()
    return lastSession

def add_session(s):
    c = conn.cursor()
    c.execute("INSERT INTO Session VALUES(?, ?, ?, ? ,?)", (s.sessionID, s.startTime, s.startMoney, s.stopTime, s.stopMoney))
    conn.commit()



def main():
    connect()
    create_session()
    session = get_last_session()
    #print("Money:", session[4]])
    close()

if __name__ == "__main__":
    main()