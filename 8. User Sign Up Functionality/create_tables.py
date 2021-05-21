import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Use INTEGER for auto incrementing id automatically instead of int
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()
connection.close()
