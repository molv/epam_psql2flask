from os.path import expanduser
import psycopg2
import requests
from flask import Flask, render_template
import threading
import time

'''Grab credentials from .pgpass file, saved in the current user`s directory'''
with open(expanduser('~/pgpass.txt'), 'r') as f:
    host, port, database, user, password = f.read().split(':')

'''Delete spaces at the end'''
password = password.rstrip()

'''Connecting to the DB'''
conn = psycopg2.connect(dbname=(database), user=(user), password=(password), host='epamdb')
cursor = conn.cursor()

app = Flask(__name__)
'''Actions when requesting / page from flask'''
@app.route("/")
def start_page():
    '''get data from 'author' table and save to variable 'author_records' '''
    postgreSQL_author_Query = "SELECT * FROM author"
    cursor.execute(postgreSQL_author_Query)
    author_records = cursor.fetchall()

    '''Generate html, using received data and templates from 'main.html' file'''
    return render_template('main.html', author_records=author_records)
    '''Disconnect from DB'''
    cursor.close()
    conn.close()

'''Send get request to flask, save response to 'req' variable.
Then write outuput to the file.
Repeat in 60 sec'''
def request_page():
    while(True):
        # print(f'executing while loop')
        req = requests.get('http://127.0.0.1:5000/')
        with open("my_new_file.html", "w") as fh:
            fh.write(req.text)
        time.sleep(60)

'''Execute flask code as thread'''
def run_app():
    app.run(debug=False, threaded=True)

'''run flask code, then request the web page and save it as file'''
if __name__ == "__main__":
    first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=request_page)
    first_thread.start()
    second_thread.start()

