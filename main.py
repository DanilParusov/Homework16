import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import json_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        return {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "age": self.age,
                "email": self.email,
                "role": self.role,
                "phone": self.phone,
            }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # user = db.relationship(User)

    def to_dict(self):
        return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "address": self.address,
                "price": self.price,
                "customer_id": self.customer_id,
                "executor_id": self.executor_id
            }

class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # order = db.relationship(Order)
    # user = db.relationship(User)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }

with app.app_context():
    db.create_all()

    for user in json_data.users:
        new_user = User(**user)
        db.session.add(new_user)
        db.session.commit()

    for order in json_data.orders:
        order['start_date'] = datetime.strptime(order['start_date'], '%m/%d/%Y').date()
        order['end_date'] = datetime.strptime(order['end_date'], '%m/%d/%Y').date()
        new_order = Order(**order)
        db.session.add(new_order)
        db.session.commit()

    for offer in json_data.offers:
        new_offer = Offer(**offer)
        db.session.add(new_offer)
        db.session.commit()


@app.route("/users", methods=['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        users = User.query.all()
        response = [user.to_dict() for user in users]
        return jsonify(response)
    elif request.method == 'POST':
        data = json.loads(request.data)
        db.session.add(User(**data))
        db.session.commit()
        return 'User добавлен'

@app.route("/users/<id>", methods=['GET','DELETE', 'PUT'])
def get_user(id):
    user = User.query.get(id)
    if request.method == 'GET':
        return jsonify(User.to_dict(user))
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return 'User удален'
    elif request.method == 'PUT':
        data = json.loads(request.data)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']
        db.session.add(user)
        db.session.commit()
        return 'User обновлен'

@app.route("/orders", methods=['GET', 'POST'])
def all_orders():
    if request.method == 'GET':
        orders = Order.query.all()
        response = [order.to_dict() for order in orders]
        return jsonify(response)
    elif request.method == 'POST':
        data = json.loads(request.data)
        db.session.add(Order(**data))
        db.session.commit()
        return 'Order добавлен'

@app.route("/orders/<id>", methods=['GET','DELETE', 'PUT'])
def get_order(id):
    order = Order.query.get(id)
    if request.method == 'GET':
        return jsonify(Order.to_dict(order))
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return 'Order удален'
    elif request.method == 'PUT':
        data = json.loads(request.data)
        order.name = data['name']
        order.description = data['description']
        order.start_date = data['start_date']
        order.end_date = data['end_date']
        order.address = data['address']
        order.price = data['price']
        order.customer_id = data['customer_id']
        order.executor_id = data['executor_id']
        return 'Order обновлен'

@app.route("/offers", methods=['GET', 'POST'])
def all_offers():
    if request.method == 'GET':
        offers = Offer.query.all()
        response = [offer.to_dict() for offer in offers]
        return jsonify(response)
    elif request.method == 'POST':
        data = json.loads(request.data)
        db.session.add(Offer(**data))
        db.session.commit()
        return 'Offer добавлен'

@app.route("/offers/<id>", methods=['GET','DELETE', 'PUT'])
def get_offer(id):
    offer = Order.query.get(id)
    if request.method == 'GET':
        return jsonify(Offer.to_dict(offer))
    elif request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return 'Offer удален'
    elif request.method == 'PUT':
        data = json.loads(request.data)
        offer.order_id = data['order_id']
        offer.executor_id = data['executor_id']
        return 'Offer обновлен'

app.run()


