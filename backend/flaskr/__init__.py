import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there. 
#     If you do not update the endpoints, the lab will not work - of no fault of your API code! 
#   - Make sure for each route that you're thinking through when to abort and with which kind of error 
#   - If you change any of the response body keys, make sure you update the frontend to correspond. 

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  # @TODO: Write a route that retrivies all books, paginated. 
  #         You can use the constant above to paginate by eight books.
  #         If you decide to change the number of books per page,
  #         update the frontend to handle additional books in the styling and pagination
  #         Response body keys: 'success', 'books' and 'total_books'
  # TEST: When completed, the webpage will display books including title, author, and rating shown as stars

  @app.route('/books')
  def get_books():
    books = Book.query.all()
    page = request.args.get('page',1,type=int)
    start = (page - 1)*8
    end = start + 8
    formatted_books = [book.format() for book in books]
    
    return jsonify({
        'success':True,
        'books':formatted_books[start:end],
        'total_books':len(formatted_books)
    })


  

  # @TODO: Write a route that will update a single book's rating. 
  #         It should only be able to update the rating, not the entire representation
  #         and should follow API design principles regarding method and route.  
  #         Response body keys: 'success'
  # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh

  @app.route('/books/<int:book_id>', methods=['PATCH'])
  def book_rating(book_id):
    
   book = Book.query.filter_by(Book.id==book_id).one_or_none()
   book.rating = book.rating + 1
   print(book.rating)
   book.update()
    
   return jsonify({
        'success': True,
        'book_rating':book.rating,
        'book':book.format()
    })
  # @TODO: Write a route that will delete a single book. 
  #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
  #        Response body keys: 'success', 'books' and 'total_books'

  # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.

  @app.route('/books/<int:book_id>', methods=['DELETE'])
  def rem_particular_book(book_id):
    books = Book.query.filter_by(book_id==Book.id).one_or_none()
    books.delete()
    
    return jsonify({
        'success':True,
        'deleted':Book.id,
        'books':books.format()
    })
    
  # @TODO: Write a route that create a new book. 
  #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
  # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books. 
  #       Your new book should show up immediately after you submit it at the end of the page. 
  


  @app.route('/books', methods=['POST'])
  def new_book():
    body = request.get_json()
    book = Book(
    body.get('title'),
    body.get('author'),
    int(body.get('rating'))
    )
    book.insert()
    book = Book.query.order_by('id').all
    formatted_books = [book.format() for book in Book]
    page = request.args.get('page',1, type=int)
    start = (page - 1) * 8
    end = start + 8
    
    return jsonify({
        'success':True,
        'Created':Book.id,
        'books':formatted_books[start:end],
        'total_books':len(formatted_books)
    })


