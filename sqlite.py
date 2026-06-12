import sqlite3

connection = sqlite3.connect('agents.db')
## Create a cursor object to interact with the database
cursor = connection.cursor()

table_info = '''CREATE TABLE STUDENTS(NAME VARCHAR(25),
CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT) '''

cursor.execute(table_info)

## Commit the changes to the database
cursor.execute(''' INSERT INTO STUDENTS VALUES('Amit', 'Data Science', 'A', 85)''')
cursor.execute(''' INSERT INTO STUDENTS VALUES('Rahul', 'Data Science', 'B', 75)''')
cursor.execute(''' INSERT INTO STUDENTS VALUES('Priya', 'Data Science', 'A', 90)''')
cursor.execute(''' INSERT INTO STUDENTS VALUES('Sneha', 'Data Science', 'B', 80)''')
cursor.execute(''' INSERT INTO STUDENTS VALUES('Rohit', 'Data Science', 'A', 95)''')


## Display the data in the table
print("The Inserted Data in the Table is:")
data = cursor.execute(''' SELECT * FROM STUDENTS''')
for row in data:
    print(row)

## Commit the changes to the database
connection.commit()