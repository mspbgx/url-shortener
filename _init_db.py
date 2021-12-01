import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
# Test Data
cur.execute("INSERT INTO urls (id, created, updated, short_url, long_url) VALUES (?, ?, ?, ?, ?)",
            (1, '2021-11-30', '2021-11-30', 'https://short.local/test', 'https://google.de')
            )

connection.commit()
connection.close()