from flask import Flask, jsonify, g
import sqlite3
app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/api1')
def api1():
    # define your logic to get data here
    data = {"message": "Hello from API 1!"}

    # insert data into database
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO api_data VALUES (?)", (data["message"],))
    db.commit()
    c.close()

    return jsonify(data)
@app.route('/api2')
def api2():
    # retrieve data from database
    db = get_db()
    c = db.cursor()
    c.execute("SELECT message FROM api_data")
    rows = c.fetchall()
    data = []
    for row in rows:
        data.append(row[0])
        break
    c.close()
    data1 = ["Hello from API 2! "]
    messages =data + data1
    # data1["message"] = "Hello from API 2! " + data
    db = get_db()
    c = db.cursor()
    c.executemany('INSERT INTO api_data (message) VALUES (?)',
                   [(message,) for message in messages])
    db.commit()
    c.close()
    

    # return jsonify(data)
    return jsonify(messages)

    
if __name__ == '__main__':
    app.run(debug=True, port=2005)
