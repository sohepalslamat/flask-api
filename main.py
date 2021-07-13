from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=True)
    
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    
    def serialize(context):
        all =[]
        for data in context:
            all.append({'id': data.id, 'name': data.name, 'price': data.price })
        all = jsonify(all)
        return all

db.create_all()

def serialize(book):
        
    return {
        'id': book.id,
        'name': book.name,
        "price": book.price
    }


@app.route("/books", methods=['GET', 'POST'])
def books_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        req = request.get_json(force=True)
                
        name = req['name']
        price = req['price']
        book = Books(name, price)
        db.session.add(book)
        db.session.commit()
        return 'created', status.HTTP_201_CREATED

    # request.method == 'GET'
    elif request.method == "GET":
        books = Books.query.all()
        books = Books.serialize(books)
        return books, status.HTTP_200_OK


@app.route("/books/<int:id>/", methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def book_detail(id):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'PUT':
        req = request.get_json(force=True)
        name = req['name']
        price = req['price']
        
        book = db.session.query(Books).filter_by(id = id).one()
        book.name = name
        book.price = price
        db.session.commit()
        return serialize(book), status.HTTP_200_OK

    elif request.method == 'PATCH':
        book = db.session.query(Books).filter_by(id = id).one()
        
        name = request.args.get('name')
        if not name:
            pass
        else:
            book.name = name
        
        price = request.args.get('price')
        if not price:
            pass
        else:
            book.price = price
        
        db.session.commit()
        
        return serialize(book), status.HTTP_200_OK
        
    elif request.method == 'DELETE':
        Books.query.filter_by(id=id).delete()
        db.session.commit()
        return 'deleted', status.HTTP_204_NO_CONTENT

    if request.method == 'GET':
        try:
            book = db.session.query(Books).filter_by(id = id).one()
            return serialize(book), status.HTTP_200_OK
        except:
            raise exceptions.NotFound()
        

        


if __name__ == "__main__":
    app.run(debug=True)