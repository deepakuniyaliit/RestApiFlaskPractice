#Reference - https://docs.python.org/3/library/sqlite3.html

import sqlite3

'''
create a connection object that represents the database named data.db.
The data stored this way will be persistent and will be available in subsequent sessions.

You can also supply the special name :memory: to create a database in RAM.
sqlite3.connect(":memory:")
'''

connection = sqlite3.connect('data.db')


# create a cursor object and call its execute() method to perform SQL commands
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'deepak', '123')

'''
Usually your SQL operations will need to use values from Python variables.
You shouldn’t assemble your query using Python’s string operations because doing so is insecure.
It makes your program vulnerable to an SQL injection attack.

# Never do this -- insecure!
symbol = 'RHAT'
cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

Instead, use the DB-API’s parameter substitution.
Put a placeholder wherever you want to use a value, and then provide a tuple of values as the second argument to the cursor’s execute() method.
An SQL statement may use one of two kinds of placeholders: question marks (qmark style) or named placeholders (named style).
For the qmark style, parameters must be a sequence.
For the named style, it can be either a sequence or dict instance.
The length of the sequence must match the number of placeholders, or a ProgrammingError is raised.
If a dict is given, it must contain keys for all named parameters. Any extra items are ignored. 
'''

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'sandeep', '456'),
    (3, 'vipin', '567')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

'''
Here is the named style:
cursor.execute("select * from users where id=:val", {"val":'1'})
print(cursor.fetchall())
It will print - [(1, 'deepak', '123')]
'''

for row in cursor.execute(select_query):
    print(row)

# save the changes and close connection
connection.commit()
connection.close()
