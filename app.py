from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Book(id={self.id}, book_name='{self.book_name}', author='{self.author}', publisher='{self.publisher}')"

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully!'})

# Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})
    return jsonify(result)

# Get a single book by id
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})

# Update a book by id
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'})

# Delete a book by id
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)