import json
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/cars', methods=['POST'])
@token_required
def add_car(current_user_token):
    name = request.json['name']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    colour = request.json['colour']
    user_token = current_user_token.token

    print(f'Test: {current_user_token.token}')

    car = Car(name,make,model,year,colour,user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = contact_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(cars)
    return jsonify(response)

@api.route('cars/<car_id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, car_id):
    car = Car.query.get(car_id)
    response = contact_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<car_id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, car_id):
    car = Car.query.get(car_id)
    car.name = request.json['name']
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.colour = request.json['colour']
    car.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<car_id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, car_id):
    car = Car.query.get(car_id)
    db.session.delete(car)
    db.session.commit()
    response = contact_schema.dump(car)
    return jsonify(response)