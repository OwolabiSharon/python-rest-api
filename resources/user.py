from db import db
from models.user import User
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask_jwt_extended import create_access_token,create_refresh_token
#from flask_mail import *

class register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('middlename',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('date_of_birth',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pin',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = register.parser.parse_args()
        if User.find_by_phone_number(data['phone_number']):
            return {'message':'user exists already '} ,400
        user = User(data['phone_number'],data['firstname'],data['middlename'],data['lastname'],data['date_of_birth'],
        data['password'],data['email'],data['pin'],'00')
        User.save_to_db(user)
        return {
        'status': True,
        'data': user.json(),
        'message':'message'
        },201


class login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = login.parser.parse_args()
        user = User.find_by_phone_number(data['phone_number']) and User.find_by_password(data['password'])
        if user is not None:
            access_token = create_access_token(identity=user.id,fresh =True)
            refresh_token= create_refresh_token(user.id)
            return {
                  'access_token':access_token,
                  'message':'you are logged in'
            },200
        return {
        'status':True,
        'message':'user not found'
        }, 404

@jwt_required()
class account_balance(Resource):
#    global users
    def get(self, phone_number):
        user = User.find_by_phone_number(phone_number)
        if user:
            return jsonify(user.money_in_the_bag)
        return {'user': 'does not exist'}

@jwt_required()
class Top_up(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('ammount',
                        type= float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def put(self):
        data = Top_up.parser.parse_args()
        user = User.find_by_phone_number(data['phone_number'])
        user.money_in_the_bag = float(user.money_in_the_bag)
        if user:
            user.money_in_the_bag = data['ammount'] + user.money_in_the_bag
            user.money_in_the_bag =str(user.money_in_the_bag)
            User.save_to_db(user)
            return jsonify(user.money_in_the_bag)
        #return{'ddhhd':'blabla'}

@jwt_required()
class transfer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pin',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('ammount',
                        type= float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('destination_phone_number',
                        type= str,
                        required=True,
                        help="This field cannot be left blank!"
                        )


    def post(self):
        data = transfer.parser.parse_args()

        user = User.find_by_phone_number(data['phone_number']) and User.find_by_pin(data['pin'])
        destination = User.find_by_phone_number(data['destination_phone_number'])


        user.money_in_the_bag = float(user.money_in_the_bag)
        destination.money_in_the_bag = float(destination.money_in_the_bag)

        if user is not None and destination is not None:
            destination.money_in_the_bag = data['ammount'] + destination.money_in_the_bag
            user.money_in_the_bag = data['ammount'] - user.money_in_the_bag
            user.money_in_the_bag =str(user.money_in_the_bag)
            destination.money_in_the_bag =str(destination.money_in_the_bag)
            User.save_to_db(user)
            return {
            #'account_balance':jsonify(user.money_in_the_bag),
            'message':'money done commot for your account'
                  }
        return{'message':'either your account or the destination account does not exist'}
