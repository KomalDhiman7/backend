from flask import Flask, request, jsonify
import json
import sqlite3



# FIX 1: Correct Flask app initialization (no space)
app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

#####################################################
def create_table():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            language TEXT,
            title TEXT
        )
    """)
    conn.commit()
    conn.close()


create_table() 


# In-memory list (used only for /books/<id>)
books_list = [
    {
        'id': 0,
        "author": "chinua achebe",
        "language": "english",
        "title": "things fall apart",
    },
    {
        'id': 1,
        "author": "hans christian andersen",
        "language": "danish",
        "title": "fairy tales",
    },
    {
        'id': 2,
        "author": "samuel beckett",
        "language": "french,english",
        "title": "molloy,malone dies,the unnamable,the triology",
    },
    {
        'id': 6,
        "author": "jorge luis borges",
        "language": "spanish",
        "title": "ficciones",
    },
    {
        'id': 3,
        "author": "giovanni boccaccio",
        "language": "italian",
        "title": "the decameron",
    },
    {
        'id': 5,
        "author": "emily bront",
        "language": "english",
        "title": "wuthering heights",
    },
]

@app.route('/')
def index():
    return 'Hello World'


# ------------------ BOOKS API ------------------
@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    # GET all books from DATABASE
    if request.method == 'GET':
        # FIX 2: Proper SQL execution
        cursor.execute("SELECT * FROM book")
        rows = cursor.fetchall()

        # FIX 3: Convert DB rows to JSON
        books = []
        for row in rows:
            books.append({
                "id": row[0],
                "author": row[1],
                "language": row[2],
                "title": row[3]
            })

        return jsonify(books)

    # POST new book into DATABASE
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']

        # FIX 4:
        # - Table name corrected (Boob -> book)
        # - Extra comma removed
        # - Query executed properly
        sql = "INSERT INTO book (author, language, title) VALUES (?, ?, ?)"
        cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()

        return jsonify({'message': 'Book added successfully'}), 201


# ------------------ SINGLE BOOK API ------------------
@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):

    # GET single book (from in-memory list)
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
        return jsonify({'error': 'Book not found'}), 404

    # UPDATE book (in-memory list)
    if request.method == 'PUT':
        for book in books_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']

                updated_book = {
                    'id': id,
                    'author': book['author'],
                    'language': book['language'],
                    'title': book['title']
                }
                return jsonify(updated_book)

        return jsonify({'error': 'Book not found'}), 404

    # DELETE book (in-memory list)
    if request.method == 'DELETE':
        for index, book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(index)
                return jsonify({'message': 'Book deleted'})

        # FIX 5: Removed stray closing bracket that caused syntax error
        return jsonify({'error': 'Book not found'}), 404
