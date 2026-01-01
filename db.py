import sqlite3
conn = sqlite3.connect("books.sqlite")   #if boooks db doesn't exist this command will generate by itself
 
 #we should an idea of structure of db, for eg in this, there will be four attributes, 
 #id, title, author, language

 # nextwe need is cursor object (used ti execute sql statements)

cursor = conn.cursor()
sql_query= """ CREATE TABLE book(
    id integer PRIMARY KEY,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
)"""

cursor.execute(sql_query)