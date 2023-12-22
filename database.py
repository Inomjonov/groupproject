
import sqlite3


#Connect to db
def connect():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, urgency TEXT)")
    conn.commit()
    conn.close()

#Insert data to db
def insertdata(task, urgency):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks VALUES (NULL, ?, ?)", (task, urgency))
    conn.commit()
    conn.close()

#Get data from db
def show():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()
    return rows

#Delete task from db
def deletebytask(task_id):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

connect()

