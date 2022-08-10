import os
import psycopg2
from flask import Flask, render_template
from os.path import expanduser

with open(expanduser('~/pgpass.txt'), 'r') as f:
    host, port, database, user, password = f.read().split(':')

#database_uri = 'postgresql://{}:{}@epamdb:5432/{}'.format(user, password, host, port, database)
#print(f'user is {user}')
# print(password.rstrip())
password = password.rstrip()
#print(f'database is {database}')
#print(len(password))
#user = (user)
#print(user)
#print(type(password))
#print(password)
conn = psycopg2.connect(dbname=(database), user=(user), password=(password), host='epamdb')
cursor = conn.cursor()
#cursor.execute("SELECT * FROM author")
#author_records = cursor.fetchall()

# postgreSQL_author_Query = "SELECT * FROM author"
# cursor.execute(postgreSQL_author_Query)
# author_records = cursor.fetchall()
# print("Print each row and it's columns values")
# for row in author_records:
#     print("Id = ", row[0], )
#     print("Author = ", row[1])
# auth_id = row[0]
# auth_author = row[1]

app = Flask(__name__)

@app.route("/")
def start_page():
    postgreSQL_author_Query = "SELECT * FROM author"
    cursor.execute(postgreSQL_author_Query)
    author_records = cursor.fetchall()
    print(author_records)
    print(type(author_records))
    print("Print each row and it's columns values")
    for row in author_records:
        print("Id = ", row[0], )
        print("Author = ", row[1])
    auth_id = row[0]
    print(type(auth_id))
    auth_author = row[1]
    print(type(auth_author))

    return render_template('main.html', author_records=author_records)

if __name__ == "__main__":
    app.run()
cursor.close()
conn.close()