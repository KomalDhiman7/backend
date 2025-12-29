from flask import Flask, request, jsonify

app = Flask (__name__)

books_list=[
     {
         'id':0,
         "author":"chinua achebe",
         "language":"english",
         "title":"things fall apart",
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


# ------Dynamic routing----------
# @app.route('/<name>')
# def greetings(name):
#     return 'Hey, Good Morning, {}'.format(name)

# --------------Building an API----------------
@app.route('/books', methods=['GET','POST'])
def books():
    if request.method == 'GET':
        return jsonify(books_list)

    else:
        'Nothing Found',404

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']

        new_id = books_list[-1]['id'] + 1

        new_obj = {
            'id': new_id,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }

        books_list.append(new_obj)
        return jsonify(new_obj), 201
    
@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):

    # GET single book
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
        return jsonify({'error': 'Book not found'}), 404

    # UPDATE book
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

    # DELETE book
    if request.method == 'DELETE':
        for index, book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(index)
                return jsonify({'message': 'Book deleted'})
        return jsonify({'error': 'Book not found'}), 404
